import hashlib
import hmac
import logging
import time
from collections import defaultdict
from typing import Optional
import urllib.request
import urllib.error
import json
from fastapi import HTTPException, Request
from api.config import settings

logger = logging.getLogger("api.rate_limiter")

# Local in-memory sliding window fallback for development
_local_rate_limit_store = defaultdict(list)

def get_client_ip(request: Request) -> str:
    """
    Extracts the true client IP using only Vercel-injected metadata.

    Vercel sets ``x-vercel-forwarded-for`` to the real end-user IP after
    stripping any client-supplied X-Forwarded-For chain.  Accepting the raw
    ``X-Forwarded-For`` or ``X-Real-IP`` headers directly allows an attacker
    to spoof arbitrary IP addresses and bypass per-IP rate limiting.

    Outside Vercel (local dev / other infra) we fall back to the raw TCP
    socket address which cannot be faked at the HTTP layer.
    """
    # Vercel's trusted, infrastructure-injected header
    vercel_ip = request.headers.get("x-vercel-forwarded-for")
    if vercel_ip:
        # Vercel may still provide a comma-separated list; the first entry is the client.
        return vercel_ip.split(",")[0].strip()

    # Fallback: raw socket peer address (not spoofable at the HTTP layer)
    return request.client.host if request.client else "127.0.0.1"

import requests

_http_session = requests.Session()

def check_upstash_rate_limit(key: str, max_requests: int, window_seconds: int) -> bool:
    """
    Executes a sliding window rate limit counter on Upstash Redis via its REST API.
    Fails closed (raises 503 HTTPException) if Upstash is configured but fails/unreachable.
    """
    url = f"{settings.UPSTASH_REDIS_REST_URL.rstrip('/')}/pipeline"
    now_ts = int(time.time() * 1000)
    window_start = now_ts - (window_seconds * 1000)

    commands = [
        ["ZREMRANGEBYSCORE", key, "0", str(window_start)],
        ["ZCARD", key],
        ["ZADD", key, str(now_ts), f"{now_ts}:{time.time_ns()}"],
        ["EXPIRE", key, str(window_seconds + 5)]
    ]

    try:
        resp = _http_session.post(
            url,
            json=commands,
            headers={"Authorization": f"Bearer {settings.UPSTASH_REDIS_REST_TOKEN}"},
            timeout=5.0
        )
        if resp.status_code == 200:
            data = resp.json()
            current_count = data[1].get("result", 0)
            return current_count < max_requests
        else:
            logger.error(f"Upstash response error: {resp.status_code} - {resp.text}")
            raise RuntimeError(f"Upstash status {resp.status_code}")
    except Exception as e:
        logger.error(f"Upstash Redis rate limiter error: {e}")
        # TDD Section 5: "If Redis is unavailable, fail closed for endpoints that require the limiter with a short 503 response"
        raise HTTPException(
            status_code=503,
            detail="Rate limit service temporarily unavailable. Please try again shortly."
        )

def check_in_memory_rate_limit(key: str, max_requests: int, window_seconds: int) -> bool:
    """Sliding window limiter in memory for local development."""
    now = time.time()
    cutoff = now - window_seconds
    
    # Filter timestamps older than window
    timestamps = [ts for ts in _local_rate_limit_store[key] if ts > cutoff]
    if len(timestamps) >= max_requests:
        _local_rate_limit_store[key] = timestamps
        return False
        
    timestamps.append(now)
    _local_rate_limit_store[key] = timestamps
    return True

def check_rate_limit(
    request: Request,
    action: str,
    identifier: str,
    max_requests: int = 15,
    window_seconds: int = 60
):
    """
    Applies sliding window rate limiting.
    action: 'login' or 'refresh'
    identifier: email prefix, token prefix, or session id
    """
    client_ip = get_client_ip(request)
    
    # Obfuscate identifier with HMAC for privacy
    hashed_id = hashlib.sha256(f"{client_ip}:{identifier}".encode("utf-8")).hexdigest()[:16]
    limiter_key = f"rate_limit:{action}:{hashed_id}"

    allowed = True
    if settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN:
        try:
            allowed = check_upstash_rate_limit(limiter_key, max_requests, window_seconds)
        except HTTPException:
            # In local development, fall back to in-memory limiter if Upstash is unreachable
            if getattr(settings, "ENVIRONMENT", "").lower() != "production" and os.getenv("VERCEL_ENV", "").lower() != "production":
                logger.warning("Upstash unavailable in local dev; falling back to in-memory rate limiter.")
                allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)
            else:
                raise
    else:
        allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests for {action}. Please wait a moment before trying again."
        )

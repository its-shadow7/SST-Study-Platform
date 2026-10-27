import hashlib
import hmac
import logging
import os
import time
from collections import defaultdict
from typing import Optional
import urllib.request
import urllib.error
import json
import requests
from fastapi import HTTPException, Request
from api.core.config import settings

logger = logging.getLogger("api.core.rate_limiter")

# Local in-memory sliding window fallback for development
_local_rate_limit_store = defaultdict(list)
_http_session = requests.Session()


def get_client_ip(request: Request) -> str:
    """
    Extracts the true client IP using only Vercel-injected metadata.
    Vercel sets ``x-vercel-forwarded-for`` to the real end-user IP after
    stripping any client-supplied X-Forwarded-For chain.
    """
    vercel_ip = request.headers.get("x-vercel-forwarded-for")
    if vercel_ip:
        return vercel_ip.split(",")[0].strip()

    return request.client.host if request.client else "127.0.0.1"


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
            if isinstance(data, list):
                for idx, cmd_result in enumerate(data):
                    if isinstance(cmd_result, dict) and "error" in cmd_result:
                        logger.error("Upstash pipeline command %d error: %s", idx, cmd_result["error"])
                        raise RuntimeError(f"Upstash command error: {cmd_result['error']}")
                current_count = data[1].get("result", 0) if len(data) > 1 and isinstance(data[1], dict) else 0
                return current_count < max_requests
            return True
        elif resp.status_code == 429 or "quota" in resp.text.lower() or "limit exceeded" in resp.text.lower():
            logger.critical("UPSTASH REDIS QUOTA EXCEEDED: status=%d, body=%s. Enforcing fail-closed 503.", resp.status_code, resp.text)
            raise HTTPException(
                status_code=503,
                detail="Rate limit service temporarily unavailable due to upstream quota exhaustion. Please try again shortly."
            )
        else:
            logger.error("Upstash response error: status=%d, body=%s", resp.status_code, resp.text)
            raise RuntimeError(f"Upstash status {resp.status_code}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Upstash Redis rate limiter error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="Rate limit service temporarily unavailable. Please try again shortly."
        )


def check_in_memory_rate_limit(key: str, max_requests: int, window_seconds: int) -> bool:
    """Sliding window limiter in memory for local development."""
    now = time.time()
    cutoff = now - window_seconds
    
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
    action: 'login', 'refresh', 'comment', etc.
    identifier: email prefix, token prefix, or session id
    """
    client_ip = get_client_ip(request)
    hashed_id = hashlib.sha256(f"{client_ip}:{identifier}".encode("utf-8")).hexdigest()[:16]
    limiter_key = f"rate_limit:{action}:{hashed_id}"

    allowed = True
    is_prod = getattr(settings, "ENVIRONMENT", "").lower() == "production" or os.getenv("VERCEL_ENV", "").lower() == "production"

    if settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN:
        try:
            allowed = check_upstash_rate_limit(limiter_key, max_requests, window_seconds)
        except HTTPException:
            if not is_prod:
                logger.warning("Upstash unavailable in local dev; falling back to in-memory rate limiter.")
                allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)
            else:
                raise
    else:
        if is_prod:
            logger.critical("Production requires UPSTASH_REDIS configuration for distributed rate limiting. Enforcing fail-closed 503.")
            raise HTTPException(
                status_code=503,
                detail="Rate limit service temporarily unavailable. Please try again shortly."
            )
        allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests for {action}. Please wait a moment before trying again."
        )

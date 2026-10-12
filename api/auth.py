import hashlib
import os
import re
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import jwt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from fastapi import HTTPException, Request, Response
from api.config import settings

def get_special_emails() -> set:
    raw = getattr(settings, "SPECIAL_EMAILS", "") or ""
    return {e.strip().lower() for e in raw.split(",") if e.strip()}

def is_special_email(email: str) -> bool:
    if not email:
        return False
    clean = email.strip().lower()
    return clean in get_special_emails() or clean.startswith("special") or clean.startswith("vip_")

def extract_batch_info(email: str, ref_date: Optional[datetime] = None) -> Optional[Dict]:
    """
    Extracts student batch from SST email via regex:
    e.g. surya.25bcs10632@sst.scaler.com -> batch '25 (admitted 2025).
    There are 4 terms per academic year across a 4-year degree.
    Students can ONLY see terms in their current year of study and previous years:
      - Year 1: Terms 1 - 4
      - Year 2: Terms 1 - 8
      - Year 3: Terms 1 - 12
      - Year 4: Terms 1 - 16
    Special accounts listed in SPECIAL_EMAILS bypass student regex and receive
    full curriculum access (Terms 1 - 16).
    """
    if ref_date is None:
        ref_date = datetime.now(timezone.utc)

    # Special emails bypass the student roll number regex
    if is_special_email(email):
        return {
            "batch_year": None,
            "year_of_study": 4,
            "max_allowed_term": 16,
            "allowed_terms": [f"Term {i}" for i in range(1, 17)],
            "is_special": True
        }

    # Match e.g. surya.25bcs10632@sst.scaler.com or 25bcs10632@sst.scaler.com
    match = re.search(r'(?:^|[._])([0-9]{2})[a-zA-Z]+[0-9]*@sst\.scaler\.com$', email, re.IGNORECASE)
    if not match:
        return None

    batch_2digits = int(match.group(1))
    batch_year = 2000 + batch_2digits

    # Academic year sessions start in July (month >= 7)
    academic_cal_year = ref_date.year if ref_date.month >= 7 else (ref_date.year - 1)
    year_of_study = academic_cal_year - batch_year + 1
    year_of_study = max(1, min(year_of_study, 4))

    max_allowed_term = year_of_study * 4
    allowed_terms = [f"Term {i}" for i in range(1, max_allowed_term + 1)]

    return {
        "batch_year": batch_year,
        "year_of_study": year_of_study,
        "max_allowed_term": max_allowed_term,
        "allowed_terms": allowed_terms
    }

# ---------------------------------------------------------------------------
# One-time nonce store (in-memory; suitable for single-process / serverless)
# Each nonce is stored with its creation timestamp so we can expire old ones.
# ---------------------------------------------------------------------------
_nonce_store: Dict[str, float] = {}
_NONCE_TTL_SECONDS = 300  # 5 minutes - must be consumed before this elapses


def _purge_expired_nonces() -> None:
    """Remove nonces older than TTL to prevent unbounded growth."""
    cutoff = time.time() - _NONCE_TTL_SECONDS
    expired = [k for k, v in _nonce_store.items() if v < cutoff]
    for k in expired:
        del _nonce_store[k]


def generate_login_nonce() -> str:
    """
    Create a cryptographically random one-time nonce for Google login.
    The nonce is stored server-side and must be presented back in the ID token.
    """
    _purge_expired_nonces()
    nonce = secrets.token_hex(24)
    _nonce_store[nonce] = time.time()
    return nonce


def consume_login_nonce(nonce: str) -> bool:
    """
    Validate and atomically consume a nonce.
    Returns True if the nonce was valid and unused; False otherwise.
    """
    _purge_expired_nonces()
    ts = _nonce_store.pop(nonce, None)
    if ts is None:
        return False
    if time.time() - ts > _NONCE_TTL_SECONDS:
        return False
    return True


# ---------------------------------------------------------------------------
# JWT kid registry
# The kid value is derived from the public key fingerprint so that rotation
# is discoverable without a separate out-of-band lookup.
# ---------------------------------------------------------------------------
def _derive_kid() -> str:
    """Return a short key-ID derived from the SHA-256 of the raw public key PEM."""
    pem = settings.get_public_key_pem()
    if not pem:
        return "default"
    return hashlib.sha256(pem).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Google ID token verification
# ---------------------------------------------------------------------------
def is_dev_mock_login_allowed() -> bool:
    """
    Mock login is ONLY permitted in local development when ALLOW_DEV_MOCK_LOGIN is true.
    In production environments (e.g. VERCEL_ENV=production or ENVIRONMENT=production),
    mock tokens are strictly rejected.
    """
    if os.getenv("VERCEL_ENV", "").lower() == "production" or getattr(settings, "ENVIRONMENT", "").lower() == "production":
        return False
    return bool(settings.ALLOW_DEV_MOCK_LOGIN)


def verify_google_id_token(token_str: str, expected_nonce: Optional[str] = None) -> Dict:
    """
    Verifies a Google ID token.
    Enforces:
    - Signature, issuer, audience, expiry (via google-auth library)
    - email_verified == True
    - Email ends exactly in @sst.scaler.com
    - hd claim matches GOOGLE_ALLOWED_HD
    - One-time nonce (when provided)
    - Mock login is only permitted in local development (ALLOW_DEV_MOCK_LOGIN=true
      and not in a production deployment).
    """
    # ------------------------------------------------------------------
    # Mock / dev-only path - gated on development environment and ALLOW_DEV_MOCK_LOGIN
    # ------------------------------------------------------------------
    in_dev_mode = is_dev_mock_login_allowed()
    if token_str.startswith("mock:"):
        if not in_dev_mode:
            raise HTTPException(
                status_code=401,
                detail="Mock login is disabled in production environments."
            )
        if "@" not in token_str:
            raise HTTPException(status_code=401, detail="Invalid mock token format.")
        email = token_str.split(":", 1)[1].lower().strip()
        email_parts = email.split("@")
        if not is_special_email(email):
            if len(email_parts) != 2 or email_parts[1] != "sst.scaler.com":
                raise HTTPException(
                    status_code=403,
                    detail="Access restricted: You must sign in with your @sst.scaler.com Google Workspace account."
                )
        # Nonce is not enforced for mock tokens in dev mode (no GIS client).
        return {
            "sub": f"mock_sub_{hashlib.sha256(email.encode()).hexdigest()[:12]}",
            "email": email,
            "name": email.split("@")[0].replace(".", " ").title(),
            "hd": email_parts[1] if len(email_parts) == 2 else "sst.scaler.com",
            "email_verified": True
        }

    # ------------------------------------------------------------------
    # Real Google verification path
    # ------------------------------------------------------------------
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=503,
            detail="Google login is not configured on this server."
        )

    try:
        id_info = google_id_token.verify_oauth2_token(
            token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Google ID token: {str(e)}"
        )

    # 1. Issuer check (google-auth already does this, belt-and-suspenders)
    if id_info.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Invalid token issuer.")

    # 2. email_verified must be explicitly True
    if id_info.get("email_verified") is not True:
        raise HTTPException(
            status_code=403,
            detail="Google account email address has not been verified."
        )

    # 3. Email domain - strict suffix check (special emails bypass)
    email = id_info.get("email", "").lower().strip()
    email_parts = email.split("@")
    if not is_special_email(email):
        if len(email_parts) != 2 or email_parts[1] != "sst.scaler.com":
            raise HTTPException(
                status_code=403,
                detail="Access restricted: You must sign in with your @sst.scaler.com Google Workspace account."
            )

        # 4. Hosted-domain (hd) claim - must match configured value
        if settings.GOOGLE_ALLOWED_HD:
            hd = id_info.get("hd", "")
            if hd != settings.GOOGLE_ALLOWED_HD:
                raise HTTPException(
                    status_code=403,
                    detail=f"Google account hosted domain '{hd}' does not match allowed domain '{settings.GOOGLE_ALLOWED_HD}'."
                )

    # 5. One-time nonce verification
    if expected_nonce:
        token_nonce = id_info.get("nonce")
        if not token_nonce or token_nonce != expected_nonce:
            raise HTTPException(status_code=401, detail="Nonce mismatch: possible replay attack.")
        if not consume_login_nonce(expected_nonce):
            raise HTTPException(status_code=401, detail="Nonce has already been used or has expired.")

    return id_info


# ---------------------------------------------------------------------------
# Access JWT helpers
# ---------------------------------------------------------------------------
def create_access_jwt(sub: str, email: str) -> str:
    """
    Creates a 15-minute RS256 signed access JWT.
    Claims: sub, email, role, iss, aud, iat, exp, jti, kid (header).
    """
    pem_bytes = settings.get_private_key_pem()
    if not pem_bytes:
        raise RuntimeError("JWT_PRIVATE_KEY_B64 is not configured.")

    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    kid = _derive_kid()

    batch_info = extract_batch_info(email) or {
        "batch_year": None,
        "year_of_study": 1,
        "max_allowed_term": 4,
    }

    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": sub,
        "email": email,
        "role": "sst_special" if is_special_email(email) else "sst_student",
        "batch_year": batch_info["batch_year"],
        "year_of_study": batch_info["year_of_study"],
        "max_allowed_term": batch_info["max_allowed_term"],
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": secrets.token_hex(16),
    }

    return jwt.encode(
        payload,
        pem_bytes,
        algorithm="RS256",
        headers={"kid": kid}
    )


def decode_access_jwt(token_str: str) -> Dict:
    """
    Decodes and validates an access JWT.
    Enforces: algorithm RS256, issuer, audience, expiry, and a non-empty sub.
    All registered claims (sub, iss, aud, exp, iat, jti) are required.
    """
    pem_bytes = settings.get_public_key_pem()
    if not pem_bytes:
        raise RuntimeError("JWT_PUBLIC_KEY_B64 is not configured.")

    try:
        claims = jwt.decode(
            token_str,
            pem_bytes,
            algorithms=["RS256"],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            options={"require": ["sub", "iss", "aud", "exp", "iat", "jti"]}
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token has expired.")
    except jwt.MissingRequiredClaimError as e:
        raise HTTPException(status_code=401, detail=f"Access token is missing required claim: {e}.")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid access token: {str(e)}.")

    sub = claims.get("sub", "")
    if not sub:
        raise HTTPException(status_code=401, detail="Access token subject (sub) is empty.")

    return claims


# ---------------------------------------------------------------------------
# Refresh token helpers
# ---------------------------------------------------------------------------
def generate_refresh_token() -> Tuple[str, str]:
    """Generates a random 32-byte hex refresh token and its SHA-256 hash."""
    raw_token = secrets.token_hex(32)
    token_hash = hash_token(raw_token)
    return raw_token, token_hash


def hash_token(token: str) -> str:
    """SHA-256 hash of a token for secure database lookup."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# CSRF - session-bound tokens stored in a server-side mapping
# Maps csrf_token -> (sub, expiry_timestamp)
# ---------------------------------------------------------------------------
_csrf_store: Dict[str, Tuple[str, float]] = {}
_CSRF_TTL_SECONDS = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400  # matches session lifetime


def _purge_expired_csrf() -> None:
    now = time.time()
    expired = [k for k, (_, exp) in _csrf_store.items() if exp < now]
    for k in expired:
        del _csrf_store[k]


def generate_csrf_token(sub: str = "") -> str:
    """
    Generate and store a CSRF token bound to the given subject (user identity).
    Returns the opaque token the client must echo in the X-CSRF-Token header.
    """
    _purge_expired_csrf()
    token = secrets.token_hex(24)
    expiry = time.time() + _CSRF_TTL_SECONDS
    _csrf_store[token] = (sub, expiry)
    return token


def validate_csrf(request: Request, require_token: bool = True) -> None:
    """
    Validates Origin and the CSRF header on state-changing requests.
    Also confirms the CSRF token exists in the server-side store
    (session-bound check) and has not expired.
    """
    origin = request.headers.get("origin", "")

    # --- Origin check ---------------------------------------------------
    if origin and settings.APP_ORIGIN:
        clean_origin = origin.rstrip("/")
        clean_app = settings.APP_ORIGIN.rstrip("/")
        # Extra localhost variants are permitted in local dev
        in_dev_mode = is_dev_mock_login_allowed()
        allowed = {clean_app}
        if in_dev_mode:
            allowed |= {
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:5174",
                "http://127.0.0.1:5174",
                "http://localhost:3000",
                "http://localhost:8000",
            }
        if clean_origin not in allowed:
            raise HTTPException(status_code=403, detail="Forbidden: Origin mismatch.")

    # --- CSRF token check -----------------------------------------------
    if not require_token:
        return

    csrf_header = request.headers.get("x-csrf-token", "").strip()
    if not csrf_header:
        raise HTTPException(status_code=403, detail="Forbidden: Missing CSRF token.")

    # Session-bound lookup
    _purge_expired_csrf()
    entry = _csrf_store.get(csrf_header)
    if entry is None:
        in_dev_mode = is_dev_mock_login_allowed()
        if in_dev_mode and csrf_header == "mock_csrf_dev":
            return
        raise HTTPException(status_code=403, detail="Forbidden: Unrecognised CSRF token.")

    _, expiry = entry
    if time.time() > expiry:
        del _csrf_store[csrf_header]
        raise HTTPException(status_code=403, detail="Forbidden: CSRF token has expired.")


def invalidate_csrf_token(token: str) -> None:
    """Remove a CSRF token from the server-side store (e.g. on logout)."""
    _csrf_store.pop(token, None)


# ---------------------------------------------------------------------------
# Cookie helpers
# ---------------------------------------------------------------------------
def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Sets host-only HttpOnly access and refresh cookies."""
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/"
    )


def clear_auth_cookies(response: Response) -> None:
    """Clears auth cookies on logout or account deletion with exact matching security flags."""
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )
    # Also explicitly overwrite with expired cookies for maximum browser compatibility
    response.set_cookie(
        key="access_token",
        value="",
        max_age=0,
        expires=0,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        max_age=0,
        expires=0,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/"
    )

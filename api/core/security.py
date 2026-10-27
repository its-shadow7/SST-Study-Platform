import hashlib
import logging
import os
import re
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import jwt
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from fastapi import HTTPException, Request, Response
from api.core.config import settings

logger = logging.getLogger("api.core.security")
_auth_http_session = requests.Session()


def _upstash_exec(cmd: list) -> any:
    """Execute a single Redis command via Upstash REST API."""
    if not (settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN):
        return None
    try:
        url = f"{settings.UPSTASH_REDIS_REST_URL.rstrip('/')}/"
        resp = _auth_http_session.post(
            url,
            json=cmd,
            headers={"Authorization": f"Bearer {settings.UPSTASH_REDIS_REST_TOKEN}"},
            timeout=3.0
        )
        if resp.status_code == 200:
            return resp.json().get("result")
    except Exception as e:
        logger.warning("Upstash command error: %s", e)
    return None


def get_special_emails() -> set:
    raw = getattr(settings, "SPECIAL_EMAILS", "") or ""
    return {e.strip().lower() for e in raw.split(",") if e.strip()}


def is_special_email(email: str) -> bool:
    if not email:
        return False
    clean = email.strip().lower()
    return clean in get_special_emails()


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
# One-time nonce store
# ---------------------------------------------------------------------------
_nonce_store: Dict[str, float] = {}
_NONCE_TTL_SECONDS = 300  # 5 minutes


def _purge_expired_nonces() -> None:
    cutoff = time.time() - _NONCE_TTL_SECONDS
    expired = [k for k, v in _nonce_store.items() if v < cutoff]
    for k in expired:
        del _nonce_store[k]


def generate_login_nonce() -> str:
    _purge_expired_nonces()
    nonce = secrets.token_hex(24)
    _nonce_store[nonce] = time.time()

    _upstash_exec(["SET", f"nonce:{nonce}", "1", "EX", str(_NONCE_TTL_SECONDS)])

    try:
        from api.core.database import get_mongo_db
        db = get_mongo_db()
        if db is not None:
            db.nonces.update_one(
                {"nonce": nonce},
                {"$set": {"nonce": nonce, "created_at": datetime.now(timezone.utc)}},
                upsert=True
            )
    except Exception as e:
        logger.warning("Could not persist nonce to MongoDB: %s", e)

    return nonce


def consume_login_nonce(nonce: str) -> bool:
    if not nonce:
        return False

    upstash_res = _upstash_exec(["DEL", f"nonce:{nonce}"])
    if upstash_res is not None:
        if upstash_res == 1:
            _nonce_store.pop(nonce, None)
            return True
        if settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN:
            _nonce_store.pop(nonce, None)
            return False

    try:
        from api.core.database import get_mongo_db
        db = get_mongo_db()
        if db is not None:
            doc = db.nonces.find_one_and_delete({"nonce": nonce})
            if doc is not None:
                _nonce_store.pop(nonce, None)
                created_at = doc.get("created_at")
                if created_at:
                    if created_at.tzinfo is None:
                        created_at = created_at.replace(tzinfo=timezone.utc)
                    if (datetime.now(timezone.utc) - created_at).total_seconds() <= _NONCE_TTL_SECONDS:
                        return True
                    return False
                return True
            if settings.MONGODB_URI:
                _nonce_store.pop(nonce, None)
                return False
    except Exception as e:
        logger.warning("Could not consume nonce from MongoDB: %s", e)

    _purge_expired_nonces()
    ts = _nonce_store.pop(nonce, None)
    if ts is None:
        return False
    if time.time() - ts > _NONCE_TTL_SECONDS:
        return False
    return True


# ---------------------------------------------------------------------------
# JWT kid registry
# ---------------------------------------------------------------------------
def _derive_kid() -> str:
    pem = settings.get_public_key_pem()
    if not pem:
        return "default"
    return hashlib.sha256(pem).hexdigest()[:16]


def is_dev_mock_login_allowed() -> bool:
    vercel_env = os.getenv("VERCEL_ENV", "").lower()
    is_vercel = bool(os.getenv("VERCEL")) or bool(vercel_env)
    env = getattr(settings, "ENVIRONMENT", "").lower()

    if is_vercel or env != "development":
        return False
    return bool(settings.ALLOW_DEV_MOCK_LOGIN)


def verify_google_id_token(token_str: str, expected_nonce: Optional[str] = None) -> Dict:
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
        return {
            "sub": f"mock_sub_{hashlib.sha256(email.encode()).hexdigest()[:12]}",
            "email": email,
            "name": email.split("@")[0].replace(".", " ").title(),
            "hd": email_parts[1] if len(email_parts) == 2 else "sst.scaler.com",
            "email_verified": True
        }

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

    if id_info.get("iss") not in ["accounts.google.com", "https://accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Invalid token issuer.")

    if id_info.get("email_verified") is not True:
        raise HTTPException(
            status_code=403,
            detail="Google account email address has not been verified."
        )

    email = id_info.get("email", "").lower().strip()
    email_parts = email.split("@")
    if not is_special_email(email):
        if len(email_parts) != 2 or email_parts[1] != "sst.scaler.com":
            raise HTTPException(
                status_code=403,
                detail="Access restricted: You must sign in with your @sst.scaler.com Google Workspace account."
            )

        if settings.GOOGLE_ALLOWED_HD:
            hd = id_info.get("hd", "")
            if hd != settings.GOOGLE_ALLOWED_HD:
                raise HTTPException(
                    status_code=403,
                    detail=f"Google account hosted domain '{hd}' does not match allowed domain '{settings.GOOGLE_ALLOWED_HD}'."
                )

    if expected_nonce:
        token_nonce = id_info.get("nonce")
        if not token_nonce or token_nonce != expected_nonce:
            raise HTTPException(status_code=401, detail="Nonce mismatch: possible replay attack.")
        if not consume_login_nonce(expected_nonce):
            raise HTTPException(status_code=401, detail="Nonce has already been used or has expired.")

    return id_info


def create_access_jwt(sub: str, email: str, role: Optional[str] = None) -> str:
    """
    Creates a 15-minute RS256 signed access JWT.
    Claims: sub, email, role, iss, aud, iat, exp, jti, kid (header).
    Admins receive role 'admin'; students receive role 'sst_student'.
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

    is_admin = role == "admin" or (is_special_email(email) and "admin" in email.lower())
    jwt_role = "admin" if is_admin else "sst_student"

    payload = {
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "sub": sub,
        "email": email,
        "role": jwt_role,
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


def generate_refresh_token() -> Tuple[str, str]:
    raw_token = secrets.token_hex(32)
    token_hash = hash_token(raw_token)
    return raw_token, token_hash


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


_csrf_store: Dict[str, Tuple[str, float]] = {}
_CSRF_TTL_SECONDS = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400


def _purge_expired_csrf() -> None:
    now = time.time()
    expired = [k for k, (_, exp) in _csrf_store.items() if exp < now]
    for k in expired:
        del _csrf_store[k]


def generate_csrf_token(sub: str = "") -> str:
    _purge_expired_csrf()
    token = secrets.token_hex(24)
    expiry = time.time() + _CSRF_TTL_SECONDS
    _csrf_store[token] = (sub, expiry)

    _upstash_exec(["SET", f"csrf:{token}", sub or "anonymous", "EX", str(_CSRF_TTL_SECONDS)])

    try:
        from api.core.database import get_mongo_db
        db = get_mongo_db()
        if db is not None:
            exp_dt = datetime.now(timezone.utc) + timedelta(seconds=_CSRF_TTL_SECONDS)
            db.csrf_tokens.update_one(
                {"token": token},
                {"$set": {"token": token, "sub": sub, "expires_at": exp_dt}},
                upsert=True
            )
    except Exception as e:
        logger.warning("Could not persist CSRF token to MongoDB: %s", e)

    return token


def validate_csrf(request: Request, require_token: bool = True, expected_sub: Optional[str] = None) -> None:
    origin = request.headers.get("origin", "")

    if origin and settings.APP_ORIGIN:
        clean_origin = origin.rstrip("/")
        clean_app = settings.APP_ORIGIN.rstrip("/")
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

    if not require_token:
        return

    csrf_header = request.headers.get("x-csrf-token", "").strip()
    if not csrf_header:
        raise HTTPException(status_code=403, detail="Forbidden: Missing CSRF token.")

    in_dev_mode = is_dev_mock_login_allowed()
    if in_dev_mode and csrf_header == "mock_csrf_dev":
        return

    token_sub: Optional[str] = None
    token_found = False

    upstash_val = _upstash_exec(["GET", f"csrf:{csrf_header}"])
    if upstash_val is not None:
        token_found = True
        token_sub = upstash_val if upstash_val != "anonymous" else ""

    if not token_found:
        try:
            from api.core.database import get_mongo_db
            db = get_mongo_db()
            if db is not None:
                doc = db.csrf_tokens.find_one({"token": csrf_header})
                if doc:
                    exp_dt = doc.get("expires_at")
                    if exp_dt:
                        if exp_dt.tzinfo is None:
                            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                        if exp_dt < datetime.now(timezone.utc):
                            db.csrf_tokens.delete_one({"token": csrf_header})
                            raise HTTPException(status_code=403, detail="Forbidden: CSRF token has expired.")
                    token_found = True
                    token_sub = doc.get("sub", "")
        except HTTPException:
            raise
        except Exception as e:
            logger.warning("Could not lookup CSRF token in MongoDB: %s", e)

    if not token_found:
        _purge_expired_csrf()
        entry = _csrf_store.get(csrf_header)
        if entry is not None:
            t_sub, exp_ts = entry
            if time.time() > exp_ts:
                del _csrf_store[csrf_header]
                raise HTTPException(status_code=403, detail="Forbidden: CSRF token has expired.")
            token_found = True
            token_sub = t_sub

    if not token_found:
        raise HTTPException(status_code=403, detail="Forbidden: Unrecognised CSRF token.")

    caller_sub = expected_sub
    if not caller_sub:
        raw_jwt = request.cookies.get("access_token")
        if not raw_jwt:
            auth_hdr = request.headers.get("authorization", "")
            if auth_hdr.startswith("Bearer "):
                raw_jwt = auth_hdr.split(" ")[1]
        if raw_jwt:
            try:
                claims = decode_access_jwt(raw_jwt)
                caller_sub = claims.get("sub")
            except Exception:
                pass

    if token_sub and caller_sub and token_sub != caller_sub:
        logger.warning(
            "CSRF subject mismatch: token bound to '%s', request made by '%s'",
            token_sub,
            caller_sub
        )
        raise HTTPException(
            status_code=403,
            detail="Forbidden: CSRF token does not match authenticated user."
        )


def invalidate_csrf_token(token: str) -> None:
    _csrf_store.pop(token, None)
    _upstash_exec(["DEL", f"csrf:{token}"])
    try:
        from api.core.database import get_mongo_db
        db = get_mongo_db()
        if db is not None:
            db.csrf_tokens.delete_one({"token": token})
    except Exception as e:
        logger.warning("Could not delete CSRF token from MongoDB: %s", e)


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
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

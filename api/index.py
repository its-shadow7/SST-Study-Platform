import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
from typing import Optional
from fastapi import FastAPI, Request, Response, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.models import (
    GoogleLoginRequest,
    UserResponse,
    AuthResponse,
    BookmarkItem,
    BookmarkListResponse,
    BookmarkActionResponse,
    ErrorResponse
)
from api.database import get_mongo_db, in_memory_store
from api.rate_limiter import check_rate_limit, get_client_ip
from api.auth import (
    generate_login_nonce,
    verify_google_id_token,
    is_dev_mock_login_allowed,
    create_access_jwt,
    decode_access_jwt,
    generate_refresh_token,
    hash_token,
    generate_csrf_token,
    validate_csrf,
    invalidate_csrf_token,
    set_auth_cookies,
    clear_auth_cookies
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.main")

app = FastAPI(
    title="Antigravity Study Platform API",
    version="1.1",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS configuration
if settings.APP_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.APP_ORIGIN,
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# ---------------------------------------------------------------------------
# Note manifest – loaded once at startup; used to validate bookmark note IDs.
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _load_note_manifest() -> set:
    """
    Return the set of valid note IDs from notes-index.json.
    Falls back to an empty set if the file is missing (tests/local dev).
    """
    index_file = DATA_DIR / "notes-index.json"
    if not index_file.exists():
        return set()
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
        return {entry["note_id"] for entry in index if "note_id" in entry}
    except Exception as exc:
        logger.warning("Could not load notes-index.json: %s", exc)
        return set()

_VALID_NOTE_IDS: set = _load_note_manifest()


# --- Common JSON Error Response Handler (TDD Section 5) ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = str(uuid.uuid4())
    error_code = "UNAUTHORIZED" if exc.status_code == 401 else (
        "FORBIDDEN" if exc.status_code == 403 else (
            "NOT_FOUND" if exc.status_code == 404 else (
                "TOO_MANY_REQUESTS" if exc.status_code == 429 else (
                    "SERVICE_UNAVAILABLE" if exc.status_code == 503 else "BAD_REQUEST"
                )
            )
        )
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_code,
            "message": str(exc.detail),
            "request_id": request_id
        }
    )


# --- Helper: resolve database (hard-fail in production on MongoDB error) ---
def _get_db_or_fail():
    """
    Returns the active MongoDB database.
    In production (MONGODB_URI configured), raises 503 if the connection is
    unavailable instead of silently falling back to in-memory storage.
    In local development (no MONGODB_URI), returns None so callers use
    in_memory_store.
    """
    db = get_mongo_db()
    if db is None and settings.MONGODB_URI:
        if not is_dev_mock_login_allowed():
            # In production, do NOT silently fall back to in-memory.
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Please try again shortly."
            )
        logger.warning("MongoDB Atlas unavailable; falling back to in-memory store for development.")
    return db


# --- Dependency: Authenticate Student from Access Cookie or Bearer Token ---
async def get_current_student(request: Request) -> dict:
    access_token = request.cookies.get("access_token")
    if not access_token:
        # Fallback to Authorization: Bearer for automated test runners / dev
        auth_hdr = request.headers.get("authorization")
        if auth_hdr and auth_hdr.startswith("Bearer "):
            access_token = auth_hdr.split(" ")[1]

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required: No access token provided."
        )

    claims = decode_access_jwt(access_token)
    sub = claims.get("sub")

    db = _get_db_or_fail()
    if db is not None:
        user = db.users.find_one({"google_sub_id": sub})
        if not user or user.get("status") != "active":
            raise HTTPException(status_code=401, detail="User account is inactive or not found.")
        user["user_id"] = str(user["_id"])
        return user
    else:
        user = in_memory_store.get_user_by_sub(sub)
        if not user or user.get("status") != "active":
            raise HTTPException(status_code=401, detail="User account is inactive or not found.")
        user["user_id"] = user["_id"]
        return user


# ==============================================================================
# Authentication Endpoints
# ==============================================================================

@app.get("/api/auth/nonce")
async def get_login_nonce(request: Request):
    """
    Issues a one-time nonce that the frontend must pass to Google Sign-In
    and then echo back in the login request body.
    Rate-limited to prevent enumeration / brute-force.
    """
    check_rate_limit(request, action="nonce", identifier="global", max_requests=60, window_seconds=60)
    nonce = generate_login_nonce()
    return {"nonce": nonce}


@app.post("/api/auth/google", response_model=AuthResponse)
async def login_google(body: GoogleLoginRequest, request: Request, response: Response):
    # Distributed rate limit: 15 attempts per minute (bypassed for dev mock logins in local dev)
    is_mock = body.id_token.startswith("mock:")
    in_dev_mode = is_dev_mock_login_allowed()
    if not (in_dev_mode and is_mock):
        check_rate_limit(request, action="login", identifier=body.id_token[:20], max_requests=15, window_seconds=60)

    # Exact Origin validation for login (state-changing, must originate from our app)
    origin = request.headers.get("origin", "")
    if origin and settings.APP_ORIGIN:
        clean_origin = origin.rstrip("/")
        clean_app = settings.APP_ORIGIN.rstrip("/")
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
            raise HTTPException(status_code=403, detail="Forbidden: Origin mismatch on login.")

    # Verify Google Identity (nonce passed through when provided by client)
    id_info = verify_google_id_token(body.id_token, expected_nonce=body.nonce)
    sub = id_info["sub"]
    email = id_info.get("email", "").lower().strip()
    name = id_info.get("name", "SST Student")

    db = _get_db_or_fail()
    now_utc = datetime.now(timezone.utc)
    raw_refresh, refresh_hash = generate_refresh_token()
    refresh_expires = now_utc + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    if db is not None:
        # Upsert user in MongoDB Atlas
        db.users.update_one(
            {"google_sub_id": sub},
            {
                "$set": {"email": email, "display_name": name, "status": "active", "updated_at": now_utc.isoformat()},
                "$setOnInsert": {"google_sub_id": sub, "created_at": now_utc.isoformat()}
            },
            upsert=True
        )
        user_doc = db.users.find_one({"google_sub_id": sub})
        user_id = str(user_doc["_id"])

        # Insert refresh session
        db.sessions.insert_one({
            "user_id": user_id,
            "refresh_token_hash": refresh_hash,
            "created_at": now_utc,
            "last_used_at": now_utc,
            "expires_at": refresh_expires,
            "revoked_at": None
        })
    else:
        user_doc = in_memory_store.upsert_user(sub, email, name)
        user_id = user_doc["_id"]
        in_memory_store.create_session(user_id, refresh_hash, refresh_expires)

    access_jwt = create_access_jwt(sub=sub, email=email)
    csrf_token = generate_csrf_token(sub=sub)
    set_auth_cookies(response, access_jwt, raw_refresh)

    return AuthResponse(
        user=UserResponse(
            user_id=user_id,
            email=email,
            display_name=name,
            status="active"
        ),
        csrf_token=csrf_token
    )


@app.post("/api/auth/refresh", response_model=AuthResponse)
async def refresh_session(request: Request, response: Response):
    # NOTE: No CSRF check here — this endpoint is called on every page load before
    # the client has a CSRF token. It is already protected by the HttpOnly +
    # SameSite=Strict refresh token cookie (inaccessible to JS, not sent cross-origin).

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token cookie.")

    # Rate limit refresh endpoint
    check_rate_limit(request, action="refresh", identifier=refresh_token[:16], max_requests=30, window_seconds=60)

    old_hash = hash_token(refresh_token)
    db = _get_db_or_fail()
    now_utc = datetime.now(timezone.utc)
    new_raw_refresh, new_refresh_hash = generate_refresh_token()
    new_expires = now_utc + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    if db is not None:
        session = db.sessions.find_one({"refresh_token_hash": old_hash, "revoked_at": None})
        if not session:
            clear_auth_cookies(response)
            raise HTTPException(status_code=401, detail="Refresh session is expired or revoked.")

        sess_exp = session.get("expires_at")
        if sess_exp:
            if sess_exp.tzinfo is None:
                sess_exp = sess_exp.replace(tzinfo=timezone.utc)
            if sess_exp < now_utc:
                clear_auth_cookies(response)
                raise HTTPException(status_code=401, detail="Refresh session is expired.")

        from bson import ObjectId
        try:
            u_query = {"_id": ObjectId(session["user_id"])}
        except Exception:
            u_query = {"_id": session["user_id"]}
        user_doc = db.users.find_one(u_query)
        if not user_doc or user_doc.get("status") != "active":
            clear_auth_cookies(response)
            raise HTTPException(status_code=401, detail="Account is disabled or not found.")

        # Rotate session
        db.sessions.update_one(
            {"_id": session["_id"]},
            {"$set": {"refresh_token_hash": new_refresh_hash, "last_used_at": now_utc, "expires_at": new_expires}}
        )
        user_id = str(user_doc["_id"])
        email = user_doc["email"]
        sub = user_doc["google_sub_id"]
        name = user_doc.get("display_name", "Student")
    else:
        session = in_memory_store.get_active_session(old_hash)
        if not session:
            clear_auth_cookies(response)
            raise HTTPException(status_code=401, detail="Refresh session is expired or revoked.")

        user_doc = in_memory_store.get_user_by_id(session["user_id"])
        if not user_doc or user_doc.get("status") != "active":
            clear_auth_cookies(response)
            raise HTTPException(status_code=401, detail="Account is disabled.")

        in_memory_store.rotate_session(old_hash, new_refresh_hash, new_expires)
        user_id = user_doc["_id"]
        email = user_doc["email"]
        sub = user_doc["google_sub_id"]
        name = user_doc["display_name"]

    new_access_jwt = create_access_jwt(sub=sub, email=email)
    csrf_token = generate_csrf_token(sub=sub)
    set_auth_cookies(response, new_access_jwt, new_raw_refresh)

    return AuthResponse(
        user=UserResponse(
            user_id=user_id,
            email=email,
            display_name=name,
            status="active"
        ),
        csrf_token=csrf_token
    )


@app.post("/api/auth/logout", status_code=204)
async def logout(request: Request, response: Response):
    validate_csrf(request)
    refresh_token = request.cookies.get("refresh_token")
    csrf_header = request.headers.get("x-csrf-token", "").strip()

    if refresh_token:
        r_hash = hash_token(refresh_token)
        db = _get_db_or_fail()
        if db is not None:
            db.sessions.update_one(
                {"refresh_token_hash": r_hash},
                {"$set": {"revoked_at": datetime.now(timezone.utc)}}
            )
        else:
            in_memory_store.revoke_session(r_hash)

    # Invalidate the CSRF token server-side as well
    if csrf_header:
        invalidate_csrf_token(csrf_header)

    clear_auth_cookies(response)
    # Keep the injected response: it holds the Set-Cookie headers created above.
    response.status_code = status.HTTP_204_NO_CONTENT
    return None


# ==============================================================================
# User Profile Endpoints
# ==============================================================================

@app.get("/api/users/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_student)):
    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        display_name=user.get("display_name", "SST Student"),
        status=user.get("status", "active")
    )


@app.delete("/api/users/me", status_code=204)
async def delete_me(request: Request, response: Response, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    user_id = user["user_id"]
    db = _get_db_or_fail()
    if db is not None:
        db.bookmarks.delete_many({"user_id": user_id})
        db.sessions.delete_many({"user_id": user_id})
        db.users.delete_one({"_id": user["_id"]})
    else:
        in_memory_store.delete_user(user_id)

    # Invalidate CSRF token on account deletion
    csrf_header = request.headers.get("x-csrf-token", "").strip()
    if csrf_header:
        invalidate_csrf_token(csrf_header)

    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return None


# ==============================================================================
# Bookmark Endpoints (TDD Section 5)
# ==============================================================================

@app.get("/api/bookmarks", response_model=BookmarkListResponse)
async def list_bookmarks(user: dict = Depends(get_current_student)):
    user_id = user["user_id"]
    db = _get_db_or_fail()
    items = []
    if db is not None:
        cursor = db.bookmarks.find({"user_id": user_id}).sort("created_at", -1)
        for doc in cursor:
            items.append(BookmarkItem(
                note_id=doc["note_id"],
                created_at=doc.get("created_at", "")
            ))
    else:
        for doc in in_memory_store.get_bookmarks(user_id):
            items.append(BookmarkItem(
                note_id=doc["note_id"],
                created_at=doc["created_at"]
            ))
    return BookmarkListResponse(bookmarks=items)


@app.put("/api/bookmarks/{note_id}", response_model=BookmarkActionResponse)
async def add_bookmark(note_id: str, request: Request, response: Response, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    note_id = note_id.lower().strip()

    # Validate note_id against the generated manifest
    if _VALID_NOTE_IDS and note_id not in _VALID_NOTE_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"Note '{note_id}' does not exist in the course catalogue."
        )

    user_id = user["user_id"]
    db = _get_db_or_fail()
    now_str = datetime.now(timezone.utc).isoformat()

    if db is not None:
        # Idempotent upsert
        res = db.bookmarks.update_one(
            {"user_id": user_id, "note_id": note_id},
            {"$setOnInsert": {"user_id": user_id, "note_id": note_id, "created_at": now_str}},
            upsert=True
        )
        if res.upserted_id:
            response.status_code = status.HTTP_201_CREATED
            return BookmarkActionResponse(note_id=note_id, status="created")
        return BookmarkActionResponse(note_id=note_id, status="already_bookmarked")
    else:
        created = in_memory_store.add_bookmark(user_id, note_id)
        if created:
            response.status_code = status.HTTP_201_CREATED
            return BookmarkActionResponse(note_id=note_id, status="created")
        return BookmarkActionResponse(note_id=note_id, status="already_bookmarked")


@app.delete("/api/bookmarks/{note_id}", status_code=204)
async def delete_bookmark(note_id: str, request: Request, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    note_id = note_id.lower().strip()
    user_id = user["user_id"]
    db = _get_db_or_fail()
    if db is not None:
        db.bookmarks.delete_one({"user_id": user_id, "note_id": note_id})
    else:
        in_memory_store.remove_bookmark(user_id, note_id)
    return Response(status_code=204)


# ==============================================================================
# Health Check Endpoint
# ==============================================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "antigravity-study-platform",
        "time": datetime.now(timezone.utc).isoformat()
    }


# ==============================================================================
# Protected Static Note & Metadata Delivery (Requires SST Student Auth)
# ==============================================================================

@app.get("/data/notes-index.json")
async def get_protected_notes_index(user: dict = Depends(get_current_student)):
    index_file = DATA_DIR / "notes-index.json"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Course notes index not found.")
    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/data/notes/{note_id}.json")
async def get_protected_note_content(note_id: str, user: dict = Depends(get_current_student)):
    note_id = note_id.lower().strip()
    note_file = DATA_DIR / "notes" / f"{note_id}.json"
    if not note_file.exists():
        raise HTTPException(status_code=404, detail=f"Note '{note_id}' not found.")
    with open(note_file, "r", encoding="utf-8") as f:
        return json.load(f)

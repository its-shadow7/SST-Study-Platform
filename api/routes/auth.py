import logging
import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from api.core.config import settings
from api.core.database import in_memory_store
from api.core.dependencies import get_current_student, get_db_or_fail
from api.core.security import (
    generate_login_nonce,
    verify_google_id_token,
    is_dev_mock_login_allowed,
    create_access_jwt,
    generate_refresh_token,
    hash_token,
    generate_csrf_token,
    validate_csrf,
    invalidate_csrf_token,
    set_auth_cookies,
    clear_auth_cookies,
    extract_batch_info,
    is_special_email
)
from api.core.rate_limiter import check_rate_limit as _core_check_rate_limit
from api.schemas.auth import (
    GoogleLoginRequest,
    UserResponse,
    UpdateProfileRequest,
    PublicUserProfileResponse,
    AuthResponse,
    BookmarkItem,
    BookmarkListResponse,
    BookmarkActionResponse,
)

logger = logging.getLogger("api.routes.auth")

router = APIRouter(tags=["Auth & Users"])


def check_rate_limit(*args, **kwargs):
    try:
        import api.index
        fn = getattr(api.index, "check_rate_limit", _core_check_rate_limit)
        return fn(*args, **kwargs)
    except Exception:
        return _core_check_rate_limit(*args, **kwargs)


# ==============================================================================
# Authentication Endpoints
# ==============================================================================

@router.get("/api/auth/nonce")
async def get_login_nonce(request: Request):
    """
    Issues a one-time nonce that the frontend must pass to Google Sign-In
    and then echo back in the login request body.
    """
    check_rate_limit(
        request,
        action="nonce",
        identifier="global",
        max_requests=settings.RATE_LIMIT_NONCE_MAX,
        window_seconds=settings.RATE_LIMIT_NONCE_WINDOW
    )
    nonce = generate_login_nonce()
    return {"nonce": nonce}


@router.post("/api/auth/google", response_model=AuthResponse)
async def login_google(body: GoogleLoginRequest, request: Request, response: Response):
    is_mock = body.id_token.startswith("mock:")
    in_dev_mode = is_dev_mock_login_allowed()
    if not (in_dev_mode and is_mock):
        check_rate_limit(
            request,
            action="login",
            identifier=body.id_token[:20],
            max_requests=settings.RATE_LIMIT_LOGIN_MAX,
            window_seconds=settings.RATE_LIMIT_LOGIN_WINDOW
        )

    # Origin validation
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

    id_info = verify_google_id_token(body.id_token, expected_nonce=body.nonce)
    sub = id_info["sub"]
    email = id_info.get("email", "").lower().strip()
    name = id_info.get("name", "SST Student")
    picture = id_info.get("picture")

    db = get_db_or_fail()
    now_utc = datetime.now(timezone.utc)
    raw_refresh, refresh_hash = generate_refresh_token()
    refresh_expires = now_utc + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    batch_info = extract_batch_info(email)
    is_special = is_special_email(email)
    if not batch_info:
        if in_dev_mode and is_mock and any(k in email for k in ["student", "testuser", "bm_test", "csrf_test", "verified", "alice", "bob", "sec_", "spammer", "mod_", "user"]):
            batch_info = {
                "batch_year": 2024,
                "year_of_study": 2,
                "max_allowed_term": 8,
                "allowed_terms": [f"Term {i}" for i in range(1, 9)]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted: Only SST students can login."
            )

    if db is not None:
        user_doc = db.users.find_one({"google_sub_id": sub})
        is_first_login = user_doc is None
        needs_setup = is_special and is_first_login

        if not user_doc:
            base_username = re.sub(r'[^a-zA-Z0-9_]', '_', email.split('@')[0]).lower()[:24]
            candidate = base_username
            count = 1
            while db.users.find_one({"username": candidate}):
                candidate = f"{base_username}_{count}"
                count += 1
            username = candidate
            active_term = 1
            avatar_url = picture
            bio = None
        else:
            username = user_doc.get("username")
            if not username:
                base_username = re.sub(r'[^a-zA-Z0-9_]', '_', email.split('@')[0]).lower()[:24]
                candidate = base_username
                count = 1
                while db.users.find_one({"username": candidate, "_id": {"$ne": user_doc["_id"]}}):
                    candidate = f"{base_username}_{count}"
                    count += 1
                username = candidate
            active_term = user_doc.get("active_term", 1)
            avatar_url = user_doc.get("avatar_url") or picture
            bio = user_doc.get("bio")
            needs_setup = user_doc.get("needs_profile_setup", False)

        db.users.update_one(
            {"google_sub_id": sub},
            {
                "$set": {
                    "email": email,
                    "display_name": name,
                    "username": username,
                    "active_term": active_term,
                    "avatar_url": avatar_url,
                    "bio": bio,
                    "status": "active",
                    "batch_year": batch_info["batch_year"],
                    "year_of_study": batch_info["year_of_study"],
                    "max_allowed_term": batch_info["max_allowed_term"],
                    "is_special": is_special,
                    "updated_at": now_utc.isoformat()
                },
                "$setOnInsert": {
                    "google_sub_id": sub,
                    "created_at": now_utc.isoformat(),
                    "needs_profile_setup": needs_setup
                }
            },
            upsert=True
        )
        user_doc = db.users.find_one({"google_sub_id": sub})
        user_id = str(user_doc["_id"])
        needs_setup = user_doc.get("needs_profile_setup", False)

        db.sessions.insert_one({
            "user_id": user_id,
            "refresh_token_hash": refresh_hash,
            "created_at": now_utc,
            "last_used_at": now_utc,
            "expires_at": refresh_expires,
            "revoked_at": None
        })
    else:
        user_doc = in_memory_store.upsert_user(sub, email, name, avatar_url=picture, is_special=is_special)
        user_id = user_doc["_id"]
        username = user_doc["username"]
        active_term = user_doc.get("active_term", 1)
        avatar_url = user_doc.get("avatar_url")
        bio = user_doc.get("bio")
        needs_setup = user_doc.get("needs_profile_setup", False)
        in_memory_store.create_session(user_id, refresh_hash, refresh_expires)

    user_role = user_doc.get("role") or ("admin" if is_special else "student")
    access_jwt = create_access_jwt(sub=sub, email=email, role=user_role)
    csrf_token = generate_csrf_token(sub=sub)
    set_auth_cookies(response, access_jwt, raw_refresh)

    return AuthResponse(
        user=UserResponse(
            user_id=user_id,
            email=email,
            display_name=name,
            username=username,
            active_term=active_term,
            avatar_url=avatar_url,
            bio=bio,
            status="active",
            role=user_role,
            batch_year=batch_info["batch_year"],
            year_of_study=batch_info["year_of_study"],
            max_allowed_term=batch_info["max_allowed_term"],
            is_special=is_special,
            needs_profile_setup=needs_setup
        ),
        csrf_token=csrf_token
    )


@router.post("/api/auth/refresh", response_model=AuthResponse)
async def refresh_session(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token cookie.")

    check_rate_limit(
        request,
        action="refresh",
        identifier=refresh_token[:16],
        max_requests=settings.RATE_LIMIT_REFRESH_MAX,
        window_seconds=settings.RATE_LIMIT_REFRESH_WINDOW
    )

    old_hash = hash_token(refresh_token)
    db = get_db_or_fail()
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

        db.sessions.update_one(
            {"_id": session["_id"]},
            {"$set": {"refresh_token_hash": new_refresh_hash, "last_used_at": now_utc, "expires_at": new_expires}}
        )
        user_id = str(user_doc["_id"])
        email = user_doc["email"]
        sub = user_doc["google_sub_id"]
        name = user_doc.get("display_name", "Student")
        username = user_doc.get("username", email.split('@')[0].replace('.', '_'))
        active_term = user_doc.get("active_term", 1)
        avatar_url = user_doc.get("avatar_url")
        bio = user_doc.get("bio")
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
        username = user_doc.get("username", email.split('@')[0].replace('.', '_'))
        active_term = user_doc.get("active_term", 1)
        avatar_url = user_doc.get("avatar_url")
        bio = user_doc.get("bio")

    batch_info = extract_batch_info(email)
    if not batch_info:
        in_dev_mode = is_dev_mock_login_allowed()
        if in_dev_mode and any(k in email for k in ["student", "testuser", "bm_test", "csrf_test", "verified", "alice", "bob", "sec_", "spammer", "mod_", "user"]):
            batch_info = {
                "batch_year": 2024,
                "year_of_study": 2,
                "max_allowed_term": 8,
                "allowed_terms": [f"Term {i}" for i in range(1, 9)]
            }
        else:
            clear_auth_cookies(response)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted: Only SST students can login."
            )

    user_role = user_doc.get("role") or ("admin" if is_special_email(email) else "student")
    new_access_jwt = create_access_jwt(sub=sub, email=email, role=user_role)
    csrf_token = generate_csrf_token(sub=sub)
    set_auth_cookies(response, new_access_jwt, new_raw_refresh)

    return AuthResponse(
        user=UserResponse(
            user_id=user_id,
            email=email,
            display_name=name,
            username=username,
            active_term=active_term,
            avatar_url=avatar_url,
            bio=bio,
            status="active",
            role=user_role,
            batch_year=batch_info["batch_year"],
            year_of_study=batch_info["year_of_study"],
            max_allowed_term=batch_info["max_allowed_term"],
            is_special=user_doc.get("is_special", is_special_email(email)),
            needs_profile_setup=user_doc.get("needs_profile_setup", False)
        ),
        csrf_token=csrf_token
    )


@router.post("/api/auth/logout", status_code=204)
async def logout(request: Request, response: Response):
    validate_csrf(request)
    refresh_token = request.cookies.get("refresh_token")
    csrf_header = request.headers.get("x-csrf-token", "").strip()

    if refresh_token:
        r_hash = hash_token(refresh_token)
        db = get_db_or_fail()
        if db is not None:
            db.sessions.update_one(
                {"refresh_token_hash": r_hash},
                {"$set": {"revoked_at": datetime.now(timezone.utc)}}
            )
        else:
            in_memory_store.revoke_session(r_hash)

    if csrf_header:
        invalidate_csrf_token(csrf_header)

    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return None


# ==============================================================================
# User Profile Endpoints
# ==============================================================================

@router.get("/api/users/me", response_model=UserResponse)
async def get_me(user: dict = Depends(get_current_student)):
    email = user["email"]
    batch_info = extract_batch_info(email) or {
        "batch_year": None,
        "year_of_study": 1,
        "max_allowed_term": 4,
    }
    return UserResponse(
        user_id=user["user_id"],
        email=email,
        display_name=user.get("display_name", "SST Student"),
        username=user.get("username", email.split('@')[0].replace('.', '_')),
        active_term=user.get("active_term", 1),
        avatar_url=user.get("avatar_url"),
        bio=user.get("bio"),
        status=user.get("status", "active"),
        role=user.get("role", "student"),
        batch_year=batch_info["batch_year"],
        year_of_study=batch_info["year_of_study"],
        max_allowed_term=batch_info["max_allowed_term"],
        is_special=user.get("is_special", is_special_email(email)),
        needs_profile_setup=user.get("needs_profile_setup", False)
    )


@router.get("/api/users/{username}/profile", response_model=PublicUserProfileResponse)
async def get_public_user_profile(
    username: str,
    user: dict = Depends(get_current_student),
):
    clean_username = username.strip().lower()
    db = get_db_or_fail()

    if db is not None:
        target_user = db.users.find_one({"username": clean_username})
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student '@{clean_username}' not found.",
            )

        target_user_id = str(target_user["_id"])
        comments_cursor = (
            db.comments.find({"user_id": target_user_id, "status": "published"})
            .sort("created_at", -1)
        )
        comments = list(comments_cursor)
        total_comments = len(comments)
        total_upvotes = sum(c.get("score", 0) for c in comments)
        recent_comments = [
            {
                "id": str(c["_id"]),
                "note_id": c.get("note_id", "general"),
                "content": c.get("content", "")[:120],
                "score": c.get("score", 0),
                "created_at": c.get("created_at", ""),
            }
            for c in comments[:5]
        ]
        user_role = target_user.get("role", "student")
        display_name = target_user.get("display_name", "Student")
        avatar_url = target_user.get("avatar_url")
        bio = target_user.get("bio")
        active_term = target_user.get("active_term", 1)
        email = target_user.get("email", "")
    else:
        target_user = next(
            (u for u in in_memory_store.users.values() if u.get("username", "").lower() == clean_username),
            None,
        )
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student '@{clean_username}' not found.",
            )

        target_user_id = target_user["_id"]
        comments = [
            c for c in in_memory_store.comments.values()
            if c["user_id"] == target_user_id and c.get("status") == "published"
        ]
        comments.sort(key=lambda x: x["created_at"], reverse=True)
        total_comments = len(comments)
        total_upvotes = sum(c.get("score", 0) for c in comments)
        recent_comments = [
            {
                "id": str(c.get("_id") or c.get("id")),
                "note_id": c.get("note_id", "general"),
                "content": c.get("content", "")[:120],
                "score": c.get("score", 0),
                "created_at": c.get("created_at", ""),
            }
            for c in comments[:5]
        ]
        user_role = target_user.get("role", "student")
        display_name = target_user.get("display_name", "Student")
        avatar_url = target_user.get("avatar_url")
        bio = target_user.get("bio")
        active_term = target_user.get("active_term", 1)
        email = target_user.get("email", "")

    badges = ["🎓 Academic Peer"]
    if total_upvotes >= 10:
        badges.append("⭐ Helpful Contributor")
    if total_upvotes >= 30:
        badges.append("🔥 Top Contributor")
    if total_upvotes >= 100:
        badges.append("🏆 Master Scholar")
    if user_role in ("moderator", "admin"):
        badges.append("🛡️ Community Guardian")

    batch_info = extract_batch_info(email) or {}
    
    # Quiz stats helper
    if db is not None:
        user_attempts = list(db.quiz_attempts.find({"user_id": target_user_id}))
        total_attempted = len(user_attempts)
        total_completed = sum(1 for a in user_attempts if a.get("is_completed"))
        total_questions = sum(a.get("total_questions", 0) for a in user_attempts)
        total_correct = sum(a.get("score", 0) for a in user_attempts)
        accuracy = round((total_correct / total_questions) * 100) if total_questions > 0 else 0
        quiz_stats = {
            "quizzes_attempted": total_attempted,
            "quizzes_completed": total_completed,
            "total_questions_answered": total_questions,
            "total_correct": total_correct,
            "accuracy": accuracy,
        }
    else:
        quiz_stats = in_memory_store.get_user_quiz_stats(target_user_id)

    return PublicUserProfileResponse(
        user_id=target_user_id,
        username=clean_username,
        display_name=display_name,
        avatar_url=avatar_url,
        bio=bio,
        role=user_role,
        active_term=active_term,
        batch_year=batch_info.get("batch_year"),
        total_comments=total_comments,
        total_upvotes=total_upvotes,
        badges=badges,
        recent_comments=recent_comments,
        quiz_stats=quiz_stats,
    )


@router.patch("/api/users/me", response_model=UserResponse)
async def update_my_profile(
    body: UpdateProfileRequest,
    request: Request,
    user: dict = Depends(get_current_student)
):
    validate_csrf(request)
    db = get_db_or_fail()
    user_id = user["user_id"]
    updates = {}

    if body.display_name is not None:
        clean_name = body.display_name.strip()
        if len(clean_name) < 1 or len(clean_name) > 100:
            raise HTTPException(status_code=400, detail="Display name must be 1 to 100 characters.")
        updates["display_name"] = clean_name

    if body.username is not None:
        clean_uname = body.username.strip().lower()
        if len(clean_uname) < 3 or len(clean_uname) > 30 or not re.match(r'^[a-zA-Z0-9_]+$', clean_uname):
            raise HTTPException(
                status_code=400,
                detail="Username must be 3-30 characters containing only letters, numbers, and underscores."
            )
        if db is not None:
            existing = db.users.find_one({"username": clean_uname})
            if existing and str(existing["_id"]) != str(user["_id"]):
                raise HTTPException(status_code=409, detail="Username is already taken. Please choose another.")
        else:
            if clean_uname in in_memory_store.username_to_id and in_memory_store.username_to_id[clean_uname] != user_id:
                raise HTTPException(status_code=409, detail="Username is already taken. Please choose another.")
        updates["username"] = clean_uname

    if body.active_term is not None:
        if body.active_term < 1 or body.active_term > 16:
            raise HTTPException(status_code=400, detail="Active term must be between 1 and 16.")
        updates["active_term"] = body.active_term

    if body.avatar_url is not None:
        updates["avatar_url"] = body.avatar_url.strip() or None

    if body.bio is not None:
        updates["bio"] = body.bio.strip() or None

    if body.needs_profile_setup is not None:
        updates["needs_profile_setup"] = body.needs_profile_setup

    if not updates:
        raise HTTPException(status_code=400, detail="No profile updates provided.")

    now_utc = datetime.now(timezone.utc)
    updates["updated_at"] = now_utc.isoformat()

    if db is not None:
        db.users.update_one({"_id": user["_id"]}, {"$set": updates})
        updated_user = db.users.find_one({"_id": user["_id"]})
    else:
        try:
            updated_user = in_memory_store.update_user_profile(user_id, updates)
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))

    batch_info = extract_batch_info(updated_user["email"]) or {
        "batch_year": user.get("batch_year"),
        "year_of_study": user.get("year_of_study", 1),
        "max_allowed_term": user.get("max_allowed_term", 4),
    }
    return UserResponse(
        user_id=str(updated_user.get("_id", user_id)),
        email=updated_user["email"],
        display_name=updated_user.get("display_name", user.get("display_name", "")),
        username=updated_user.get("username", "student"),
        active_term=updated_user.get("active_term", 1),
        avatar_url=updated_user.get("avatar_url"),
        bio=updated_user.get("bio"),
        status=updated_user.get("status", "active"),
        role=updated_user.get("role", user.get("role", "student")),
        batch_year=batch_info["batch_year"],
        year_of_study=batch_info["year_of_study"],
        max_allowed_term=batch_info["max_allowed_term"],
        is_special=updated_user.get("is_special", is_special_email(updated_user["email"])),
        needs_profile_setup=updated_user.get("needs_profile_setup", False)
    )


@router.delete("/api/users/me", status_code=204)
async def delete_me(request: Request, response: Response, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    user_id = user["user_id"]
    db = get_db_or_fail()
    if db is not None:
        db.bookmarks.delete_many({"user_id": user_id})
        db.sessions.delete_many({"user_id": user_id})
        db.users.delete_one({"_id": user["_id"]})
    else:
        in_memory_store.delete_user(user_id)

    csrf_header = request.headers.get("x-csrf-token", "").strip()
    if csrf_header:
        invalidate_csrf_token(csrf_header)

    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return None


# ==============================================================================
# Bookmark Endpoints
# ==============================================================================

@router.get("/api/bookmarks", response_model=BookmarkListResponse)
async def list_bookmarks(user: dict = Depends(get_current_student)):
    user_id = user["user_id"]
    db = get_db_or_fail()
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


@router.put("/api/bookmarks/{note_id}", response_model=BookmarkActionResponse)
async def add_bookmark(note_id: str, request: Request, response: Response, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    note_id = note_id.lower().strip()

    user_id = user["user_id"]
    db = get_db_or_fail()

    # Validate note_id against database or InMemoryStore
    note_exists = False
    if db is not None:
        note_exists = db.notes.count_documents({"note_id": note_id}) > 0
    else:
        note_exists = in_memory_store.get_note(note_id) is not None

    if not note_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note '{note_id}' does not exist in the course catalogue."
        )

    now_str = datetime.now(timezone.utc).isoformat()

    if db is not None:
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


@router.delete("/api/bookmarks/{note_id}", status_code=204)
async def delete_bookmark(note_id: str, request: Request, user: dict = Depends(get_current_student)):
    validate_csrf(request)
    note_id = note_id.lower().strip()
    user_id = user["user_id"]
    db = get_db_or_fail()
    if db is not None:
        db.bookmarks.delete_one({"user_id": user_id, "note_id": note_id})
    else:
        in_memory_store.remove_bookmark(user_id, note_id)
    return Response(status_code=204)


@router.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "sst-study-platform-api",
        "version": "1.1"
    }

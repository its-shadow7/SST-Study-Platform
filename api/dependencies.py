import logging
from fastapi import Request, HTTPException, status
from api.auth import decode_access_jwt, is_dev_mock_login_allowed
from api.database import get_mongo_db, in_memory_store
from api.config import settings

logger = logging.getLogger("api.dependencies")

def get_db_or_fail():
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
            raise HTTPException(
                status_code=503,
                detail="Database unavailable. Please try again shortly."
            )
        logger.warning("MongoDB Atlas unavailable; falling back to in-memory store for development.")
    return db

async def get_current_student(request: Request) -> dict:
    """
    Authenticates student from access_token cookie or Bearer authorization header.
    Returns active user document with user_id mapped to stringified _id.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
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

    db = get_db_or_fail()
    if db is not None:
        user = db.users.find_one({"google_sub_id": sub})
        if not user or user.get("status") != "active":
            raise HTTPException(status_code=401, detail="User account is inactive or not found.")
        user["user_id"] = str(user["_id"])
        user["role"] = user.get("role", "student")
        return user
    else:
        user = in_memory_store.get_user_by_sub(sub)
        if not user or user.get("status") != "active":
            raise HTTPException(status_code=401, detail="User account is inactive or not found.")
        user["user_id"] = user["_id"]
        user["role"] = user.get("role", "student")
        return user


def require_roles(allowed_roles: list[str]):
    """
    RBAC dependency factory that validates the authenticated user possesses
    one of the allowed roles. Users with 'admin' role always bypass role restrictions.
    Raises 403 Forbidden if unauthorized.
    """
    async def role_checker(request: Request) -> dict:
        user = await get_current_student(request)
        user_role = user.get("role", "student")
        if user_role == "admin" or user_role in allowed_roles:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Insufficient permissions."
        )
    return role_checker

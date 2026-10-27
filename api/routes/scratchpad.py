import logging
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pymongo import ReturnDocument

from api.core.config import settings
from api.core.database import in_memory_store
from api.core.dependencies import get_current_student, get_db_or_fail
from api.core.rate_limiter import check_in_memory_rate_limit, check_upstash_rate_limit
from api.schemas.scratchpad import (
    PrivateNoteDocument,
    ScratchpadResponse,
    ScratchpadSummaryResponse,
    UpdateScratchpadRequest,
)

logger = logging.getLogger("api.routes.scratchpad")

router = APIRouter(tags=["scratchpad"])


def check_scratchpad_rate_limit(user_id: str) -> None:
    """
    Enforces auto-save rate limit: maximum 30 requests per minute per user_id.
    Uses Upstash Redis in production, falling back to local memory in dev.
    Raises 429 Too Many Requests if the limit is exceeded.
    """
    limiter_key = f"rate_limit:scratchpad:{user_id}"
    max_requests = 30
    window_seconds = 60

    allowed = True
    is_prod = (
        getattr(settings, "ENVIRONMENT", "").lower() == "production"
        or os.getenv("VERCEL_ENV", "").lower() == "production"
    )

    if settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN:
        try:
            allowed = check_upstash_rate_limit(limiter_key, max_requests, window_seconds)
        except HTTPException:
            if not is_prod:
                allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)
            else:
                raise
    else:
        if is_prod:
            logger.critical(
                "Production requires UPSTASH_REDIS configuration for distributed rate limiting. Enforcing fail-closed 503."
            )
            raise HTTPException(
                status_code=503,
                detail="Rate limit service temporarily unavailable. Please try again shortly."
            )
        allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too Many Requests: Maximum {max_requests} scratchpad saves per minute allowed.",
        )


@router.get("/api/scratchpads/summary", response_model=ScratchpadSummaryResponse)
async def get_scratchpad_summary(user: dict = Depends(get_current_student)):
    """
    Returns note_ids for which the authenticated user has non-empty scratchpad notes.
    Used by the Left Island navigation to display personal note indicators.
    """
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            cursor = db.scratchpads.find(
                {
                    "user_id": user_id,
                    "content": {"$nin": ["", None]}
                },
                {"note_id": 1, "_id": 0}
            )
            note_ids = [doc["note_id"] for doc in cursor if doc.get("note_id")]
            return ScratchpadSummaryResponse(note_ids=sorted(list(set(note_ids))))
        except Exception as e:
            logger.error(f"Error fetching scratchpad summary for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch scratchpad summary.")
    else:
        note_ids = [
            doc["note_id"]
            for doc in in_memory_store.scratchpads.values()
            if doc.get("user_id") == user_id and (doc.get("content") or "").strip() != ""
        ]
        return ScratchpadSummaryResponse(note_ids=sorted(list(set(note_ids))))


@router.get("/api/notes/{note_id}/scratchpad", response_model=ScratchpadResponse)
async def get_scratchpad(note_id: str, user: dict = Depends(get_current_student)):
    """
    Fetches the user's private scratchpad note for a specific note_id.
    If none exists, returns 200 with content: "" and updated_at: null.
    """
    clean_note_id = note_id.lower().strip()
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            doc = db.scratchpads.find_one({"user_id": user_id, "note_id": clean_note_id})
            if not doc:
                return ScratchpadResponse(
                    id=None,
                    user_id=user_id,
                    note_id=clean_note_id,
                    content="",
                    updated_at=None
                )
            return ScratchpadResponse(
                id=str(doc["_id"]),
                user_id=doc.get("user_id", user_id),
                note_id=doc.get("note_id", clean_note_id),
                content=doc.get("content", ""),
                updated_at=doc.get("updated_at")
            )
        except Exception as e:
            logger.error(f"Error fetching scratchpad for user {user_id}, note {clean_note_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch scratchpad.")
    else:
        key = f"{user_id}:{clean_note_id}"
        doc = in_memory_store.scratchpads.get(key)
        if not doc:
            return ScratchpadResponse(
                id=None,
                user_id=user_id,
                note_id=clean_note_id,
                content="",
                updated_at=None
            )
        return ScratchpadResponse(
            id=doc.get("id"),
            user_id=doc.get("user_id", user_id),
            note_id=doc.get("note_id", clean_note_id),
            content=doc.get("content", ""),
            updated_at=doc.get("updated_at")
        )


@router.put("/api/notes/{note_id}/scratchpad", response_model=ScratchpadResponse)
async def save_scratchpad(
    note_id: str,
    body: UpdateScratchpadRequest,
    user: dict = Depends(get_current_student)
):
    """
    Performs an atomic upsert of the student's personal scratchpad for note_id.
    Enforces a rate limit of 30 saves per minute per student.
    """
    clean_note_id = note_id.lower().strip()
    user_id = user["user_id"]

    # Enforce 30 requests/minute rate limit to prevent spam
    check_scratchpad_rate_limit(user_id)

    now_dt = datetime.now(timezone.utc)
    db = get_db_or_fail()

    if db is not None:
        try:
            # Atomic MongoDB update with upsert=True
            res = db.scratchpads.find_one_and_update(
                {"user_id": user_id, "note_id": clean_note_id},
                {
                    "$set": {
                        "content": body.content,
                        "updated_at": now_dt
                    },
                    "$setOnInsert": {
                        "user_id": user_id,
                        "note_id": clean_note_id,
                        "created_at": now_dt
                    }
                },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            return ScratchpadResponse(
                id=str(res["_id"]),
                user_id=res["user_id"],
                note_id=res["note_id"],
                content=res.get("content", ""),
                updated_at=res.get("updated_at")
            )
        except Exception as e:
            logger.error(f"Error saving scratchpad for user {user_id}, note {clean_note_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to save scratchpad.")
    else:
        key = f"{user_id}:{clean_note_id}"
        existing = in_memory_store.scratchpads.get(key)
        doc_id = existing.get("id") if existing else f"sp_{uuid.uuid4().hex[:12]}"
        doc = {
            "id": doc_id,
            "user_id": user_id,
            "note_id": clean_note_id,
            "content": body.content,
            "updated_at": now_dt,
            "created_at": existing.get("created_at", now_dt) if existing else now_dt
        }
        in_memory_store.scratchpads[key] = doc
        return ScratchpadResponse(
            id=doc["id"],
            user_id=doc["user_id"],
            note_id=doc["note_id"],
            content=doc["content"],
            updated_at=doc["updated_at"]
        )

import logging
import os
import re
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from bson import ObjectId
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from pymongo import ReturnDocument

from api.core.security import validate_csrf
from api.core.config import settings
from api.core.database import in_memory_store
from api.core.dependencies import get_current_student, get_db_or_fail
from api.schemas.comment import (
    CommentDocument,
    CommentListResponse,
    CreateCommentRequest,
    DeleteCommentResponse,
    VoteCommentRequest,
    VoteCommentResponse,
    ReportCommentRequest,
    ReportCommentResponse,
)
from api.routes.notifications import create_notification
from api.core.rate_limiter import check_in_memory_rate_limit, check_upstash_rate_limit

logger = logging.getLogger("api.routes.comments")

router = APIRouter(tags=["comments"])


def sanitize_comment_content(raw_text: str) -> str:
    """
    Sanitizes comment text to prevent stored XSS and HTML injection.
    Treats comments strictly as safe text / Markdown.
    Disallows raw HTML tags completely and strips dangerous link protocols (javascript:, data:, vbscript:).
    """
    if not raw_text:
        return ""
    # Strip null bytes
    cleaned = raw_text.replace("\x00", "")
    # Remove script, style, iframe, object, embed tags and their contents completely
    cleaned = re.sub(
        r"<\s*(?:script|style|iframe|object|embed)[^>]*>.*?<\s*/\s*(?:script|style|iframe|object|embed)\s*>",
        "",
        cleaned,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # Strip all remaining HTML tags (<...>) so comments cannot inject arbitrary HTML
    cleaned = re.sub(r"<[^>]*>", "", cleaned)
    # Strip dangerous URI schemes in markdown links or plain text
    cleaned = re.sub(r"(?i)\b(?:javascript|vbscript|data)\s*:", "", cleaned)
    return cleaned.strip()[:1000]


def check_comment_rate_limit(user_id: str) -> None:
    """
    Enforces rate limit: maximum 10 comments per minute per user_id.
    Uses Upstash Redis in production, falling back to local memory in dev.
    Raises 429 Too Many Requests if the limit is exceeded.
    """
    limiter_key = f"rate_limit:comment:{user_id}"
    max_requests = getattr(settings, "RATE_LIMIT_COMMENT_MAX", 10)
    window_seconds = getattr(settings, "RATE_LIMIT_COMMENT_WINDOW", 60)

    allowed = True
    is_prod = getattr(settings, "ENVIRONMENT", "").lower() == "production" or os.getenv("VERCEL_ENV", "").lower() == "production"

    upstash_fn = check_upstash_rate_limit
    try:
        import api.comments
        if hasattr(api.comments, "check_upstash_rate_limit"):
            upstash_fn = api.comments.check_upstash_rate_limit
    except Exception:
        pass

    if settings.UPSTASH_REDIS_REST_URL and settings.UPSTASH_REDIS_REST_TOKEN:
        try:
            allowed = upstash_fn(limiter_key, max_requests, window_seconds)
        except HTTPException:
            if not is_prod:
                allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)
            else:
                raise
    else:
        if is_prod:
            logger.critical("Production requires UPSTASH_REDIS configuration for distributed comment rate limiting. Enforcing fail-closed 503.")
            raise HTTPException(
                status_code=503,
                detail="Rate limit service temporarily unavailable. Please try again shortly."
            )
        allowed = check_in_memory_rate_limit(limiter_key, max_requests, window_seconds)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too Many Requests: Maximum {max_requests} comments per minute allowed.",
        )


def check_spam_heuristics(text: str) -> List[str]:
    """
    Evaluates comment text against rule-based spam, scam, and character-flood patterns.
    """
    reasons = []
    lower = text.lower()

    # 1. Repetitive character flood
    if re.search(r'(.)\1{7,}', text):
        reasons.append("spam/character-flood")

    # 2. Known scam / spam promotional patterns
    spam_patterns = [
        r'\b(free\s+robux|free\s+crypto|free\s+bitcoin|buy\s+crypto|airdrop)\b',
        r'\b(t\.me\/|telegram\.me\/|wa\.me\/|whatsapp\.com\/channel\/)',
        r'\b(casino|betting|slots|win\s+real\s+money|prize\s+money)\b',
        r'\b(viagra|cialis|enhancement\s+pills)\b',
        r'\b(click\s+here\s+to\s+claim|claim\s+your\s+reward|earn\s+\$\d+)\b',
    ]
    for pattern in spam_patterns:
        if re.search(pattern, lower):
            reasons.append("spam/promotional")
            break

    # 3. Excessive URL flooding or suspicious scam links
    urls = re.findall(r'https?://\S+|www\.\S+', lower)
    if len(urls) >= 3 or (len(urls) >= 1 and any(bad in url for url in urls for bad in ['crypto', 'airdrop', 'claim', 'free', 'bonus', 'gift', 'freemoney', 't.me'])):
        reasons.append("spam/suspicious-links")

    return reasons


async def check_content_safety(text: str) -> List[str]:
    """
    Validates comment text against:
    1. Built-in proactive spam and link abuse heuristics.
    2. OpenAI Moderation API for harassment, hate, self-harm, sexual, violence.
    Returns a list of flagged category names if flagged.
    """
    if not text:
        return []

    flagged_reasons = []

    # 1. Proactive rule-based spam check
    spam_flags = check_spam_heuristics(text)
    flagged_reasons.extend(spam_flags)

    # 2. OpenAI Moderation API
    api_key = getattr(settings, "OPENAI_API_KEY", "").strip()
    if not api_key:
        logger.warning("OPENAI_API_KEY is not set. OpenAI Moderation API call skipped.")
        return flagged_reasons

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            resp = await client.post(
                "https://api.openai.com/v1/moderations",
                headers=headers,
                json={"input": text},
            )
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    categories = results[0].get("categories", {})
                    flagged_categories = [cat for cat, flagged in categories.items() if flagged is True]
                    flagged_reasons.extend(flagged_categories)
            else:
                logger.error(f"OpenAI Moderation API returned {resp.status_code}: {resp.text}")
    except Exception as exc:
        logger.error(f"Moderation API request failed: {exc}")

    return list(dict.fromkeys(flagged_reasons))


# Alias for backward compatibility
check_openai_moderation = check_content_safety


@router.get("/api/notes/{note_id}/comments", response_model=CommentListResponse)
async def get_comments_for_note(
    note_id: str,
    sort: str = Query("top", pattern="^(newest|top)$"),
    user: dict = Depends(get_current_student),
):
    clean_note_id = note_id.strip()
    db = get_db_or_fail()

    sort_stage = (
        {"$sort": {"score": -1, "created_at": -1}}
        if sort == "top"
        else {"$sort": {"created_at": -1}}
    )

    if db is not None:
        pipeline = [
            {
                "$match": {
                    "note_id": clean_note_id,
                    "$or": [
                        {"status": {"$in": ["published", "reported"]}},
                        {"status": {"$exists": False}}
                    ]
                }
            },
            sort_stage,
            {
                "$lookup": {
                    "from": "users",
                    "let": {"c_user_id": "$user_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$or": [
                                        {"$eq": [{"$toString": "$_id"}, "$$c_user_id"]},
                                        {"$eq": ["$_id", "$$c_user_id"]},
                                    ]
                                }
                            }
                        },
                        {"$project": {"_id": 0, "username": 1, "avatar_url": 1, "role": 1}},
                    ],
                    "as": "author",
                }
            },
            {
                "$unwind": {
                    "path": "$author",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": {"$toString": "$_id"},
                    "note_id": 1,
                    "user_id": 1,
                    "content": 1,
                    "parent_id": 1,
                    "score": {"$ifNull": ["$score", 0]},
                    "upvoted_by": {"$ifNull": ["$upvoted_by", []]},
                    "downvoted_by": {"$ifNull": ["$downvoted_by", []]},
                    "status": {"$ifNull": ["$status", "published"]},
                    "moderation_reasons": {"$ifNull": ["$moderation_reasons", []]},
                    "reported_by": {"$ifNull": ["$reported_by", []]},
                    "created_at": 1,
                    "updated_at": 1,
                    "username": "$author.username",
                    "avatar_url": "$author.avatar_url",
                    "author_role": {"$ifNull": ["$author.role", "student"]},
                }
            },
        ]
        raw_comments = list(db.comments.aggregate(pipeline))
        comments = [CommentDocument(**c) for c in raw_comments]
        return CommentListResponse(comments=comments, total=len(comments))
    else:
        raw_comments = in_memory_store.get_comments_for_note(clean_note_id, sort=sort)
        comments = [CommentDocument(**c) for c in raw_comments]
        return CommentListResponse(comments=comments, total=len(comments))


@router.post(
    "/api/notes/{note_id}/comments",
    response_model=CommentDocument,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    note_id: str,
    payload: CreateCommentRequest,
    request: Request,
    user: dict = Depends(get_current_student),
):
    validate_csrf(request)
    clean_note_id = note_id.strip()
    user_id = user["user_id"]

    check_comment_rate_limit(user_id)

    cleaned_content = sanitize_comment_content(payload.content)
    if not cleaned_content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Comment content cannot be empty after sanitization.",
        )

    flagged_reasons = await check_content_safety(cleaned_content)
    comment_status = "quarantined" if flagged_reasons else "published"

    clean_parent_id = payload.parent_id.strip() if payload.parent_id else None
    now_iso = datetime.now(timezone.utc).isoformat()
    db = get_db_or_fail()

    if db is not None:
        parent = None
        if clean_parent_id:
            try:
                p_oid = ObjectId(clean_parent_id)
                p_filter = {
                    "$or": [
                        {"_id": p_oid},
                        {"_id": clean_parent_id},
                        {"id": clean_parent_id},
                    ]
                }
            except Exception:
                p_filter = {
                    "$or": [
                        {"_id": clean_parent_id},
                        {"id": clean_parent_id},
                    ]
                }
            parent = db.comments.find_one(p_filter)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found.",
                )

        doc = {
            "note_id": clean_note_id,
            "user_id": user_id,
            "content": cleaned_content,
            "parent_id": clean_parent_id,
            "score": 0,
            "upvoted_by": [],
            "downvoted_by": [],
            "status": comment_status,
            "moderation_reasons": flagged_reasons,
            "reported_by": [],
            "report_history": [],
            "created_at": now_iso,
            "updated_at": now_iso,
        }
        res = db.comments.insert_one(doc)
        comment_id = str(res.inserted_id)

        if clean_parent_id and parent and parent.get("user_id") != user_id:
            create_notification(
                user_id=parent["user_id"],
                notif_type="reply",
                title="New Reply",
                message=f"@{user.get('username', 'Student')} replied to your comment on '{clean_note_id}'.",
                link=f"/read/{clean_note_id}?commentId={comment_id}#comment-{comment_id}",
                db=db,
            )
    else:
        parent = None
        if clean_parent_id:
            parent = in_memory_store.get_comment_by_id(clean_parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found.",
                )

        created = in_memory_store.add_comment(
            clean_note_id,
            user_id,
            cleaned_content,
            parent_id=clean_parent_id,
            status=comment_status,
            moderation_reasons=flagged_reasons,
            reported_by=[],
        )
        comment_id = created["id"]

        if clean_parent_id and parent and parent.get("user_id") != user_id:
            create_notification(
                user_id=parent["user_id"],
                notif_type="reply",
                title="New Reply",
                message=f"@{user.get('username', 'Student')} replied to your comment on '{clean_note_id}'.",
                link=f"/read/{clean_note_id}?commentId={comment_id}#comment-{comment_id}",
                db=None,
            )

    return CommentDocument(
        id=comment_id,
        note_id=clean_note_id,
        user_id=user_id,
        content=cleaned_content,
        parent_id=clean_parent_id,
        score=0,
        upvoted_by=[],
        downvoted_by=[],
        status=comment_status,
        moderation_reasons=flagged_reasons,
        reported_by=[],
        created_at=now_iso,
        updated_at=now_iso,
        username=user.get("username"),
        avatar_url=user.get("avatar_url"),
        author_role=user.get("role", "student"),
    )


@router.post("/api/comments/{comment_id}/vote", response_model=VoteCommentResponse)
async def vote_comment(
    comment_id: str,
    payload: VoteCommentRequest,
    request: Request,
    user: dict = Depends(get_current_student),
):
    validate_csrf(request)
    clean_id = comment_id.strip()
    user_id = user["user_id"]
    action = payload.action
    db = get_db_or_fail()

    if db is not None:
        try:
            oid = ObjectId(clean_id)
            id_filter = {"$or": [{"_id": oid}, {"_id": clean_id}]}
        except Exception:
            id_filter = {"_id": clean_id}

        if action == "upvote":
            doc = db.comments.find_one_and_update(
                {**id_filter, "upvoted_by": user_id},
                {"$pull": {"upvoted_by": user_id}, "$inc": {"score": -1}},
                return_document=ReturnDocument.AFTER,
            )
            if doc:
                user_vote = None
            else:
                doc = db.comments.find_one_and_update(
                    {**id_filter, "downvoted_by": user_id},
                    {
                        "$pull": {"downvoted_by": user_id},
                        "$addToSet": {"upvoted_by": user_id},
                        "$inc": {"score": 2},
                    },
                    return_document=ReturnDocument.AFTER,
                )
                if doc:
                    user_vote = "upvote"
                else:
                    doc = db.comments.find_one_and_update(
                        {
                            **id_filter,
                            "upvoted_by": {"$ne": user_id},
                            "downvoted_by": {"$ne": user_id},
                        },
                        {
                            "$addToSet": {"upvoted_by": user_id},
                            "$inc": {"score": 1},
                        },
                        return_document=ReturnDocument.AFTER,
                    )
                    if doc:
                        user_vote = "upvote"
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment '{clean_id}' not found.",
                        )
        else:  # downvote
            doc = db.comments.find_one_and_update(
                {**id_filter, "downvoted_by": user_id},
                {"$pull": {"downvoted_by": user_id}, "$inc": {"score": 1}},
                return_document=ReturnDocument.AFTER,
            )
            if doc:
                user_vote = None
            else:
                doc = db.comments.find_one_and_update(
                    {**id_filter, "upvoted_by": user_id},
                    {
                        "$pull": {"upvoted_by": user_id},
                        "$addToSet": {"downvoted_by": user_id},
                        "$inc": {"score": -2},
                    },
                    return_document=ReturnDocument.AFTER,
                )
                if doc:
                    user_vote = "downvote"
                else:
                    doc = db.comments.find_one_and_update(
                        {
                            **id_filter,
                            "upvoted_by": {"$ne": user_id},
                            "downvoted_by": {"$ne": user_id},
                        },
                        {
                            "$addToSet": {"downvoted_by": user_id},
                            "$inc": {"score": -1},
                        },
                        return_document=ReturnDocument.AFTER,
                    )
                    if doc:
                        user_vote = "downvote"
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment '{clean_id}' not found.",
                        )

        final_score = doc.get("score", 0)
        return VoteCommentResponse(id=clean_id, score=final_score, user_vote=user_vote)
    else:
        res = in_memory_store.vote_comment(clean_id, user_id, action)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )
        user_vote, final_score = res
        return VoteCommentResponse(id=clean_id, score=final_score, user_vote=user_vote)


@router.delete("/api/comments/{comment_id}", response_model=DeleteCommentResponse)
async def delete_comment(
    comment_id: str,
    request: Request,
    user: dict = Depends(get_current_student),
):
    validate_csrf(request)
    clean_id = comment_id.strip()
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            oid = ObjectId(clean_id)
            query = {"$or": [{"_id": oid}, {"_id": clean_id}]}
        except Exception:
            query = {"_id": clean_id}

        target = db.comments.find_one(query)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )

        if str(target.get("user_id")) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only delete your own comments.",
            )

        has_children = db.comments.count_documents({"parent_id": clean_id}) > 0
        if has_children:
            now_iso = datetime.now(timezone.utc).isoformat()
            db.comments.update_one(
                query,
                {"$set": {"content": "[Deleted]", "updated_at": now_iso}},
            )
            return DeleteCommentResponse(status="redacted", id=clean_id)
        else:
            db.comments.delete_one(query)
            return DeleteCommentResponse(status="deleted", id=clean_id)
    else:
        target = in_memory_store.get_comment_by_id(clean_id)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )

        try:
            del_status = in_memory_store.delete_comment(clean_id, user_id)
        except PermissionError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: You can only delete your own comments.",
            )

        return DeleteCommentResponse(status=del_status, id=clean_id)


@router.post("/api/comments/{comment_id}/report", response_model=ReportCommentResponse)
async def report_comment(
    comment_id: str,
    payload: ReportCommentRequest,
    request: Request,
    user: dict = Depends(get_current_student),
):
    validate_csrf(request)
    clean_id = comment_id.strip()
    user_id = user["user_id"]
    reason = payload.reason.strip()

    if not reason:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Report reason cannot be empty.",
        )

    db = get_db_or_fail()
    now_utc = datetime.now(timezone.utc)
    now_iso = now_utc.isoformat()
    window_threshold = now_utc - timedelta(hours=settings.AUTO_QUARANTINE_WINDOW_HOURS)

    if db is not None:
        try:
            oid = ObjectId(clean_id)
            query = {"$or": [{"_id": oid}, {"_id": clean_id}]}
        except Exception:
            query = {"_id": clean_id}

        target = db.comments.find_one(query)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )

        reported_by = list(target.get("reported_by", []))
        report_history = list(target.get("report_history", []))

        if user_id not in reported_by:
            reported_by.append(user_id)
            new_report_entry = {
                "user_id": user_id,
                "reason": reason,
                "reported_at": now_iso,
            }
            report_history.append(new_report_entry)

            recent_unique_reporters = set()
            for r in report_history:
                reported_at_str = r.get("reported_at")
                rep_user = r.get("user_id")
                if not reported_at_str or not rep_user:
                    continue
                try:
                    rep_time = datetime.fromisoformat(reported_at_str)
                    if rep_time.tzinfo is None:
                        rep_time = rep_time.replace(tzinfo=timezone.utc)
                    if rep_time >= window_threshold:
                        recent_unique_reporters.add(rep_user)
                except Exception:
                    pass

            is_quarantined = len(recent_unique_reporters) >= settings.AUTO_QUARANTINE_REPORT_THRESHOLD

            update_ops: dict = {
                "$addToSet": {"reported_by": user_id, "moderation_reasons": reason},
                "$push": {"report_history": new_report_entry},
                "$set": {"updated_at": now_iso},
            }

            if is_quarantined:
                update_ops["$set"]["status"] = "quarantined"
                quarantine_reason = (
                    f"auto_quarantine: {len(recent_unique_reporters)} distinct reports "
                    f"within {settings.AUTO_QUARANTINE_WINDOW_HOURS}h"
                )
                update_ops["$addToSet"]["moderation_reasons"] = quarantine_reason

                try:
                    db.moderation_logs.insert_one({
                        "action": "auto_quarantined",
                        "comment_id": clean_id,
                        "note_id": target.get("note_id", "general"),
                        "comment_content": target.get("content", "")[:150],
                        "moderator_id": "system",
                        "moderator_name": "Automated Moderation",
                        "moderator_role": "admin",
                        "reason": quarantine_reason,
                        "created_at": now_iso,
                    })
                except Exception as log_err:
                    logger.warning("Could not record auto-quarantine audit log: %s", log_err)

                author_id = target.get("user_id")
                if author_id:
                    note_ref = target.get("note_id", "general")
                    create_notification(
                        user_id=author_id,
                        notif_type="comment_status",
                        title="Comment Quarantined",
                        message=f"Your comment on '{note_ref}' was automatically quarantined due to multiple community reports.",
                        link=f"/read/{note_ref}?commentId={clean_id}#comment-{clean_id}",
                        db=db,
                    )
            elif target.get("status", "published") == "published":
                update_ops["$set"]["status"] = "reported"

            db.comments.update_one(query, update_ops)
            final_status = "quarantined" if is_quarantined else ("reported" if target.get("status", "published") == "published" else target.get("status"))
        else:
            final_status = target.get("status", "reported")

        return ReportCommentResponse(
            message=(
                "Comment has been automatically quarantined due to community reports."
                if final_status == "quarantined"
                else "Comment has been reported for review."
            ),
            status=final_status,
            id=clean_id,
        )
    else:
        target = in_memory_store.get_comment_by_id(clean_id)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )

        updated = in_memory_store.report_comment(clean_id, user_id, reason)
        final_status = updated.get("status", "reported") if updated else "reported"
        return ReportCommentResponse(
            message=(
                "Comment has been automatically quarantined due to community reports."
                if final_status == "quarantined"
                else "Comment has been reported for review."
            ),
            status=final_status,
            id=clean_id,
        )

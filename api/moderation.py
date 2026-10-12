import logging
from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.auth import validate_csrf
from api.database import in_memory_store
from api.dependencies import get_db_or_fail, require_roles
from api.notifications import create_notification
from models.comment import (
    CommentDocument,
    ModerationQueueResponse,
    ResolveModerationRequest,
    ResolveModerationResponse,
    ModerationAuditLogItem,
    ModerationAuditLogResponse,
)

logger = logging.getLogger("api.moderation")

router = APIRouter(prefix="/api/moderation", tags=["moderation"])


@router.get("/queue", response_model=ModerationQueueResponse)
async def get_moderation_queue(
    user: dict = Depends(require_roles(["moderator", "admin"])),
):
    """
    Retrieves all comments awaiting moderation (quarantined by AI or reported by students).
    Requires moderator or admin role.
    Joins author details (username, avatar_url, role) from users collection.
    """
    db = get_db_or_fail()

    if db is not None:
        pipeline = [
            {
                "$match": {
                    "status": {"$in": ["quarantined", "reported"]},
                }
            },
            {"$sort": {"updated_at": -1, "created_at": -1}},
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
                    "status": 1,
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
        raw_items = list(db.comments.aggregate(pipeline))
        comments = [CommentDocument(**item) for item in raw_items]
        return ModerationQueueResponse(queue=comments, total=len(comments))
    else:
        raw_items = in_memory_store.get_moderation_queue()
        comments = [CommentDocument(**item) for item in raw_items]
        return ModerationQueueResponse(queue=comments, total=len(comments))


@router.post("/queue/{comment_id}/resolve", response_model=ResolveModerationResponse)
async def resolve_moderation_item(
    comment_id: str,
    payload: ResolveModerationRequest,
    request: Request,
    user: dict = Depends(require_roles(["moderator", "admin"])),
):
    """
    Resolves a moderated comment.
    Action 'approve' sets status to 'published'.
    Action 'delete' sets status to 'deleted' and redacts content.
    Requires moderator or admin role and valid CSRF token.
    """
    validate_csrf(request)
    clean_id = comment_id.strip()
    action = payload.action
    now_iso = datetime.now(timezone.utc).isoformat()
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

        if action == "approve":
            new_status = "published"
            db.comments.update_one(
                query,
                {"$set": {"status": new_status, "updated_at": now_iso}},
            )
        elif action == "delete":
            new_status = "deleted"
            db.comments.update_one(
                query,
                {
                    "$set": {
                        "status": new_status,
                        "content": "[Deleted]",
                        "updated_at": now_iso,
                    }
                },
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid moderation action '{action}'.",
            )

        # 1. Record Audit Log in MongoDB
        mod_id = user["user_id"]
        mod_name = user.get("display_name") or user.get("username", "Moderator")
        mod_role = user.get("role", "moderator")
        note_id = target.get("note_id", "general")
        content_snippet = target.get("content", "")[:150]

        log_doc = {
            "action": f"{action}d",
            "comment_id": clean_id,
            "note_id": note_id,
            "comment_content": content_snippet,
            "moderator_id": mod_id,
            "moderator_name": mod_name,
            "moderator_role": mod_role,
            "reason": f"Manually resolved as {action}d by {mod_role}",
            "created_at": now_iso,
        }
        try:
            db.moderation_logs.insert_one(log_doc)
        except Exception as e:
            logger.warning("Failed to write moderation log to MongoDB: %s", e)

        # 2. Dispatch Notifications
        author_id = target.get("user_id")
        if author_id and author_id != mod_id:
            if action == "approve":
                create_notification(
                    user_id=author_id,
                    notif_type="comment_status",
                    title="Comment Approved",
                    message=f"Your comment on '{note_id}' has been approved by the moderation team.",
                    link=f"/read/{note_id}?commentId={clean_id}#comment-{clean_id}",
                    db=db,
                )
            else:
                create_notification(
                    user_id=author_id,
                    notif_type="comment_status",
                    title="Comment Removed",
                    message=f"Your comment on '{note_id}' was removed for violating community guidelines.",
                    link=f"/read/{note_id}#comments",
                    db=db,
                )

        # Notify students who reported this comment
        for rep_id in target.get("reported_by", []):
            if rep_id != mod_id and rep_id != author_id:
                create_notification(
                    user_id=rep_id,
                    notif_type="report_resolved",
                    title="Report Resolved",
                    message=f"A comment you reported on '{note_id}' has been reviewed and resolved.",
                    link=f"/read/{note_id}?commentId={clean_id}#comment-{clean_id}",
                    db=db,
                )

        logger.info(
            "Moderation item resolved: comment_id=%s, action=%s, moderator=%s",
            clean_id,
            action,
            mod_id,
        )
        return ResolveModerationResponse(
            message=f"Comment {action}d successfully.",
            status=new_status,
            id=clean_id,
        )
    else:
        target = in_memory_store.get_comment_by_id(clean_id)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{clean_id}' not found.",
            )

        res = in_memory_store.resolve_moderation(clean_id, action)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not resolve comment '{clean_id}'.",
            )

        new_status = "published" if action == "approve" else "deleted"
        mod_id = user["user_id"]
        mod_name = user.get("display_name") or user.get("username", "Moderator")
        mod_role = user.get("role", "moderator")
        note_id = target.get("note_id", "general")

        in_memory_store.add_audit_log(
            action=f"{action}d",
            comment_id=clean_id,
            moderator_id=mod_id,
            moderator_name=mod_name,
            moderator_role=mod_role,
            note_id=note_id,
            comment_content=target.get("content", ""),
            reason=f"Manually resolved as {action}d by {mod_role}",
        )

        author_id = target.get("user_id")
        if author_id and author_id != mod_id:
            if action == "approve":
                in_memory_store.add_notification(
                    user_id=author_id,
                    notif_type="comment_status",
                    title="Comment Approved",
                    message=f"Your comment on '{note_id}' has been approved by the moderation team.",
                    link=f"/read/{note_id}?commentId={clean_id}#comment-{clean_id}",
                )
            else:
                in_memory_store.add_notification(
                    user_id=author_id,
                    notif_type="comment_status",
                    title="Comment Removed",
                    message=f"Your comment on '{note_id}' was removed for violating community guidelines.",
                    link=f"/read/{note_id}#comments",
                )

        for rep_id in target.get("reported_by", []):
            if rep_id != mod_id and rep_id != author_id:
                in_memory_store.add_notification(
                    user_id=rep_id,
                    notif_type="report_resolved",
                    title="Report Resolved",
                    message=f"A comment you reported on '{note_id}' has been reviewed and resolved.",
                    link=f"/read/{note_id}?commentId={clean_id}#comment-{clean_id}",
                )

        return ResolveModerationResponse(
            message=f"Comment {action}d successfully.",
            status=new_status,
            id=clean_id,
        )


@router.get("/audit-log", response_model=ModerationAuditLogResponse)
async def get_moderation_audit_log(
    user: dict = Depends(require_roles(["moderator", "admin"])),
):
    """
    Retrieves chronological moderation audit logs for tracking moderator decisions.
    Requires moderator or admin role.
    """
    db = get_db_or_fail()
    if db is not None:
        try:
            cursor = db.moderation_logs.find().sort("created_at", -1).limit(50)
            logs = []
            for doc in cursor:
                doc["id"] = str(doc.get("_id") or doc.get("id"))
                doc.pop("_id", None)
                logs.append(ModerationAuditLogItem(**doc))
            return ModerationAuditLogResponse(logs=logs, total=len(logs))
        except Exception as e:
            logger.error("Failed to fetch moderation logs from MongoDB: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve moderation audit logs.",
            )
    else:
        raw_logs = in_memory_store.get_audit_logs(limit=50)
        logs = [ModerationAuditLogItem(**l) for l in raw_logs]
        return ModerationAuditLogResponse(logs=logs, total=len(logs))


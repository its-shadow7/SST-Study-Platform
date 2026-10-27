import logging
from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.core.security import validate_csrf
from api.core.database import in_memory_store
from api.core.dependencies import get_current_student, get_db_or_fail
from api.schemas.comment import NotificationItem, NotificationListResponse

logger = logging.getLogger("api.routes.notifications")

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def create_notification(
    user_id: str,
    notif_type: str,
    title: str,
    message: str,
    link: str = None,
    db=None,
) -> None:
    """Helper to dispatch a notification to MongoDB or InMemoryStore."""
    now_iso = datetime.now(timezone.utc).isoformat()
    if db is not None:
        try:
            doc = {
                "user_id": user_id,
                "type": notif_type,
                "title": title,
                "message": message,
                "link": link,
                "read": False,
                "created_at": now_iso,
            }
            db.notifications.insert_one(doc)
        except Exception as e:
            logger.warning("Failed to save notification: %s", e)
    else:
        in_memory_store.add_notification(user_id, notif_type, title, message, link)


@router.get("", response_model=NotificationListResponse)
async def get_user_notifications(
    user: dict = Depends(get_current_student),
):
    """
    Retrieves the latest 20 notifications for the authenticated student,
    along with their current unread count.
    """
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            cursor = (
                db.notifications.find({"user_id": user_id})
                .sort("created_at", -1)
                .limit(20)
            )
            items = []
            for doc in cursor:
                doc["id"] = str(doc.get("_id") or doc.get("id"))
                doc.pop("_id", None)
                items.append(NotificationItem(**doc))

            unread_count = db.notifications.count_documents(
                {"user_id": user_id, "read": False}
            )
            return NotificationListResponse(
                notifications=items, unread_count=unread_count
            )
        except Exception as e:
            logger.error("Failed to load notifications from MongoDB: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to load notifications.",
            )
    else:
        raw_items = in_memory_store.get_notifications(user_id)
        unread_count = in_memory_store.get_unread_notification_count(user_id)
        notifications = [NotificationItem(**n) for n in raw_items]
        return NotificationListResponse(
            notifications=notifications, unread_count=unread_count
        )


@router.patch("/{notif_id}/read")
async def mark_notification_as_read(
    notif_id: str,
    request: Request,
    user: dict = Depends(get_current_student),
):
    """
    Marks a single notification as read.
    """
    validate_csrf(request)
    clean_id = notif_id.strip()
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            try:
                oid = ObjectId(clean_id)
                query = {"$or": [{"_id": oid}, {"_id": clean_id}], "user_id": user_id}
            except Exception:
                query = {"_id": clean_id, "user_id": user_id}

            res = db.notifications.update_one(query, {"$set": {"read": True}})
            if res.matched_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Notification not found.",
                )
            return {"success": True, "id": clean_id}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to update notification: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update notification.",
            )
    else:
        success = in_memory_store.mark_notification_read(clean_id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )
        return {"success": True, "id": clean_id}


@router.post("/mark-all-read")
async def mark_all_notifications_read(
    request: Request,
    user: dict = Depends(get_current_student),
):
    """
    Marks all notifications for the current student as read.
    """
    validate_csrf(request)
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        try:
            res = db.notifications.update_many(
                {"user_id": user_id, "read": False},
                {"$set": {"read": True}},
            )
            return {"success": True, "marked_count": res.modified_count}
        except Exception as e:
            logger.error("Failed to mark all notifications read: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update notifications.",
            )
    else:
        count = in_memory_store.mark_all_notifications_read(user_id)
        return {"success": True, "marked_count": count}

import logging
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from api.core.dependencies import get_current_student, require_moderator, get_db_or_fail
from api.core.security import validate_csrf, extract_batch_info, is_special_email
from api.core.database import in_memory_store
from api.schemas.note import NoteDocument, NoteIndexItem, NoteUpsertRequest, extract_term_number

logger = logging.getLogger("api.routes.notes")

router = APIRouter(prefix="/api/notes", tags=["Notes"])


def _get_user_max_allowed_term(user: dict) -> int:
    """Calculates max allowed curriculum term for user, with moderator/admin full bypass."""
    role = user.get("role", "student")
    if role in ("moderator", "admin"):
        return 16

    email = user.get("email", "")
    if is_special_email(email):
        return 16

    batch_info = extract_batch_info(email)
    if batch_info and "max_allowed_term" in batch_info:
        return batch_info["max_allowed_term"]
    return 4


@router.get("", response_model=List[NoteIndexItem])
async def list_notes(
    include_drafts: bool = Query(False, description="Include draft notes (moderator/admin only)"),
    user: dict = Depends(get_current_student),
):
    """
    Returns catalogue index of available course notes filtered by student's active term eligibility.
    Lightweight projection excludes heavy sections and quiz fields.
    """
    db = get_db_or_fail()
    is_elevated = user.get("role") in ("moderator", "admin")
    can_include_drafts = include_drafts and is_elevated
    max_term = _get_user_max_allowed_term(user)

    if db is not None:
        query = {}
        if not can_include_drafts:
            query["approval_status"] = "approved"

        if not is_elevated:
            query["term_number"] = {"$lte": max_term}

        # Projection: exclude _id, sections, quiz
        cursor = db.notes.find(
            query,
            {"_id": 0, "sections": 0, "quiz": 0}
        ).sort([("term_number", 1), ("subject_code", 1), ("note_id", 1)])

        notes_list = []
        for doc in cursor:
            if "term_number" not in doc or not doc["term_number"]:
                doc["term_number"] = extract_term_number(doc.get("term", ""))
            notes_list.append(NoteIndexItem(**doc))

        # Include any in-memory store notes
        seen_ids = {n.note_id for n in notes_list}
        for item in in_memory_store.list_notes(
            max_allowed_term=None if is_elevated else max_term,
            include_drafts=can_include_drafts
        ):
            if item["note_id"] not in seen_ids:
                notes_list.append(NoteIndexItem(**item))

        return notes_list
    else:
        # InMemoryStore path
        items = in_memory_store.list_notes(
            max_allowed_term=None if is_elevated else max_term,
            include_drafts=can_include_drafts
        )
        return [NoteIndexItem(**item) for item in items]


@router.get("/{note_id}", response_model=NoteDocument)
async def get_note_by_id(
    note_id: str,
    user: dict = Depends(get_current_student),
):
    """
    Fetches the complete lecture note by note_id.
    Enforces term gating and approval status restrictions.
    """
    db = get_db_or_fail()
    is_elevated = user.get("role") in ("moderator", "admin")
    max_term = _get_user_max_allowed_term(user)

    doc = None
    if db is not None:
        doc = db.notes.find_one({"note_id": note_id}, {"_id": 0})
    if not doc:
        doc = in_memory_store.get_note(note_id)

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lecture note '{note_id}' not found."
        )

    term_num = doc.get("term_number") or extract_term_number(doc.get("term", ""))
    approval_status = doc.get("approval_status", "approved")

    # Term access gating
    if not is_elevated and term_num > max_term:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Term {term_num} notes are beyond your current academic year (up to Term {max_term})."
        )

    # Draft gating
    if not is_elevated and approval_status != "approved":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Lecture note '{note_id}' is currently unpublished."
        )

    doc["term_number"] = term_num
    return NoteDocument(**doc)


@router.post("", response_model=NoteDocument, status_code=status.HTTP_201_CREATED)
async def create_note(
    request: Request,
    body: NoteUpsertRequest,
    user: dict = Depends(require_moderator),
):
    """
    Creates a new course lecture note directly in the database.
    Requires moderator or admin privileges and valid CSRF token.
    """
    validate_csrf(request)
    db = get_db_or_fail()

    note_data = body.model_dump()
    now_iso = datetime.now(timezone.utc).isoformat()
    note_data["last_updated"] = now_iso
    note_data["schema_version"] = 1

    note_id = note_data["note_id"]

    # Check for existing note with identical note_id
    if db is not None:
        existing = db.notes.find_one({"note_id": note_id})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Note with note_id '{note_id}' already exists. Use PUT to update."
            )
        db.notes.insert_one(note_data)
        # Log to audit trail
        db.moderation_audit_logs.insert_one({
            "action": "created_note",
            "note_id": note_id,
            "moderator_id": user["user_id"],
            "moderator_name": user.get("display_name", "Moderator"),
            "moderator_role": user.get("role", "moderator"),
            "comment_content": f"Created note '{body.topic_title}'",
            "created_at": now_iso
        })
    else:
        if in_memory_store.get_note(note_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Note with note_id '{note_id}' already exists. Use PUT to update."
            )

    in_memory_store.save_note(note_data)
    in_memory_store.add_audit_log(
        action="created_note",
        comment_id=f"note_{note_id}",
        moderator_id=user["user_id"],
        moderator_name=user.get("display_name", "Moderator"),
        moderator_role=user.get("role", "moderator"),
        note_id=note_id,
        comment_content=f"Created note '{body.topic_title}'"
    )

    # Clean out MongoDB internal _id if present
    note_data.pop("_id", None)
    return NoteDocument(**note_data)


@router.put("/{note_id}", response_model=NoteDocument)
async def update_note(
    note_id: str,
    request: Request,
    body: NoteUpsertRequest,
    user: dict = Depends(require_moderator),
):
    """
    Updates or upserts an existing course lecture note.
    Requires moderator or admin privileges and valid CSRF token.
    """
    validate_csrf(request)
    db = get_db_or_fail()

    note_data = body.model_dump()
    note_data["note_id"] = note_id
    now_iso = datetime.now(timezone.utc).isoformat()
    note_data["last_updated"] = now_iso
    note_data["schema_version"] = 1

    if db is not None:
        db.notes.update_one(
            {"note_id": note_id},
            {"$set": note_data},
            upsert=True
        )
        # Log to audit trail
        db.moderation_audit_logs.insert_one({
            "action": "updated_note",
            "note_id": note_id,
            "moderator_id": user["user_id"],
            "moderator_name": user.get("display_name", "Moderator"),
            "moderator_role": user.get("role", "moderator"),
            "comment_content": f"Updated note '{body.topic_title}'",
            "created_at": now_iso
        })

    in_memory_store.save_note(note_data)
    in_memory_store.add_audit_log(
        action="updated_note",
        comment_id=f"note_{note_id}",
        moderator_id=user["user_id"],
        moderator_name=user.get("display_name", "Moderator"),
        moderator_role=user.get("role", "moderator"),
        note_id=note_id,
        comment_content=f"Updated note '{body.topic_title}'"
    )

    note_data.pop("_id", None)
    return NoteDocument(**note_data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    request: Request,
    user: dict = Depends(require_moderator),
):
    """
    Deletes a course lecture note from the database.
    Requires moderator or admin privileges and valid CSRF token.
    """
    validate_csrf(request)
    db = get_db_or_fail()
    now_iso = datetime.now(timezone.utc).isoformat()
    deleted = False

    if db is not None:
        res = db.notes.delete_one({"note_id": note_id})
        if res.deleted_count > 0:
            deleted = True
            db.moderation_audit_logs.insert_one({
                "action": "deleted_note",
                "note_id": note_id,
                "moderator_id": user["user_id"],
                "moderator_name": user.get("display_name", "Moderator"),
                "moderator_role": user.get("role", "moderator"),
                "comment_content": f"Deleted note '{note_id}'",
                "created_at": now_iso
            })

    if in_memory_store.get_note(note_id):
        in_memory_store.delete_note(note_id)
        deleted = True
        in_memory_store.add_audit_log(
            action="deleted_note",
            comment_id=f"note_{note_id}",
            moderator_id=user["user_id"],
            moderator_name=user.get("display_name", "Moderator"),
            moderator_role=user.get("role", "moderator"),
            note_id=note_id,
            comment_content=f"Deleted note '{note_id}'"
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note '{note_id}' not found."
        )

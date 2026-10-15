import logging
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from api.auth import validate_csrf
from api.database import in_memory_store
from api.dependencies import get_current_student, get_db_or_fail
from models.quiz import (
    SaveQuizAttemptRequest,
    QuizAttemptResponse,
    UserQuizStats,
)

logger = logging.getLogger("api.quizzes")

router = APIRouter(tags=["quizzes"])


def get_quiz_stats_for_user(user_id: str, db=None) -> dict:
    """Helper to compute aggregate quiz statistics for a student."""
    if db is not None:
        try:
            attempts = list(db.quiz_attempts.find({"user_id": user_id}))
            total_attempted = len(attempts)
            total_completed = sum(1 for a in attempts if a.get("is_completed"))
            total_questions = sum(a.get("total_questions", 0) for a in attempts)
            total_correct = sum(a.get("score", 0) for a in attempts)
            accuracy = round((total_correct / total_questions) * 100) if total_questions > 0 else 0
            return {
                "quizzes_attempted": total_attempted,
                "quizzes_completed": total_completed,
                "total_questions_answered": total_questions,
                "total_correct": total_correct,
                "accuracy": accuracy,
            }
        except Exception as e:
            logger.warning("Error calculating quiz stats from MongoDB: %s", e)
            return {
                "quizzes_attempted": 0,
                "quizzes_completed": 0,
                "total_questions_answered": 0,
                "total_correct": 0,
                "accuracy": 0,
            }
    return in_memory_store.get_user_quiz_stats(user_id)


@router.get("/api/notes/{note_id}/quiz/attempt", response_model=QuizAttemptResponse)
async def get_quiz_attempt(
    note_id: str,
    user: dict = Depends(get_current_student),
):
    """
    Fetch student's saved quiz progress / answers for a specific lecture note.
    Returns empty attempt defaults if no previous attempt exists.
    """
    clean_note_id = note_id.lower().strip()
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        doc = db.quiz_attempts.find_one({"user_id": user_id, "note_id": clean_note_id})
        if doc:
            return QuizAttemptResponse(
                note_id=clean_note_id,
                user_id=user_id,
                selected_answers=doc.get("selected_answers", {}),
                checked_questions=doc.get("checked_questions", {}),
                is_completed=doc.get("is_completed", False),
                score=doc.get("score", 0),
                total_questions=doc.get("total_questions", 0),
                percentage=doc.get("percentage", 0),
                updated_at=doc.get("updated_at"),
            )
    else:
        doc = in_memory_store.get_quiz_attempt(user_id, clean_note_id)
        if doc:
            return QuizAttemptResponse(
                note_id=clean_note_id,
                user_id=user_id,
                selected_answers=doc.get("selected_answers", {}),
                checked_questions=doc.get("checked_questions", {}),
                is_completed=doc.get("is_completed", False),
                score=doc.get("score", 0),
                total_questions=doc.get("total_questions", 0),
                percentage=doc.get("percentage", 0),
                updated_at=doc.get("updated_at"),
            )

    # Default empty attempt
    return QuizAttemptResponse(
        note_id=clean_note_id,
        user_id=user_id,
        selected_answers={},
        checked_questions={},
        is_completed=False,
        score=0,
        total_questions=0,
        percentage=0,
        updated_at=None,
    )


@router.put("/api/notes/{note_id}/quiz/attempt", response_model=QuizAttemptResponse)
async def save_quiz_attempt(
    note_id: str,
    payload: SaveQuizAttemptRequest,
    request: Request,
    user: dict = Depends(get_current_student),
):
    """
    Save or update student's quiz attempt (answers, checked state, score, completion).
    Validates CSRF token.
    """
    validate_csrf(request)
    clean_note_id = note_id.lower().strip()
    user_id = user["user_id"]
    now_iso = datetime.now(timezone.utc).isoformat()
    db = get_db_or_fail()

    update_data = {
        "user_id": user_id,
        "note_id": clean_note_id,
        "selected_answers": payload.selected_answers,
        "checked_questions": payload.checked_questions,
        "is_completed": payload.is_completed,
        "score": payload.score,
        "total_questions": payload.total_questions,
        "percentage": payload.percentage,
        "updated_at": now_iso,
    }

    if db is not None:
        db.quiz_attempts.update_one(
            {"user_id": user_id, "note_id": clean_note_id},
            {"$set": update_data},
            upsert=True,
        )
    else:
        in_memory_store.save_quiz_attempt(user_id, clean_note_id, update_data)

    return QuizAttemptResponse(**update_data)


@router.delete("/api/notes/{note_id}/quiz/attempt", status_code=204)
async def reset_quiz_attempt(
    note_id: str,
    request: Request,
    user: dict = Depends(get_current_student),
):
    """
    Resets all answers and progress for the topic quiz on this lecture note.
    Validates CSRF token.
    """
    validate_csrf(request)
    clean_note_id = note_id.lower().strip()
    user_id = user["user_id"]
    db = get_db_or_fail()

    if db is not None:
        db.quiz_attempts.delete_one({"user_id": user_id, "note_id": clean_note_id})
    else:
        in_memory_store.delete_quiz_attempt(user_id, clean_note_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/api/users/me/quiz-stats", response_model=UserQuizStats)
async def get_my_quiz_stats(user: dict = Depends(get_current_student)):
    """Returns the authenticated student's aggregated quiz performance statistics."""
    db = get_db_or_fail()
    stats = get_quiz_stats_for_user(user["user_id"], db=db)
    return UserQuizStats(**stats)

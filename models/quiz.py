from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SaveQuizAttemptRequest(BaseModel):
    selected_answers: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Map of question_id to list of chosen option IDs (e.g. {'q1': ['A']})"
    )
    checked_questions: Dict[str, bool] = Field(
        default_factory=dict,
        description="Map of question_id to whether the question answer was checked"
    )
    is_completed: bool = Field(
        False,
        description="Whether the entire quiz has been submitted/completed"
    )
    score: int = Field(0, description="Total correct questions")
    total_questions: int = Field(0, description="Total questions in the quiz")
    percentage: int = Field(0, description="Accuracy percentage (0-100)")


class QuizAttemptResponse(BaseModel):
    note_id: str
    user_id: str
    selected_answers: Dict[str, List[str]] = Field(default_factory=dict)
    checked_questions: Dict[str, bool] = Field(default_factory=dict)
    is_completed: bool = False
    score: int = 0
    total_questions: int = 0
    percentage: int = 0
    updated_at: Optional[str] = None


class UserQuizStats(BaseModel):
    quizzes_attempted: int = 0
    quizzes_completed: int = 0
    total_questions_answered: int = 0
    total_correct: int = 0
    accuracy: int = 0

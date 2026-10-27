from api.routes.auth import router as auth_router
from api.routes.notes import router as notes_router
from api.routes.comments import router as comments_router
from api.routes.quizzes import router as quizzes_router
from api.routes.scratchpad import router as scratchpad_router
from api.routes.moderation import router as moderation_router
from api.routes.notifications import router as notifications_router

__all__ = [
    "auth_router",
    "notes_router",
    "comments_router",
    "quizzes_router",
    "scratchpad_router",
    "moderation_router",
    "notifications_router",
]

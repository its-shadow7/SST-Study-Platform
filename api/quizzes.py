"""
Backward compatibility shim for api.quizzes.
Canonical location is now api.routes.quizzes.
"""
from api.routes.quizzes import router, get_quiz_stats_for_user

__all__ = ["router", "get_quiz_stats_for_user"]

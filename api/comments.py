"""
Backward compatibility shim for api.comments.
Canonical location is now api.routes.comments.
"""
from api.routes.comments import (
    router,
    sanitize_comment_content,
    check_comment_rate_limit,
    check_openai_moderation,
)
from api.core.rate_limiter import check_upstash_rate_limit, check_in_memory_rate_limit

__all__ = [
    "router",
    "sanitize_comment_content",
    "check_comment_rate_limit",
    "check_openai_moderation",
    "check_upstash_rate_limit",
    "check_in_memory_rate_limit",
]

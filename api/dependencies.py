"""
Backward compatibility shim for api.dependencies.
Canonical location is now api.core.dependencies.
"""
from api.core.dependencies import (
    get_db_or_fail,
    get_current_student,
    require_roles,
    require_moderator,
)

__all__ = [
    "get_db_or_fail",
    "get_current_student",
    "require_roles",
    "require_moderator",
]

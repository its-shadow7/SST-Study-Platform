"""
Backward compatibility shim for api.moderation.
Canonical location is now api.routes.moderation.
"""
from api.routes.moderation import router

__all__ = ["router"]

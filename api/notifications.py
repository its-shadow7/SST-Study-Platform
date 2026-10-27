"""
Backward compatibility shim for api.notifications.
Canonical location is now api.routes.notifications.
"""
from api.routes.notifications import router, create_notification

__all__ = ["router", "create_notification"]

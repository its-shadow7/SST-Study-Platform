"""
Backward compatibility shim for api.scratchpad.
Canonical location is now api.routes.scratchpad.
"""
from api.routes.scratchpad import router, check_scratchpad_rate_limit

__all__ = ["router", "check_scratchpad_rate_limit"]

"""
Backward compatibility shim for api.config.
Canonical location is now api.core.config.
"""
from api.core.config import Settings, settings, get_settings

__all__ = ["Settings", "settings", "get_settings"]

"""
Backward compatibility shim for api.rate_limiter.
Canonical location is now api.core.rate_limiter.
"""
from api.core.rate_limiter import (
    _local_rate_limit_store,
    _http_session,
    get_client_ip,
    check_upstash_rate_limit,
    check_in_memory_rate_limit,
    check_rate_limit,
)

__all__ = [
    "_local_rate_limit_store",
    "_http_session",
    "get_client_ip",
    "check_upstash_rate_limit",
    "check_in_memory_rate_limit",
    "check_rate_limit",
]

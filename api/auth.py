"""
Backward compatibility shim for api.auth.
Canonical location is now api.core.security.
"""
from api.core.security import (
    get_special_emails,
    is_special_email,
    extract_batch_info,
    is_dev_mock_login_allowed,
    generate_login_nonce,
    generate_refresh_token,
    hash_token,
    generate_csrf_token,
    validate_csrf,
    invalidate_csrf_token,
    create_access_jwt,
    decode_access_jwt,
    verify_google_id_token,
    set_auth_cookies,
    clear_auth_cookies,
)

__all__ = [
    "get_special_emails",
    "is_special_email",
    "extract_batch_info",
    "is_dev_mock_login_allowed",
    "generate_login_nonce",
    "generate_refresh_token",
    "hash_token",
    "generate_csrf_token",
    "validate_csrf",
    "invalidate_csrf_token",
    "create_access_jwt",
    "decode_access_jwt",
    "verify_google_id_token",
    "set_auth_cookies",
    "clear_auth_cookies",
]

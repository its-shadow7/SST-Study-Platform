from api.core.config import settings
from api.core.database import get_mongo_db, in_memory_store, seed_initial_notes
from api.core.security import (
    generate_login_nonce,
    consume_login_nonce,
    verify_google_id_token,
    create_access_jwt,
    decode_access_jwt,
    generate_refresh_token,
    hash_token,
    generate_csrf_token,
    validate_csrf,
    invalidate_csrf_token,
    set_auth_cookies,
    clear_auth_cookies,
    extract_batch_info,
    is_special_email,
    is_dev_mock_login_allowed
)
from api.core.dependencies import get_current_student, require_roles, require_moderator, get_db_or_fail
from api.core.rate_limiter import check_rate_limit, get_client_ip

__all__ = [
    "settings",
    "get_mongo_db",
    "in_memory_store",
    "seed_initial_notes",
    "generate_login_nonce",
    "consume_login_nonce",
    "verify_google_id_token",
    "create_access_jwt",
    "decode_access_jwt",
    "generate_refresh_token",
    "hash_token",
    "generate_csrf_token",
    "validate_csrf",
    "invalidate_csrf_token",
    "set_auth_cookies",
    "clear_auth_cookies",
    "extract_batch_info",
    "is_special_email",
    "is_dev_mock_login_allowed",
    "get_current_student",
    "require_roles",
    "require_moderator",
    "get_db_or_fail",
    "check_rate_limit",
    "get_client_ip"
]

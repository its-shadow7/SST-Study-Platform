import os
import pytest
from scripts.generate_keys import generate_keys
from api.core.config import settings

@pytest.fixture(scope="session", autouse=True)
def ensure_test_jwt_keys():
    """
    Ensure valid RS256 Base64 PEM keys are available for the test session.
    If not already configured via environment, generates ephemeral keys.
    """
    if not settings.JWT_PRIVATE_KEY_B64 or not settings.JWT_PUBLIC_KEY_B64:
        priv_b64, pub_b64 = generate_keys()
        settings.JWT_PRIVATE_KEY_B64 = priv_b64
        settings.JWT_PUBLIC_KEY_B64 = pub_b64
        os.environ["JWT_PRIVATE_KEY_B64"] = priv_b64
        os.environ["JWT_PUBLIC_KEY_B64"] = pub_b64

    # Ensure test special account is registered for test fixtures without hardcoding in app code
    existing_specials = [e for e in getattr(settings, "SPECIAL_EMAILS", "").split(",") if e]
    if "acca3402@gmail.com" not in existing_specials:
        existing_specials.append("acca3402@gmail.com")
        settings.SPECIAL_EMAILS = ",".join(existing_specials)
        os.environ["SPECIAL_EMAILS"] = settings.SPECIAL_EMAILS

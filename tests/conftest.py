import os
import pytest
from tooling.generate_keys import generate_keys
from api.config import settings

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

"""
Acceptance tests for the Antigravity Study Platform API.

Security contract enforced here:
- Mock tokens (mock:...) ONLY work when GOOGLE_CLIENT_ID is absent AND
  ALLOW_DEV_MOCK_LOGIN=True.  Tests that exercise mock login explicitly
  patch GOOGLE_CLIENT_ID to "" so the guard behaves as in local dev.
- Tests that verify mock-login is blocked in production patch
  GOOGLE_CLIENT_ID to a real-looking value and expect 401.
- CSRF tokens are now session-bound; tests echo the exact token returned
  by login/refresh.
- Bookmark note IDs are validated against the note manifest; the test
  uses a valid ID from data/notes-index.json.
"""

import pytest
from fastapi.testclient import TestClient
from api.config import settings
from api.auth import decode_access_jwt

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_dev_client():
    """
    Return a TestClient whose app instance sees GOOGLE_CLIENT_ID == ""
    (local-dev mode), enabling mock-token login.
    We patch the settings object directly; FastAPI's module-level import
    means we must also reload auth so its in_dev_mode check picks up the
    change.
    """
    original_cid = settings.GOOGLE_CLIENT_ID
    settings.GOOGLE_CLIENT_ID = ""          # simulate: no real OAuth client configured
    from api.index import app              # already imported; just grab reference
    client = TestClient(app)
    # We'll reset after the call — callers must do so themselves or use the
    # fixture below.
    return client, original_cid


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=False)
def dev_mode(monkeypatch):
    """Patch settings so mock tokens are accepted (local-dev simulation)."""
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "")
    monkeypatch.setattr(settings, "ALLOW_DEV_MOCK_LOGIN", True)


@pytest.fixture()
def dev_client(dev_mode):
    """TestClient operating in local-dev mode (mock login enabled)."""
    from api.index import app
    return TestClient(app)


@pytest.fixture()
def prod_client(monkeypatch):
    """TestClient with production environment simulation (mock login blocked)."""
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    from api.index import app
    return TestClient(app)


# ---------------------------------------------------------------------------
# Health check (no auth required)
# ---------------------------------------------------------------------------

def test_health_check(prod_client):
    response = prod_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "sst-study-platform"


# ---------------------------------------------------------------------------
# Nonce endpoint
# ---------------------------------------------------------------------------

def test_nonce_endpoint_returns_nonce(dev_client):
    resp = dev_client.get("/api/auth/nonce")
    assert resp.status_code == 200
    data = resp.json()
    assert "nonce" in data
    assert len(data["nonce"]) >= 16


# ---------------------------------------------------------------------------
# Google login — dev mode (mock tokens)
# ---------------------------------------------------------------------------

def test_google_login_dev_mode(dev_client):
    payload = {"id_token": "mock:student@sst.scaler.com"}
    response = dev_client.post("/api/auth/google", json=payload)
    assert response.status_code == 200, response.json()

    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "student@sst.scaler.com"
    assert "csrf_token" in data

    # Check cookies
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

    access_token = response.cookies["access_token"]
    claims = decode_access_jwt(access_token)
    assert claims["role"] == "sst_student"
    assert claims["iss"] == settings.JWT_ISSUER
    assert claims["aud"] == settings.JWT_AUDIENCE
    assert claims["email"] == "student@sst.scaler.com"
    # kid must be present in the JWT header
    import jwt as pyjwt
    header = pyjwt.get_unverified_header(access_token)
    assert "kid" in header and header["kid"]


def test_google_login_disallowed_domain(dev_client):
    payload = {"id_token": "mock:hacker@gmail.com"}
    response = dev_client.post("/api/auth/google", json=payload)
    assert response.status_code == 403
    err = response.json()
    assert "error" in err
    assert err["error"] == "FORBIDDEN"
    assert "request_id" in err


def test_google_login_non_student_sst_email_rejected(dev_client):
    """Staff/faculty, generic @sst.scaler.com emails lacking roll numbers, or unauthorized special@ emails must be rejected with 403."""
    for bad_email in ["professor.smith@sst.scaler.com", "special@sst.scaler.com", "admin@sst.scaler.com", "special_reviewer@sst.scaler.com"]:
        payload = {"id_token": f"mock:{bad_email}"}
        response = dev_client.post("/api/auth/google", json=payload)
        assert response.status_code == 403
        err = response.json()
        assert err["error"] == "FORBIDDEN"


def test_google_login_acca3402_special_gmail_allowed(dev_client):
    """acca3402@gmail.com is the authorized special account and receives full 16-term curriculum access."""
    payload = {"id_token": "mock:acca3402@gmail.com"}
    response = dev_client.post("/api/auth/google", json=payload)
    assert response.status_code == 200, response.json()

    data = response.json()
    user = data["user"]
    assert user["email"] == "acca3402@gmail.com"
    assert user["is_special"] is True
    assert isinstance(user.get("needs_profile_setup"), bool)
    assert user["max_allowed_term"] == 16
    assert "access_token" in response.cookies


def test_special_email_profile_setup_completion(dev_client):
    """Special user completes one-time onboarding by submitting user details via PATCH /api/users/me."""
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:acca3402@gmail.com"})
    assert login_resp.status_code == 200
    csrf_token = login_resp.json()["csrf_token"]
    cookies = login_resp.cookies

    # Submit profile setup details
    update_payload = {
        "display_name": "Prof. Alan Turing",
        "username": "alan_turing_special",
        "active_term": 5,
        "bio": "Visiting Faculty in Computation",
        "needs_profile_setup": False
    }
    patch_resp = dev_client.patch(
        "/api/users/me",
        json=update_payload,
        headers={"x-csrf-token": csrf_token},
        cookies=cookies
    )
    assert patch_resp.status_code == 200, patch_resp.json()
    updated = patch_resp.json()
    assert updated["display_name"] == "Prof. Alan Turing"
    assert updated["username"] == "alan_turing_special"
    assert updated["active_term"] == 5
    assert updated["bio"] == "Visiting Faculty in Computation"
    assert updated["needs_profile_setup"] is False

    # Verify subsequent GET /api/users/me retains the completed profile state
    me_resp = dev_client.get("/api/users/me", cookies=cookies)
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["display_name"] == "Prof. Alan Turing"
    assert me_data["needs_profile_setup"] is False


# ---------------------------------------------------------------------------
# Mock login blocked in production (GOOGLE_CLIENT_ID set)
# ---------------------------------------------------------------------------

def test_mock_login_blocked_in_production(prod_client):
    """When GOOGLE_CLIENT_ID is configured, mock tokens must be rejected."""
    payload = {"id_token": "mock:student@sst.scaler.com"}
    response = prod_client.post("/api/auth/google", json=payload)
    assert response.status_code == 401
    assert response.json()["error"] == "UNAUTHORIZED"


# ---------------------------------------------------------------------------
# Full authenticated flow: profile + bookmarks
# ---------------------------------------------------------------------------

def test_authenticated_user_profile_and_bookmarks(dev_client):
    # 1. Login
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:testuser@sst.scaler.com"})
    assert login_resp.status_code == 200, login_resp.json()
    csrf_token = login_resp.json()["csrf_token"]

    # Extract cookies
    cookies = login_resp.cookies

    # 2. GET /api/users/me
    me_resp = dev_client.get("/api/users/me", cookies=cookies)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "testuser@sst.scaler.com"

    # 3. Add Bookmark — use a real note ID from the manifest
    bm_resp = dev_client.put(
        "/api/bookmarks/cn-lecture-01-introduction",
        cookies=cookies,
        headers={"x-csrf-token": csrf_token, "origin": "http://localhost:5173"}
    )
    assert bm_resp.status_code in [200, 201], bm_resp.json()
    assert bm_resp.json()["status"] == "created"

    # 4. Idempotent duplicate bookmark
    bm_dup_resp = dev_client.put(
        "/api/bookmarks/cn-lecture-01-introduction",
        cookies=cookies,
        headers={"x-csrf-token": csrf_token, "origin": "http://localhost:5173"}
    )
    assert bm_dup_resp.json()["status"] == "already_bookmarked"

    # 5. List bookmarks
    list_resp = dev_client.get("/api/bookmarks", cookies=cookies)
    assert list_resp.status_code == 200
    bms = list_resp.json()["bookmarks"]
    assert len(bms) == 1
    assert bms[0]["note_id"] == "cn-lecture-01-introduction"

    # 6. Delete Bookmark
    del_bm_resp = dev_client.delete(
        "/api/bookmarks/cn-lecture-01-introduction",
        cookies=cookies,
        headers={"x-csrf-token": csrf_token, "origin": "http://localhost:5173"}
    )
    assert del_bm_resp.status_code == 204

    # 7. Verify bookmark is deleted
    list_after_resp = dev_client.get("/api/bookmarks", cookies=cookies)
    assert len(list_after_resp.json()["bookmarks"]) == 0


# ---------------------------------------------------------------------------
# Invalid note ID rejected by bookmark manifest validation
# ---------------------------------------------------------------------------

def test_bookmark_invalid_note_id_rejected(dev_client):
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:bm_test@sst.scaler.com"})
    assert login_resp.status_code == 200
    csrf_token = login_resp.json()["csrf_token"]
    cookies = login_resp.cookies

    resp = dev_client.put(
        "/api/bookmarks/totally-fake-note-xyz-999",
        cookies=cookies,
        headers={"x-csrf-token": csrf_token, "origin": "http://localhost:5173"}
    )
    assert resp.status_code == 404
    assert resp.json()["error"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# Session refresh and logout
# ---------------------------------------------------------------------------

def test_session_refresh_and_logout(dev_client):
    # Login
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:student2@sst.scaler.com"})
    assert login_resp.status_code == 200, login_resp.json()
    csrf_token = login_resp.json()["csrf_token"]
    cookies = login_resp.cookies

    # Refresh — no CSRF check on this endpoint by design
    ref_resp = dev_client.post(
        "/api/auth/refresh",
        cookies=cookies,
        headers={"origin": "http://localhost:5173"}
    )
    assert ref_resp.status_code == 200, ref_resp.json()
    assert "access_token" in ref_resp.cookies
    assert "refresh_token" in ref_resp.cookies
    new_cookies = ref_resp.cookies
    new_csrf = ref_resp.json()["csrf_token"]

    # Logout — must use the CSRF token issued by refresh
    logout_resp = dev_client.post(
        "/api/auth/logout",
        cookies=new_cookies,
        headers={"x-csrf-token": new_csrf, "origin": "http://localhost:5173"}
    )
    assert logout_resp.status_code == 204
    # Logout must send cookie-expiry headers
    set_cookie = logout_resp.headers.get("set-cookie", "")
    assert "access_token=" in set_cookie
    assert "refresh_token=" in set_cookie

    # Old refresh token must now be invalid
    refreshed_after_logout = dev_client.post("/api/auth/refresh")
    assert refreshed_after_logout.status_code == 401


# ---------------------------------------------------------------------------
# CSRF — stale/unknown token must be rejected
# ---------------------------------------------------------------------------

def test_csrf_unknown_token_rejected(dev_client):
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:csrf_test@sst.scaler.com"})
    assert login_resp.status_code == 200
    cookies = login_resp.cookies

    resp = dev_client.put(
        "/api/bookmarks/cn-lecture-01-introduction",
        cookies=cookies,
        headers={"x-csrf-token": "aaabbbcccdddeeefffggghhh", "origin": "http://localhost:5173"}
    )
    assert resp.status_code == 403
    assert resp.json()["error"] == "FORBIDDEN"


# ---------------------------------------------------------------------------
# Unauthenticated access to protected note routes
# ---------------------------------------------------------------------------

def test_unauthenticated_note_access_rejected():
    from api.index import app
    fresh_client = TestClient(app)
    idx_resp = fresh_client.get("/data/notes-index.json")
    assert idx_resp.status_code == 401
    assert idx_resp.json()["error"] == "UNAUTHORIZED"

    note_resp = fresh_client.get("/data/notes/cn-lecture-01-introduction.json")
    assert note_resp.status_code == 401
    assert note_resp.json()["error"] == "UNAUTHORIZED"


# ---------------------------------------------------------------------------
# Authenticated access to protected note routes
# ---------------------------------------------------------------------------

def test_authenticated_note_access_allowed(dev_client):
    # Sign in as approved SST student
    login_resp = dev_client.post("/api/auth/google", json={"id_token": "mock:verified@sst.scaler.com"})
    assert login_resp.status_code == 200, login_resp.json()
    cookies = login_resp.cookies

    # Access protected notes index
    idx_resp = dev_client.get("/data/notes-index.json", cookies=cookies)
    assert idx_resp.status_code == 200
    notes_list = idx_resp.json()
    assert isinstance(notes_list, list)
    assert len(notes_list) >= 1

    # Access protected individual note
    note_resp = dev_client.get("/data/notes/cn-lecture-01-introduction.json", cookies=cookies)
    assert note_resp.status_code == 200
    note_data = note_resp.json()
    assert note_data["note_id"] == "cn-lecture-01-introduction"
    assert note_data["subject_code"] == "CN"


# ---------------------------------------------------------------------------
# Domain lookalike / non-SST domains
# ---------------------------------------------------------------------------

def test_lookalike_and_non_sst_domains_rejected(dev_client):
    for bad_email in [
        "student@sst.scaler.com.attacker.com",
        "student@scaler.com",
        "student@gmail.com",
        "fake@sst.scaler.org"
    ]:
        resp = dev_client.post("/api/auth/google", json={"id_token": f"mock:{bad_email}"})
        assert resp.status_code == 403, f"Expected 403 for {bad_email}, got {resp.status_code}"
        assert resp.json()["error"] == "FORBIDDEN"


# ---------------------------------------------------------------------------
# Common API Error Format: Validation Errors (422)
# ---------------------------------------------------------------------------

def test_validation_error_format_422(dev_client):
    """Payloads failing Pydantic schema validation return standardized error response."""
    resp = dev_client.post("/api/auth/google", json={})
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"] == "VALIDATION_ERROR"
    assert "request_id" in data
    assert "message" in data
    assert "details" in data
    assert isinstance(data["details"], list)


# ---------------------------------------------------------------------------
# Rate Limiting & Redis Fail-Closed (503) & Quota Exhaustion
# ---------------------------------------------------------------------------

def test_redis_fail_closed_503_behavior(prod_client, monkeypatch):
    """
    In production, if the Upstash Redis rate limiter is configured but unreachable,
    the endpoint must fail closed and return 503 SERVICE_UNAVAILABLE.
    """
    import requests
    from api import rate_limiter

    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "https://mock-redis.upstash.io")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "mock-token-secret")
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")

    def mock_post_failure(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Redis connection refused")

    monkeypatch.setattr(rate_limiter._http_session, "post", mock_post_failure)

    resp = prod_client.get("/api/auth/nonce")
    assert resp.status_code == 503
    data = resp.json()
    assert data["error"] == "SERVICE_UNAVAILABLE"
    assert "request_id" in data
    assert "Rate limit service temporarily unavailable" in data["message"]


def test_redis_quota_exhaustion_503_behavior(prod_client, monkeypatch):
    """
    If Upstash returns 429 quota exhaustion, the service fails closed with 503.
    """
    from unittest.mock import MagicMock
    from api import rate_limiter

    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "https://mock-redis.upstash.io")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "mock-token-secret")
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")

    mock_resp = MagicMock()
    mock_resp.status_code = 429
    mock_resp.text = '{"error": "Daily request limit exceeded"}'

    monkeypatch.setattr(rate_limiter._http_session, "post", lambda *args, **kwargs: mock_resp)

    resp = prod_client.get("/api/auth/nonce")
    assert resp.status_code == 503
    data = resp.json()
    assert data["error"] == "SERVICE_UNAVAILABLE"
    assert "request_id" in data


def test_rate_limit_exceeded_429(dev_client, monkeypatch):
    """Exceeding the request threshold returns 429 TOO_MANY_REQUESTS."""
    from api.rate_limiter import _local_rate_limit_store
    _local_rate_limit_store.clear()

    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_URL", "")
    monkeypatch.setattr(settings, "UPSTASH_REDIS_REST_TOKEN", "")
    monkeypatch.setattr(settings, "RATE_LIMIT_NONCE_MAX", 2)
    monkeypatch.setattr(settings, "RATE_LIMIT_NONCE_WINDOW", 60)

    # 1st and 2nd should pass
    r1 = dev_client.get("/api/auth/nonce")
    assert r1.status_code == 200
    r2 = dev_client.get("/api/auth/nonce")
    assert r2.status_code == 200

    # 3rd should be rate-limited
    r3 = dev_client.get("/api/auth/nonce")
    assert r3.status_code == 429
    data = r3.json()
    assert data["error"] == "TOO_MANY_REQUESTS"
    assert "request_id" in data


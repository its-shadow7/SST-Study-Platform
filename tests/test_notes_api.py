"""
Tests for the Notes REST API (/api/notes), term-level access enforcement,
startup catalogue seeding, projection efficiency, and Moderator Note Studio CRUD.
"""

import pytest
from fastapi.testclient import TestClient
from api.core.config import settings
from api.core.database import in_memory_store, seed_initial_notes


@pytest.fixture(autouse=False)
def dev_mode(monkeypatch):
    """Patch settings so mock tokens are accepted in local development."""
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "")
    monkeypatch.setattr(settings, "ALLOW_DEV_MOCK_LOGIN", True)


@pytest.fixture()
def client(dev_mode):
    """FastAPI TestClient in dev mode with seeded InMemoryStore."""
    from api.index import app
    # Ensure startup seeding is populated
    seed_initial_notes(None)
    return TestClient(app)


# ---------------------------------------------------------------------------
# Test 1: Startup Seeding Verification
# ---------------------------------------------------------------------------

def test_startup_fixtures_seeded_into_in_memory_store():
    """Confirms that startup fixture seeding populates all lecture notes into InMemoryStore."""
    seed_initial_notes(None)
    notes = in_memory_store.list_notes(include_drafts=True)
    assert len(notes) >= 3, f"Expected at least 3 fixture notes, found {len(notes)}"
    
    note_ids = {n["note_id"] for n in notes}
    assert "cn-lecture-01-introduction" in note_ids
    assert "cml-lecture-01-linear-regression" in note_ids


# ---------------------------------------------------------------------------
# Test 2: Unauthenticated Access Blocked
# ---------------------------------------------------------------------------

def test_unauthenticated_note_endpoints_rejected(client):
    """Unauthenticated requests to /api/notes or /api/notes/{id} return 401 Unauthorized."""
    resp_index = client.get("/api/notes")
    assert resp_index.status_code == 401
    assert resp_index.json()["error"] == "UNAUTHORIZED"

    resp_note = client.get("/api/notes/cn-lecture-01-introduction")
    assert resp_note.status_code == 401
    assert resp_note.json()["error"] == "UNAUTHORIZED"


# ---------------------------------------------------------------------------
# Test 3: Term-Level Access Gating on Note Catalogue (GET /api/notes)
# ---------------------------------------------------------------------------

def test_term_access_catalogue_filtering_by_year_of_study(client):
    """
    Year 1 student (e.g. surya.26bcs10632@sst.scaler.com -> admitted 2026 -> Year 1 -> max_allowed_term=4)
    only receives notes with term_number <= 4 in GET /api/notes.
    Higher-term notes (e.g. Term 5) are excluded from the response.
    """
    login_resp = client.post("/api/auth/google", json={"id_token": "mock:student.26bcs001@sst.scaler.com"})
    assert login_resp.status_code == 200
    cookies = login_resp.cookies

    # Fetch notes catalogue
    cat_resp = client.get("/api/notes", cookies=cookies)
    assert cat_resp.status_code == 200
    notes = cat_resp.json()

    assert len(notes) > 0
    for note in notes:
        assert note["term_number"] <= 4, f"Year 1 student received note {note['note_id']} from Term {note['term_number']}"
        # Projection verification: lightweight index items MUST NOT include heavy sections or quiz
        assert "sections" not in note
        assert "quiz" not in note


# ---------------------------------------------------------------------------
# Test 4: Term-Level Access Gating on Individual Note (GET /api/notes/{id})
# ---------------------------------------------------------------------------

def test_term_access_individual_note_403_forbidden(client):
    """
    When a Year 1 student attempts to fetch a Term 5 note (e.g. cml-t5-l02),
    FastAPI immediately rejects the request with 403 FORBIDDEN.
    """
    # Seed a Term 5 test note into store
    in_memory_store.save_note({
        "note_id": "test-t5-advanced-deep-learning",
        "term": "Term 5",
        "term_number": 5,
        "subject_code": "DL",
        "topic_title": "Advanced Deep Learning",
        "summary": "Term 5 neural network theory",
        "sections": [{"section_id": "s1", "heading": "Intro", "body": "Math here", "citations": []}],
        "quiz": [],
        "approval_status": "approved",
        "last_updated": "2026-10-27T00:00:00Z"
    })

    # 1. Login as Year 1 student (max_allowed_term = 4)
    y1_login = client.post("/api/auth/google", json={"id_token": "mock:student.26bcs999@sst.scaler.com"})
    assert y1_login.status_code == 200
    y1_cookies = y1_login.cookies

    # Attempt to access Term 5 note -> 403 FORBIDDEN
    y1_fetch = client.get("/api/notes/test-t5-advanced-deep-learning", cookies=y1_cookies)
    assert y1_fetch.status_code == 403
    assert y1_fetch.json()["error"] == "FORBIDDEN"
    assert "beyond your current academic year" in y1_fetch.json()["message"]

    # 2. Login as Year 2 student (batch '25 -> max_allowed_term = 8)
    y2_login = client.post("/api/auth/google", json={"id_token": "mock:student.25bcs888@sst.scaler.com"})
    assert y2_login.status_code == 200
    y2_cookies = y2_login.cookies

    # Accessing Term 5 note succeeds -> 200 OK
    y2_fetch = client.get("/api/notes/test-t5-advanced-deep-learning", cookies=y2_cookies)
    assert y2_fetch.status_code == 200
    note_data = y2_fetch.json()
    assert note_data["note_id"] == "test-t5-advanced-deep-learning"
    assert len(note_data["sections"]) == 1


# ---------------------------------------------------------------------------
# Test 5: Moderator Bypass of Term Access Limits
# ---------------------------------------------------------------------------

def test_moderator_bypasses_term_access_limits(client):
    """Moderators and Administrators can access notes from all terms (1 to 16)."""
    in_memory_store.save_note({
        "note_id": "test-t12-quantum-computing",
        "term": "Term 12",
        "term_number": 12,
        "subject_code": "QC",
        "topic_title": "Quantum Computing",
        "summary": "Term 12 specialized elective",
        "sections": [{"section_id": "s1", "heading": "Qubits", "body": "Quantum state", "citations": []}],
        "approval_status": "approved",
        "last_updated": "2026-10-27T00:00:00Z"
    })

    # Login as admin
    admin_login = client.post("/api/auth/google", json={"id_token": "mock:acca3402@gmail.com"})
    assert admin_login.status_code == 200
    admin_cookies = admin_login.cookies

    # Admin accesses Term 12 note -> 200 OK
    resp = client.get("/api/notes/test-t12-quantum-computing", cookies=admin_cookies)
    assert resp.status_code == 200
    assert resp.json()["note_id"] == "test-t12-quantum-computing"


# ---------------------------------------------------------------------------
# Test 6: Moderator CRUD Lifecycle (Create, Update, Delete) & CSRF Enforcement
# ---------------------------------------------------------------------------

def test_moderator_note_crud_lifecycle_and_csrf_protection(client):
    """
    Verifies full lifecycle of Note Studio operations:
    1. Regular student rejected on POST /api/notes (403)
    2. Moderator without CSRF rejected (403)
    3. Moderator creates note -> 201 Created
    4. Moderator updates note -> 200 OK
    5. Moderator deletes note -> 204 No Content
    """
    # 1. Student attempt to create note fails
    student_login = client.post("/api/auth/google", json={"id_token": "mock:student.25bcs111@sst.scaler.com"})
    student_csrf = student_login.json()["csrf_token"]
    student_cookies = student_login.cookies

    payload = {
        "schema_version": 1,
        "note_id": "studio-test-lecture-01",
        "term": "Term 3",
        "term_number": 3,
        "subject_code": "OS",
        "topic_title": "Operating Systems Virtual Memory",
        "summary": "Memory management algorithms",
        "sections": [
            {
                "section_id": "sec-01",
                "heading": "Paging Mechanisms",
                "body": "Paging maps virtual addresses to physical page frames.",
                "citations": ["Silberschatz et al. (2018)"]
            }
        ],
        "quiz": {
            "title": "OS Memory Quiz",
            "description": "Comprehension check",
            "estimated_minutes": 10,
            "questions": []
        },
        "approval_status": "approved"
    }

    fail_student = client.post(
        "/api/notes",
        json=payload,
        cookies=student_cookies,
        headers={"x-csrf-token": student_csrf, "origin": "http://localhost:5173"}
    )
    assert fail_student.status_code == 403

    # 2. Login as Administrator
    admin_login = client.post("/api/auth/google", json={"id_token": "mock:acca3402@gmail.com"})
    admin_csrf = admin_login.json()["csrf_token"]
    admin_cookies = admin_login.cookies

    # Missing CSRF token rejected
    fail_no_csrf = client.post(
        "/api/notes",
        json=payload,
        cookies=admin_cookies,
        headers={"origin": "http://localhost:5173"}
    )
    assert fail_no_csrf.status_code == 403

    # 3. Create Note with valid CSRF -> 201 Created
    create_resp = client.post(
        "/api/notes",
        json=payload,
        cookies=admin_cookies,
        headers={"x-csrf-token": admin_csrf, "origin": "http://localhost:5173"}
    )
    assert create_resp.status_code == 201
    created_note = create_resp.json()
    assert created_note["note_id"] == "studio-test-lecture-01"
    assert created_note["topic_title"] == "Operating Systems Virtual Memory"

    # 4. Update Note (PUT /api/notes/{id})
    payload["topic_title"] = "Operating Systems Virtual Memory & TLB Caches"
    update_resp = client.put(
        "/api/notes/studio-test-lecture-01",
        json=payload,
        cookies=admin_cookies,
        headers={"x-csrf-token": admin_csrf, "origin": "http://localhost:5173"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["topic_title"] == "Operating Systems Virtual Memory & TLB Caches"

    # 5. Delete Note (DELETE /api/notes/{id})
    del_resp = client.delete(
        "/api/notes/studio-test-lecture-01",
        cookies=admin_cookies,
        headers={"x-csrf-token": admin_csrf, "origin": "http://localhost:5173"}
    )
    assert del_resp.status_code == 204

    # Verify note is deleted
    get_del = client.get("/api/notes/studio-test-lecture-01", cookies=admin_cookies)
    assert get_del.status_code == 404

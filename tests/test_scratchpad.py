import uuid
import pytest
from fastapi.testclient import TestClient
from api.config import settings
from api.index import app
from api.database import in_memory_store, get_mongo_db


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", "")
    monkeypatch.setattr(settings, "ALLOW_DEV_MOCK_LOGIN", True)
    # Clear in-memory stores for clean testing
    in_memory_store.scratchpads.clear()
    in_memory_store.users.clear()
    in_memory_store.sub_to_id.clear()
    in_memory_store.username_to_id.clear()
    # Clean up test scratchpads in MongoDB if connected
    db = get_mongo_db()
    if db is not None:
        db.scratchpads.delete_many({"note_id": {"$regex": "^test-note-"}})


def _login(client: TestClient, email: str = "alice.25bcs10001@sst.scaler.com"):
    resp = client.post("/api/auth/google", json={"id_token": f"mock:{email}"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    csrf = data["csrf_token"]
    user_id = data["user"]["user_id"]
    return csrf, user_id


def test_scratchpad_requires_jwt():
    client = TestClient(app)
    # GET summary
    res_summary = client.get("/api/scratchpads/summary")
    assert res_summary.status_code == 401

    # GET note scratchpad
    res_get = client.get("/api/notes/test-note-1/scratchpad")
    assert res_get.status_code == 401

    # PUT note scratchpad
    res_put = client.put("/api/notes/test-note-1/scratchpad", json={"content": "Notes"})
    assert res_put.status_code == 401


def test_scratchpad_get_default_empty():
    client = TestClient(app)
    csrf, user_id = _login(client, f"student_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    res = client.get(f"/api/notes/{note_id}/scratchpad")
    assert res.status_code == 200
    data = res.json()
    assert data["content"] == ""
    assert data["updated_at"] is None
    assert data["note_id"] == note_id


def test_scratchpad_upsert_and_summary():
    client = TestClient(app)
    csrf, user_id = _login(client, f"student_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note1 = f"test-note-a-{uuid.uuid4().hex[:6]}"
    note2 = f"test-note-b-{uuid.uuid4().hex[:6]}"

    # 1. Summary initially empty
    sum_res1 = client.get("/api/scratchpads/summary")
    assert sum_res1.status_code == 200
    assert sum_res1.json()["note_ids"] == []

    # 2. Put note 1
    content1 = "## Key concepts\n- KaTeX: $E = mc^2$\n- AI summary notes."
    put_res1 = client.put(f"/api/notes/{note1}/scratchpad", json={"content": content1})
    assert put_res1.status_code == 200
    assert put_res1.json()["content"] == content1
    assert put_res1.json()["updated_at"] is not None

    # 3. Put note 2
    content2 = "TCP Three-way handshake:\n1. SYN\n2. SYN-ACK\n3. ACK"
    put_res2 = client.put(f"/api/notes/{note2}/scratchpad", json={"content": content2})
    assert put_res2.status_code == 200

    # 4. Summary now contains both notes
    sum_res2 = client.get("/api/scratchpads/summary")
    assert sum_res2.status_code == 200
    note_ids = sum_res2.json()["note_ids"]
    assert note1 in note_ids
    assert note2 in note_ids

    # 5. Emptying note 1 removes it from summary
    put_empty = client.put(f"/api/notes/{note1}/scratchpad", json={"content": ""})
    assert put_empty.status_code == 200
    sum_res3 = client.get("/api/scratchpads/summary")
    assert note1 not in sum_res3.json()["note_ids"]
    assert note2 in sum_res3.json()["note_ids"]


def test_scratchpad_max_length_validation():
    client = TestClient(app)
    csrf, user_id = _login(client, f"student_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Content within limit (30,000 chars)
    valid_content = "A" * 30000
    res_valid = client.put(f"/api/notes/{note_id}/scratchpad", json={"content": valid_content})
    assert res_valid.status_code == 200

    # Content exceeding limit (30,001 chars)
    invalid_content = "A" * 30001
    res_invalid = client.put(f"/api/notes/{note_id}/scratchpad", json={"content": invalid_content})
    assert res_invalid.status_code == 422

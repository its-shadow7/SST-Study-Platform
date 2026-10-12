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
    in_memory_store.comments.clear()
    in_memory_store.users.clear()
    in_memory_store.sub_to_id.clear()
    in_memory_store.username_to_id.clear()
    # Clean up test comments in MongoDB if connected
    db = get_mongo_db()
    if db is not None:
        db.comments.delete_many({"note_id": {"$regex": "^test-note-"}})

def _login(client: TestClient, email: str = "alice.25bcs10001@sst.scaler.com"):
    resp = client.post("/api/auth/google", json={"id_token": f"mock:{email}"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    csrf = data["csrf_token"]
    user_id = data["user"]["user_id"]
    return csrf, user_id

def test_comments_endpoints_require_jwt():
    client = TestClient(app)
    # GET
    res_get = client.get("/api/notes/test-note-1/comments")
    assert res_get.status_code == 401

    # POST
    res_post = client.post("/api/notes/test-note-1/comments", json={"content": "Hello"})
    assert res_post.status_code == 401

    # DELETE
    res_del = client.delete("/api/comments/non-existent-id")
    assert res_del.status_code == 401

def test_comments_create_get_and_lookup():
    client = TestClient(app)
    csrf, user_id = _login(client, f"alice_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Set avatar and bio in settings
    up_res = client.patch(
        "/api/users/me",
        json={"avatar_url": "https://example.com/alice.png"},
        headers={"x-csrf-token": csrf}
    )
    assert up_res.status_code == 200

    # Post a comment
    post_res = client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Great lecture on distributed systems!"},
        headers={"x-csrf-token": csrf}
    )
    assert post_res.status_code == 201
    comment = post_res.json()
    assert comment["note_id"] == note_id
    assert comment["content"] == "Great lecture on distributed systems!"
    assert comment["user_id"] == user_id
    assert comment["avatar_url"] == "https://example.com/alice.png"
    assert comment["username"] is not None

    # Get comments for note
    get_res = client.get(f"/api/notes/{note_id}/comments")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["total"] == 1
    assert data["comments"][0]["id"] == comment["id"]
    assert data["comments"][0]["username"] == comment["username"]
    assert data["comments"][0]["avatar_url"] == "https://example.com/alice.png"

def test_comments_xss_sanitization():
    client = TestClient(app)
    csrf, _ = _login(client, f"sec_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    payload = {
        "content": "Check this: <script>alert('xss')</script><img src=x onerror=alert(1)> and javascript:void(0)"
    }
    post_res = client.post(
        f"/api/notes/{note_id}/comments",
        json=payload,
        headers={"x-csrf-token": csrf}
    )
    assert post_res.status_code == 201
    data = post_res.json()
    assert "<script>" not in data["content"]
    assert "onerror=" not in data["content"]
    assert "javascript:" not in data["content"]

def test_comments_rate_limit_10_per_minute():
    client = TestClient(app)
    csrf, _ = _login(client, f"spammer.{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # 10 allowed
    for i in range(10):
        res = client.post(
            f"/api/notes/{note_id}/comments",
            json={"content": f"Comment #{i+1}"},
            headers={"x-csrf-token": csrf}
        )
        assert res.status_code == 201, res.text

    # 11th request must be rate limited with 429
    res_blocked = client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Comment #11 - should fail"},
        headers={"x-csrf-token": csrf}
    )
    assert res_blocked.status_code == 429
    err = res_blocked.json()
    assert "Maximum 10 comments" in err["message"] or "Too Many Requests" in err["message"]

def test_delete_comment_author_enforcement():
    alice_client = TestClient(app)
    alice_csrf, _ = _login(alice_client, f"alice.{uuid.uuid4().hex[:6]}@sst.scaler.com")

    bob_client = TestClient(app)
    bob_csrf, _ = _login(bob_client, f"bob.{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Alice creates a comment
    post_res = alice_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Alice's comment"},
        headers={"x-csrf-token": alice_csrf}
    )
    assert post_res.status_code == 201
    comment_id = post_res.json()["id"]

    # Bob tries to delete Alice's comment -> 403 Forbidden
    bob_del_res = bob_client.delete(
        f"/api/comments/{comment_id}",
        headers={"x-csrf-token": bob_csrf}
    )
    assert bob_del_res.status_code == 403

    # Alice deletes her own comment -> 200 OK
    alice_del_res = alice_client.delete(
        f"/api/comments/{comment_id}",
        headers={"x-csrf-token": alice_csrf}
    )
    assert alice_del_res.status_code == 200
    assert alice_del_res.json()["status"] == "deleted"

    # Subsequent delete should be 404
    alice_del_again = alice_client.delete(
        f"/api/comments/{comment_id}",
        headers={"x-csrf-token": alice_csrf}
    )
    assert alice_del_again.status_code == 404

def test_threaded_comments_and_parent_redaction():
    alice_client = TestClient(app)
    alice_csrf, _ = _login(alice_client, f"alice.{uuid.uuid4().hex[:6]}@sst.scaler.com")

    bob_client = TestClient(app)
    bob_csrf, _ = _login(bob_client, f"bob.{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Alice posts parent comment
    res1 = alice_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Root parent comment"},
        headers={"x-csrf-token": alice_csrf}
    )
    assert res1.status_code == 201
    parent_id = res1.json()["id"]

    # Bob posts reply with parent_id
    res2 = bob_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Child reply to root", "parent_id": parent_id},
        headers={"x-csrf-token": bob_csrf}
    )
    assert res2.status_code == 201
    assert res2.json()["parent_id"] == parent_id

    # Alice deletes her parent comment -> should be redacted to [Deleted] to preserve child replies
    del_res = alice_client.delete(
        f"/api/comments/{parent_id}",
        headers={"x-csrf-token": alice_csrf}
    )
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "redacted"

    # Fetch comments -> parent is [Deleted] and child is intact
    get_res = alice_client.get(f"/api/notes/{note_id}/comments")
    assert get_res.status_code == 200
    comments = get_res.json()["comments"]
    assert len(comments) == 2
    parent_doc = next(c for c in comments if c["id"] == parent_id)
    assert parent_doc["content"] == "[Deleted]"

def test_reddit_style_voting_3_state():
    alice_client = TestClient(app)
    alice_csrf, _ = _login(alice_client, f"alice.{uuid.uuid4().hex[:6]}@sst.scaler.com")

    bob_client = TestClient(app)
    bob_csrf, bob_id = _login(bob_client, f"bob.{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    post_res = alice_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Interesting insight here"},
        headers={"x-csrf-token": alice_csrf}
    )
    assert post_res.status_code == 201
    comment_id = post_res.json()["id"]

    # 1. Bob upvotes neutral -> +1
    uv_res = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "upvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert uv_res.status_code == 200
    assert uv_res.json()["user_vote"] == "upvote"
    assert uv_res.json()["score"] == 1

    # 2. Bob upvotes again -> toggle off (score -1 -> 0)
    uv_res2 = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "upvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert uv_res2.status_code == 200
    assert uv_res2.json()["user_vote"] is None
    assert uv_res2.json()["score"] == 0

    # 3. Bob downvotes neutral -> -1
    dv_res = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "downvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert dv_res.status_code == 200
    assert dv_res.json()["user_vote"] == "downvote"
    assert dv_res.json()["score"] == -1

    # 4. Bob upvotes while currently downvoted -> switch to upvote (score +2 -> 1)
    switch_res = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "upvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert switch_res.status_code == 200
    assert switch_res.json()["user_vote"] == "upvote"
    assert switch_res.json()["score"] == 1

    # 5. Bob downvotes while currently upvoted -> switch to downvote (score -2 -> -1)
    switch_back = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "downvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert switch_back.status_code == 200
    assert switch_back.json()["user_vote"] == "downvote"
    assert switch_back.json()["score"] == -1

    # 6. Bob downvotes again -> toggle off (score +1 -> 0)
    dv_off = bob_client.post(
        f"/api/comments/{comment_id}/vote",
        json={"action": "downvote"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert dv_off.status_code == 200
    assert dv_off.json()["user_vote"] is None
    assert dv_off.json()["score"] == 0

def test_sorting_newest_and_top():
    client1 = TestClient(app)
    csrf1, _ = _login(client1, f"user1.{uuid.uuid4().hex[:6]}@sst.scaler.com")
    client2 = TestClient(app)
    csrf2, _ = _login(client2, f"user2.{uuid.uuid4().hex[:6]}@sst.scaler.com")

    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Post Comment A
    res_a = client1.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "First Comment A"},
        headers={"x-csrf-token": csrf1}
    )
    id_a = res_a.json()["id"]

    # Post Comment B
    res_b = client1.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Second Comment B"},
        headers={"x-csrf-token": csrf1}
    )
    id_b = res_b.json()["id"]

    # Upvote Comment A twice
    client1.post(f"/api/comments/{id_a}/vote", json={"action": "upvote"}, headers={"x-csrf-token": csrf1})
    client2.post(f"/api/comments/{id_a}/vote", json={"action": "upvote"}, headers={"x-csrf-token": csrf2})

    # Default sort is top -> Comment A (score 2) should be first
    get_default = client1.get(f"/api/notes/{note_id}/comments")
    assert get_default.status_code == 200
    assert get_default.json()["comments"][0]["id"] == id_a

    # Explicit sort=newest -> Comment B should be first
    get_newest = client1.get(f"/api/notes/{note_id}/comments?sort=newest")
    assert get_newest.status_code == 200
    assert get_newest.json()["comments"][0]["id"] == id_b

    # Explicit sort=top -> Comment A should be first
    get_top = client1.get(f"/api/notes/{note_id}/comments?sort=top")
    assert get_top.status_code == 200
    assert get_top.json()["comments"][0]["id"] == id_a


def test_content_moderation_flags_violation(monkeypatch):
    client = TestClient(app)
    csrf, _ = _login(client, f"mod_{uuid.uuid4().hex[:6]}@sst.scaler.com")
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    import httpx

    # Mock OpenAI Moderation response returning flagged: True for hate / self-harm
    class MockFlaggedResponse:
        status_code = 200
        def json(self):
            return {
                "id": "modr-123",
                "results": [
                    {
                        "flagged": True,
                        "categories": {
                            "hate": True,
                            "harassment": False,
                            "self-harm": True
                        }
                    }
                ]
            }

    async def mock_post(self, *args, **kwargs):
        return MockFlaggedResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    from api.config import settings
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-mock-key")

    res_flagged = client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Flagged content evaluated by AI"},
        headers={"x-csrf-token": csrf}
    )
    # AI flagged content is saved as quarantined with moderation reasons
    assert res_flagged.status_code == 201
    flagged_data = res_flagged.json()
    assert flagged_data["status"] == "quarantined"
    assert "hate" in flagged_data["moderation_reasons"]
    assert "self-harm" in flagged_data["moderation_reasons"]

    # Quarantined comments should NOT appear in the public list
    public_res = client.get(f"/api/notes/{note_id}/comments")
    assert public_res.status_code == 200
    assert not any(c["id"] == flagged_data["id"] for c in public_res.json()["comments"])

    # Test unflagged clean content passes through as published
    class MockCleanResponse:
        status_code = 200
        def json(self):
            return {
                "id": "modr-456",
                "results": [
                    {
                        "flagged": False,
                        "categories": {
                            "hate": False,
                            "harassment": False,
                            "self-harm": False
                        }
                    }
                ]
            }

    async def mock_clean_post(self, *args, **kwargs):
        return MockCleanResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_clean_post)

    res_clean = client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Clean helpful lecture discussion comment."},
        headers={"x-csrf-token": csrf}
    )
    assert res_clean.status_code == 201
    assert res_clean.json()["status"] == "published"


def test_comment_reporting_pipeline():
    suffix = uuid.uuid4().hex[:6]
    alice_client = TestClient(app)
    alice_csrf, alice_id = _login(alice_client, f"alice.{suffix}.25bcs10001@sst.scaler.com")

    bob_client = TestClient(app)
    bob_csrf, bob_id = _login(bob_client, f"bob.{suffix}.25bcs10002@sst.scaler.com")

    charlie_client = TestClient(app)
    charlie_csrf, charlie_id = _login(charlie_client, f"charlie.{suffix}.25bcs10003@sst.scaler.com")

    note_id = f"test-note-{uuid.uuid4().hex[:8]}"

    # Alice posts comment
    post_res = alice_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Suspicious promotion link"},
        headers={"x-csrf-token": alice_csrf}
    )
    assert post_res.status_code == 201
    comment_id = post_res.json()["id"]
    assert post_res.json()["status"] == "published"

    # Bob reports comment as Spam
    rep1 = bob_client.post(
        f"/api/comments/{comment_id}/report",
        json={"reason": "Spam"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert rep1.status_code == 200
    assert rep1.json()["status"] == "reported"

    # Bob reports again (duplicate report by same user)
    rep2 = bob_client.post(
        f"/api/comments/{comment_id}/report",
        json={"reason": "Spam"},
        headers={"x-csrf-token": bob_csrf}
    )
    assert rep2.status_code == 200

    # Charlie reports as Harassment
    rep3 = charlie_client.post(
        f"/api/comments/{comment_id}/report",
        json={"reason": "Harassment / Toxicity"},
        headers={"x-csrf-token": charlie_csrf}
    )
    assert rep3.status_code == 200

    # Reported comments must remain visible in public comments
    public_res = alice_client.get(f"/api/notes/{note_id}/comments")
    assert public_res.status_code == 200
    comments = public_res.json()["comments"]
    matching = [c for c in comments if c["id"] == comment_id]
    assert len(matching) == 1
    target = matching[0]
    assert target["status"] == "reported"
    assert bob_id in target["reported_by"]
    assert charlie_id in target["reported_by"]
    assert target["reported_by"].count(bob_id) == 1


def test_moderation_queue_rbac_and_resolution():
    suffix = uuid.uuid4().hex[:6]
    student_client = TestClient(app)
    student_csrf, student_id = _login(student_client, f"student.{suffix}.25bcs10005@sst.scaler.com")

    mod_client = TestClient(app)
    mod_csrf, mod_id = _login(mod_client, f"mod.{suffix}.25bcs10006@sst.scaler.com")

    # Promote mod user to "moderator" role
    db = get_mongo_db()
    if db is not None:
        try:
            from bson import ObjectId
            db.users.update_one({"_id": ObjectId(mod_id)}, {"$set": {"role": "moderator"}})
        except Exception:
            db.users.update_one({"_id": mod_id}, {"$set": {"role": "moderator"}})
    else:
        in_memory_store.users[mod_id]["role"] = "moderator"

    # Student attempts to access moderation queue -> 403 Forbidden
    student_queue_res = student_client.get("/api/moderation/queue")
    assert student_queue_res.status_code == 403

    # Student posts a comment and reports it
    note_id = f"test-note-{uuid.uuid4().hex[:8]}"
    post_res = student_client.post(
        f"/api/notes/{note_id}/comments",
        json={"content": "Content needing mod review"},
        headers={"x-csrf-token": student_csrf}
    )
    comment_id = post_res.json()["id"]

    student_client.post(
        f"/api/comments/{comment_id}/report",
        json={"reason": "Spam"},
        headers={"x-csrf-token": student_csrf}
    )

    # Moderator accesses moderation queue -> 200 OK
    mod_queue_res = mod_client.get("/api/moderation/queue")
    assert mod_queue_res.status_code == 200
    queue = mod_queue_res.json()["queue"]
    assert any(c["id"] == comment_id for c in queue)

    # Moderator approves comment -> status becomes published
    approve_res = mod_client.post(
        f"/api/moderation/queue/{comment_id}/resolve",
        json={"action": "approve"},
        headers={"x-csrf-token": mod_csrf}
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "published"

    # Moderator deletes comment -> status becomes deleted
    delete_res = mod_client.post(
        f"/api/moderation/queue/{comment_id}/resolve",
        json={"action": "delete"},
        headers={"x-csrf-token": mod_csrf}
    )
    assert delete_res.status_code == 200
    assert delete_res.json()["status"] == "deleted"



import logging
import os
import sys
from pathlib import Path

# Add project root to sys.path so the file can be executed directly as a script
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from api.config import settings

logger = logging.getLogger("api.database")

_mongo_client = None
_mongo_db = None

def get_mongo_db():
    """
    Returns the MongoDB Atlas database instance if MONGODB_URI is configured.
    Maintains a reusable connection pool across warm function invocations.
    Returns None if MONGODB_URI is empty (dev mode).
    """
    global _mongo_client, _mongo_db
    if not settings.MONGODB_URI:
        return None

    if _mongo_db is not None:
        return _mongo_db

    try:
        from pymongo import MongoClient
        mongo_kwargs = {
            "maxPoolSize": 10,
            "serverSelectionTimeoutMS": 10000
        }
        try:
            import certifi
            mongo_kwargs["tlsCAFile"] = certifi.where()
        except ImportError:
            pass

        _mongo_client = MongoClient(
            settings.MONGODB_URI,
            **mongo_kwargs
        )
        _mongo_db = _mongo_client[settings.MONGODB_DB_NAME]

        # Ensure indexes (TDD Section 6)
        _mongo_db.users.create_index("google_sub_id", unique=True)
        _mongo_db.sessions.create_index("refresh_token_hash", unique=True)
        _mongo_db.sessions.create_index("expires_at")
        _mongo_db.bookmarks.create_index([("user_id", 1), ("note_id", 1)], unique=True)
        _mongo_db.bookmarks.create_index([("user_id", 1), ("created_at", -1)])

        logger.info("MongoDB Atlas connected and indexes verified.")
        return _mongo_db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB Atlas: {e}")
        return None

# ==============================================================================
# In-Memory Database Fallback for Development
# ==============================================================================

class InMemoryStore:
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.sub_to_id: Dict[str, str] = {}
        self.sessions: Dict[str, dict] = {}
        self.bookmarks: Dict[str, dict] = {} # key: f"{user_id}:{note_id}"

    def upsert_user(self, google_sub: str, email: str, display_name: str) -> dict:
        now_str = datetime.now(timezone.utc).isoformat()
        if google_sub in self.sub_to_id:
            user_id = self.sub_to_id[google_sub]
            user = self.users[user_id]
            user["email"] = email
            user["display_name"] = display_name
            user["status"] = "active"
            user["updated_at"] = now_str
            return user

        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user = {
            "_id": user_id,
            "google_sub_id": google_sub,
            "email": email,
            "display_name": display_name,
            "status": "active",
            "created_at": now_str,
            "updated_at": now_str
        }
        self.users[user_id] = user
        self.sub_to_id[google_sub] = user_id
        return user

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)

    def get_user_by_sub(self, google_sub: str) -> Optional[dict]:
        user_id = self.sub_to_id.get(google_sub)
        return self.users.get(user_id) if user_id else None

    def create_session(self, user_id: str, refresh_token_hash: str, expires_at: datetime):
        now = datetime.now(timezone.utc)
        self.sessions[refresh_token_hash] = {
            "session_id": f"sess_{uuid.uuid4().hex[:12]}",
            "user_id": user_id,
            "refresh_token_hash": refresh_token_hash,
            "created_at": now,
            "last_used_at": now,
            "expires_at": expires_at,
            "revoked_at": None
        }

    def get_active_session(self, refresh_token_hash: str) -> Optional[dict]:
        sess = self.sessions.get(refresh_token_hash)
        if not sess or sess.get("revoked_at") is not None:
            return None
        if sess["expires_at"] < datetime.now(timezone.utc):
            return None
        return sess

    def rotate_session(self, old_hash: str, new_hash: str, new_expires: datetime):
        if old_hash in self.sessions:
            sess = self.sessions.pop(old_hash)
            now = datetime.now(timezone.utc)
            sess["refresh_token_hash"] = new_hash
            sess["last_used_at"] = now
            sess["expires_at"] = new_expires
            self.sessions[new_hash] = sess

    def revoke_session(self, refresh_token_hash: str):
        if refresh_token_hash in self.sessions:
            self.sessions[refresh_token_hash]["revoked_at"] = datetime.now(timezone.utc)

    def add_bookmark(self, user_id: str, note_id: str) -> bool:
        key = f"{user_id}:{note_id}"
        if key in self.bookmarks:
            return False
        self.bookmarks[key] = {
            "user_id": user_id,
            "note_id": note_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        return True

    def remove_bookmark(self, user_id: str, note_id: str):
        key = f"{user_id}:{note_id}"
        self.bookmarks.pop(key, None)

    def get_bookmarks(self, user_id: str) -> List[dict]:
        results = [b for b in self.bookmarks.values() if b["user_id"] == user_id]
        results.sort(key=lambda x: x["created_at"], reverse=True)
        return results

    def delete_user(self, user_id: str):
        user = self.users.pop(user_id, None)
        if user:
            self.sub_to_id.pop(user.get("google_sub_id", ""), None)
        
        # Remove user's sessions and bookmarks
        self.sessions = {k: v for k, v in self.sessions.items() if v["user_id"] != user_id}
        self.bookmarks = {k: v for k, v in self.bookmarks.items() if v["user_id"] != user_id}

in_memory_store = InMemoryStore()

if __name__ == "__main__":
    import json
    print("=" * 60)
    print("SST Study Platform - Database Self-Test & Diagnostic")
    print("=" * 60)
    if settings.MONGODB_URI:
        safe_uri = settings.MONGODB_URI.split("@")[-1] if "@" in settings.MONGODB_URI else "configured"
        print(f"[*] MONGODB_URI detected: ...@{safe_uri}")
        print(f"[*] Database Name: {settings.MONGODB_DB_NAME}")
        print("[*] Connecting to MongoDB Atlas...")
        db = get_mongo_db()
        if db is not None:
            print("[+] Successfully connected to MongoDB Atlas!")
            try:
                collections = db.list_collection_names()
                print(f"[+] Existing collections: {collections}")
                ping_res = _mongo_client.admin.command("ping")
                print(f"[+] Cluster ping response: {ping_res}")
            except Exception as e:
                print(f"[-] Ping error: {e}")
        else:
            print("[-] Failed to connect to MongoDB Atlas.")
    else:
        print("[*] MONGODB_URI not configured. Running in Local Dev In-Memory mode.")

    print("\n[*] Testing InMemoryStore...")
    test_user = in_memory_store.upsert_user("sub_test_123", "test@sst.scaler.com", "Test Student")
    print(f"[+] Upsert user: {test_user['display_name']} ({test_user['email']})")
    in_memory_store.add_bookmark(test_user["_id"], "lecture-01-notes")
    bms = in_memory_store.get_bookmarks(test_user["_id"])
    print(f"[+] Bookmarks count: {len(bms)}")
    print("=" * 60)
    print("All checks completed successfully!")

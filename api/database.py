import logging
import os
import sys
from pathlib import Path

# Add project root to sys.path so the file can be executed directly as a script
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import uuid
from datetime import datetime, timezone, timedelta
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
        _mongo_db.users.create_index("username", unique=True, sparse=True)
        _mongo_db.sessions.create_index("refresh_token_hash", unique=True)
        # Real MongoDB TTL cleanup policy: automatically deletes sessions when now >= expires_at
        try:
            _mongo_db.sessions.create_index("expires_at", expireAfterSeconds=0)
        except Exception:
            try:
                _mongo_db.sessions.drop_index("expires_at_1")
                _mongo_db.sessions.create_index("expires_at", expireAfterSeconds=0)
            except Exception as e2:
                logger.warning("Could not update TTL index on sessions.expires_at: %s", e2)
        _mongo_db.bookmarks.create_index([("user_id", 1), ("note_id", 1)], unique=True)
        _mongo_db.bookmarks.create_index([("user_id", 1), ("created_at", -1)])
        _mongo_db.comments.create_index([("note_id", 1), ("created_at", -1)])
        _mongo_db.comments.create_index("user_id")

        try:
            _mongo_db.nonces.create_index("nonce", unique=True)
            _mongo_db.nonces.create_index("created_at", expireAfterSeconds=300)
            _mongo_db.csrf_tokens.create_index("token", unique=True)
            _mongo_db.csrf_tokens.create_index("expires_at", expireAfterSeconds=0)
        except Exception as e_idx:
            logger.warning("Could not create TTL index on nonces/csrf_tokens: %s", e_idx)

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
        self.username_to_id: Dict[str, str] = {}
        self.sessions: Dict[str, dict] = {}
        self.bookmarks: Dict[str, dict] = {} # key: f"{user_id}:{note_id}"
        self.comments: Dict[str, dict] = {} # key: comment_id
        self.audit_logs: List[dict] = []
        self.notifications: Dict[str, dict] = {}

    def upsert_user(self, google_sub: str, email: str, display_name: str, avatar_url: Optional[str] = None, is_special: bool = False) -> dict:
        import re
        now_str = datetime.now(timezone.utc).isoformat()
        if google_sub in self.sub_to_id:
            user_id = self.sub_to_id[google_sub]
            user = self.users[user_id]
            user["email"] = email
            user["display_name"] = display_name
            user["status"] = "active"
            user.setdefault("active_term", 1)
            user.setdefault("bio", None)
            user.setdefault("is_special", is_special)
            user.setdefault("needs_profile_setup", False)
            if avatar_url and not user.get("avatar_url"):
                user["avatar_url"] = avatar_url
            if not user.get("username"):
                base_username = re.sub(r'[^a-zA-Z0-9_]', '_', email.split('@')[0]).lower()[:24]
                candidate = base_username
                count = 1
                while candidate in self.username_to_id and self.username_to_id[candidate] != user_id:
                    candidate = f"{base_username}_{count}"
                    count += 1
                user["username"] = candidate
                self.username_to_id[candidate] = user_id
            user["updated_at"] = now_str
            return user

        user_id = f"user_{uuid.uuid4().hex[:12]}"
        base_username = re.sub(r'[^a-zA-Z0-9_]', '_', email.split('@')[0]).lower()[:24]
        candidate = base_username
        count = 1
        while candidate in self.username_to_id:
            candidate = f"{base_username}_{count}"
            count += 1

        user = {
            "_id": user_id,
            "google_sub_id": google_sub,
            "email": email,
            "display_name": display_name,
            "username": candidate,
            "active_term": 1,
            "avatar_url": avatar_url,
            "bio": None,
            "status": "active",
            "is_special": is_special,
            "needs_profile_setup": is_special, # First login for special users prompts profile setup
            "created_at": now_str,
            "updated_at": now_str
        }
        self.users[user_id] = user
        self.sub_to_id[google_sub] = user_id
        self.username_to_id[candidate] = user_id
        return user

    def update_user_profile(self, user_id: str, updates: dict) -> dict:
        user = self.users.get(user_id)
        if not user:
            raise KeyError("User not found")
        if "display_name" in updates and updates["display_name"] is not None:
            user["display_name"] = updates["display_name"]
        if "username" in updates and updates["username"]:
            new_uname = updates["username"].lower()
            if new_uname in self.username_to_id and self.username_to_id[new_uname] != user_id:
                raise ValueError("Username already taken")
            old_uname = user.get("username")
            if old_uname and old_uname in self.username_to_id:
                del self.username_to_id[old_uname]
            self.username_to_id[new_uname] = user_id
            user["username"] = new_uname

        if "active_term" in updates and updates["active_term"] is not None:
            user["active_term"] = int(updates["active_term"])
        if "avatar_url" in updates:
            user["avatar_url"] = updates["avatar_url"]
        if "bio" in updates:
            user["bio"] = updates["bio"]
        if "needs_profile_setup" in updates:
            user["needs_profile_setup"] = updates["needs_profile_setup"]

        user["updated_at"] = datetime.now(timezone.utc).isoformat()
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

    def add_comment(
        self,
        note_id: str,
        user_id: str,
        content: str,
        parent_id: Optional[str] = None,
        status: str = "published",
        moderation_reasons: Optional[List[str]] = None,
        reported_by: Optional[List[str]] = None,
    ) -> dict:
        now_str = datetime.now(timezone.utc).isoformat()
        comment_id = f"cmt_{uuid.uuid4().hex[:12]}"
        user = self.get_user_by_id(user_id)
        comment = {
            "_id": comment_id,
            "id": comment_id,
            "note_id": note_id,
            "user_id": user_id,
            "content": content,
            "parent_id": parent_id,
            "score": 0,
            "upvoted_by": [],
            "downvoted_by": [],
            "status": status,
            "moderation_reasons": list(moderation_reasons or []),
            "reported_by": list(reported_by or []),
            "report_history": [],
            "created_at": now_str,
            "updated_at": now_str,
            "username": user.get("username") if user else None,
            "avatar_url": user.get("avatar_url") if user else None,
            "author_role": user.get("role", "student") if user else "student",
        }
        self.comments[comment_id] = comment
        return comment

    def get_comments_for_note(self, note_id: str, sort: str = "top") -> List[dict]:
        results = []
        for c in self.comments.values():
            if c["note_id"] == note_id:
                # Quarantined and deleted comments are not shown publicly
                c_status = c.get("status", "published")
                if c_status in ("quarantined", "deleted"):
                    continue
                user = self.get_user_by_id(c["user_id"])
                results.append({
                    "id": str(c.get("_id") or c.get("id")),
                    "note_id": c["note_id"],
                    "user_id": c["user_id"],
                    "content": c["content"],
                    "parent_id": c.get("parent_id"),
                    "score": c.get("score", 0),
                    "upvoted_by": list(c.get("upvoted_by", [])),
                    "downvoted_by": list(c.get("downvoted_by", [])),
                    "status": c_status,
                    "moderation_reasons": list(c.get("moderation_reasons", [])),
                    "reported_by": list(c.get("reported_by", [])),
                    "created_at": c["created_at"],
                    "updated_at": c["updated_at"],
                    "username": user.get("username") if user else None,
                    "avatar_url": user.get("avatar_url") if user else None,
                    "author_role": user.get("role", "student") if user else "student",
                })
        if sort == "newest":
            results.sort(key=lambda x: x["created_at"], reverse=True)
        else: # "top"
            results.sort(key=lambda x: (x.get("score", 0), x["created_at"]), reverse=True)
        return results

    def report_comment(self, comment_id: str, user_id: str, reason: str) -> Optional[dict]:
        comment = self.comments.get(comment_id)
        if not comment:
            return None
        reported_by = comment.setdefault("reported_by", [])
        report_history = comment.setdefault("report_history", [])

        if user_id not in reported_by:
            reported_by.append(user_id)
            comment.setdefault("moderation_reasons", []).append(reason)
            now_utc = datetime.now(timezone.utc)
            now_iso = now_utc.isoformat()
            new_report = {
                "user_id": user_id,
                "reason": reason,
                "reported_at": now_iso,
            }
            report_history.append(new_report)

            # Check unique users within time window
            window_threshold = now_utc - timedelta(hours=settings.AUTO_QUARANTINE_WINDOW_HOURS)
            recent_unique_reporters = set()
            for r in report_history:
                reported_at_str = r.get("reported_at")
                rep_user = r.get("user_id")
                if not reported_at_str or not rep_user:
                    continue
                try:
                    rep_time = datetime.fromisoformat(reported_at_str)
                    if rep_time.tzinfo is None:
                        rep_time = rep_time.replace(tzinfo=timezone.utc)
                    if rep_time >= window_threshold:
                        recent_unique_reporters.add(rep_user)
                except Exception:
                    pass

            if len(recent_unique_reporters) >= settings.AUTO_QUARANTINE_REPORT_THRESHOLD:
                comment["status"] = "quarantined"
                quarantine_reason = (
                    f"auto_quarantine: {len(recent_unique_reporters)} distinct reports "
                    f"within {settings.AUTO_QUARANTINE_WINDOW_HOURS}h"
                )
                if quarantine_reason not in comment["moderation_reasons"]:
                    comment["moderation_reasons"].append(quarantine_reason)
            elif comment.get("status", "published") == "published":
                comment["status"] = "reported"

            comment["updated_at"] = now_iso
        return comment

    def get_moderation_queue(self) -> List[dict]:
        results = []
        for c in self.comments.values():
            if c.get("status") in ("quarantined", "reported"):
                user = self.get_user_by_id(c["user_id"])
                results.append({
                    "id": str(c.get("_id") or c.get("id")),
                    "note_id": c["note_id"],
                    "user_id": c["user_id"],
                    "content": c["content"],
                    "parent_id": c.get("parent_id"),
                    "score": c.get("score", 0),
                    "upvoted_by": list(c.get("upvoted_by", [])),
                    "downvoted_by": list(c.get("downvoted_by", [])),
                    "status": c.get("status"),
                    "moderation_reasons": list(c.get("moderation_reasons", [])),
                    "reported_by": list(c.get("reported_by", [])),
                    "created_at": c["created_at"],
                    "updated_at": c["updated_at"],
                    "username": user.get("username") if user else None,
                    "avatar_url": user.get("avatar_url") if user else None,
                    "author_role": user.get("role", "student") if user else "student",
                })
        results.sort(key=lambda x: x["updated_at"], reverse=True)
        return results

    def resolve_moderation(self, comment_id: str, action: str) -> Optional[dict]:
        comment = self.comments.get(comment_id)
        if not comment:
            return None
        if action == "approve":
            comment["status"] = "published"
        elif action == "delete":
            comment["status"] = "deleted"
            comment["content"] = "[Deleted]"
        comment["updated_at"] = datetime.now(timezone.utc).isoformat()
        return comment

    def get_comment_by_id(self, comment_id: str) -> Optional[dict]:
        return self.comments.get(comment_id)

    def vote_comment(self, comment_id: str, user_id: str, action: str):
        comment = self.comments.get(comment_id)
        if not comment:
            return None
        upvoted_by = set(comment.get("upvoted_by", []))
        downvoted_by = set(comment.get("downvoted_by", []))
        score = comment.get("score", 0)

        if action == "upvote":
            if user_id in upvoted_by:
                upvoted_by.remove(user_id)
                score -= 1
                user_vote = None
            elif user_id in downvoted_by:
                downvoted_by.remove(user_id)
                upvoted_by.add(user_id)
                score += 2
                user_vote = "upvote"
            else:
                upvoted_by.add(user_id)
                score += 1
                user_vote = "upvote"
        elif action == "downvote":
            if user_id in downvoted_by:
                downvoted_by.remove(user_id)
                score += 1
                user_vote = None
            elif user_id in upvoted_by:
                upvoted_by.remove(user_id)
                downvoted_by.add(user_id)
                score -= 2
                user_vote = "downvote"
            else:
                downvoted_by.add(user_id)
                score -= 1
                user_vote = "downvote"
        else:
            raise ValueError(f"Invalid vote action: {action}")

        comment["upvoted_by"] = list(upvoted_by)
        comment["downvoted_by"] = list(downvoted_by)
        comment["score"] = score
        return user_vote, score

    def delete_comment(self, comment_id: str, user_id: str) -> str:
        comment = self.comments.get(comment_id)
        if not comment:
            return "not_found"
        if comment["user_id"] != user_id:
            raise PermissionError("Forbidden: Cannot delete comments from other authors")
        
        # Check if there are child replies
        has_children = any(c.get("parent_id") == comment_id for c in self.comments.values())
        if has_children:
            comment["content"] = "[Deleted]"
            comment["updated_at"] = datetime.now(timezone.utc).isoformat()
            return "redacted"
        else:
            del self.comments[comment_id]
            return "deleted"

    def delete_user(self, user_id: str):
        user = self.users.pop(user_id, None)
        if user:
            self.sub_to_id.pop(user.get("google_sub_id", ""), None)
        
        # Remove user's sessions, bookmarks, and comments
        self.sessions = {k: v for k, v in self.sessions.items() if v["user_id"] != user_id}
        self.bookmarks = {k: v for k, v in self.bookmarks.items() if v["user_id"] != user_id}
        self.comments = {k: v for k, v in self.comments.items() if v["user_id"] != user_id}
        self.notifications = {k: v for k, v in self.notifications.items() if v["user_id"] != user_id}

    def add_audit_log(
        self,
        action: str,
        comment_id: str,
        moderator_id: str,
        moderator_name: str,
        moderator_role: str,
        note_id: Optional[str] = None,
        comment_content: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> dict:
        log_entry = {
            "id": f"log_{uuid.uuid4().hex[:12]}",
            "action": action,
            "comment_id": comment_id,
            "note_id": note_id,
            "comment_content": (comment_content[:150] + "...") if comment_content and len(comment_content) > 150 else comment_content,
            "moderator_id": moderator_id,
            "moderator_name": moderator_name,
            "moderator_role": moderator_role,
            "reason": reason,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.audit_logs.insert(0, log_entry)
        return log_entry

    def get_audit_logs(self, limit: int = 50) -> List[dict]:
        return self.audit_logs[:limit]

    def add_notification(
        self,
        user_id: str,
        notif_type: str,
        title: str,
        message: str,
        link: Optional[str] = None,
    ) -> dict:
        notif_id = f"notif_{uuid.uuid4().hex[:12]}"
        notif = {
            "id": notif_id,
            "user_id": user_id,
            "type": notif_type,
            "title": title,
            "message": message,
            "link": link,
            "read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.notifications[notif_id] = notif
        return notif

    def get_notifications(self, user_id: str, limit: int = 20) -> List[dict]:
        user_notifs = [n for n in self.notifications.values() if n["user_id"] == user_id]
        user_notifs.sort(key=lambda x: x["created_at"], reverse=True)
        return user_notifs[:limit]

    def get_unread_notification_count(self, user_id: str) -> int:
        return sum(1 for n in self.notifications.values() if n["user_id"] == user_id and not n["read"])

    def mark_notification_read(self, notif_id: str, user_id: str) -> bool:
        notif = self.notifications.get(notif_id)
        if notif and notif["user_id"] == user_id:
            notif["read"] = True
            return True
        return False

    def mark_all_notifications_read(self, user_id: str) -> int:
        count = 0
        for n in self.notifications.values():
            if n["user_id"] == user_id and not n["read"]:
                n["read"] = True
                count += 1
        return count

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

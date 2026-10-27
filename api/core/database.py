import logging
import os
import sys
import re
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from api.core.config import settings

logger = logging.getLogger("api.core.database")

_mongo_client = None
_mongo_db = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = PROJECT_ROOT / "content" / "fixtures"


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

        # Ensure indexes
        _mongo_db.users.create_index("google_sub_id", unique=True)
        _mongo_db.users.create_index("username", unique=True, sparse=True)
        _mongo_db.sessions.create_index("refresh_token_hash", unique=True)
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
        _mongo_db.scratchpads.create_index([("user_id", 1), ("note_id", 1)], unique=True)
        _mongo_db.quiz_attempts.create_index([("user_id", 1), ("note_id", 1)], unique=True)

        # Notes collection indexes (Phase 2 requirement)
        _mongo_db.notes.create_index("note_id", unique=True)
        _mongo_db.notes.create_index([("approval_status", 1), ("term_number", 1), ("subject_code", 1)])

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
# In-Memory Database Fallback for Development & Offline Mode
# ==============================================================================

class InMemoryStore:
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.sub_to_id: Dict[str, str] = {}
        self.username_to_id: Dict[str, str] = {}
        self.sessions: Dict[str, dict] = {}
        self.bookmarks: Dict[str, dict] = {}       # key: f"{user_id}:{note_id}"
        self.comments: Dict[str, dict] = {}        # key: comment_id
        self.scratchpads: Dict[str, dict] = {}     # key: f"{user_id}:{note_id}"
        self.audit_logs: List[dict] = []
        self.notifications: Dict[str, dict] = {}
        self.quiz_attempts: Dict[str, dict] = {}   # key: f"{user_id}:{note_id}"
        self.notes: Dict[str, dict] = {}           # key: note_id

    # ---------------------------------------------------------------------------
    # Notes Persistence (Phase 2 Parity)
    # ---------------------------------------------------------------------------
    def get_note(self, note_id: str) -> Optional[dict]:
        return self.notes.get(note_id)

    def list_notes(
        self,
        max_allowed_term: Optional[int] = None,
        include_drafts: bool = False
    ) -> List[dict]:
        results = []
        for note in self.notes.values():
            status = note.get("approval_status", "approved")
            if not include_drafts and status != "approved":
                continue
            term_num = note.get("term_number", 1)
            if max_allowed_term is not None and term_num > max_allowed_term:
                continue
            # Lightweight projection (exclude sections and quiz)
            lightweight = {
                "schema_version": note.get("schema_version", 1),
                "note_id": note["note_id"],
                "term": note.get("term", f"Term {term_num}"),
                "term_number": term_num,
                "subject_code": note.get("subject_code", ""),
                "topic_title": note.get("topic_title", ""),
                "tags": note.get("tags", []),
                "learning_objectives": note.get("learning_objectives", []),
                "summary": note.get("summary", ""),
                "key_takeaways": note.get("key_takeaways", []),
                "last_updated": note.get("last_updated", ""),
                "approval_status": status,
            }
            results.append(lightweight)

        results.sort(key=lambda x: (x["term_number"], x["subject_code"], x["note_id"]))
        return results

    def save_note(self, note_data: dict) -> dict:
        note_id = note_data["note_id"]
        if "term_number" not in note_data or not note_data["term_number"]:
            term = note_data.get("term", "")
            match = re.search(r'(\d+)', str(term))
            note_data["term_number"] = int(match.group(1)) if match else 1

        self.notes[note_id] = note_data
        return note_data

    def delete_note(self, note_id: str) -> bool:
        if note_id in self.notes:
            del self.notes[note_id]
            return True
        return False

    # ---------------------------------------------------------------------------
    # User Profile & Accounts
    # ---------------------------------------------------------------------------
    def upsert_user(
        self,
        google_sub: str,
        email: str,
        display_name: str,
        avatar_url: Optional[str] = None,
        is_special: bool = False
    ) -> dict:
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
            "role": "admin" if (is_special or is_special_email(email)) else "student",
            "active_term": 1,
            "avatar_url": avatar_url,
            "bio": None,
            "status": "active",
            "is_special": is_special,
            "needs_profile_setup": is_special,
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

    def delete_user(self, user_id: str):
        if user_id in self.users:
            user = self.users[user_id]
            google_sub_id = user.get("google_sub_id")
            if google_sub_id and google_sub_id in self.sub_to_id:
                del self.sub_to_id[google_sub_id]
            uname = user.get("username")
            if uname and uname in self.username_to_id:
                del self.username_to_id[uname]
            del self.users[user_id]

            self.sessions = {k: v for k, v in self.sessions.items() if v.get("user_id") != user_id}
            self.bookmarks = {k: v for k, v in self.bookmarks.items() if not k.startswith(f"{user_id}:")}
            self.scratchpads = {k: v for k, v in self.scratchpads.items() if not k.startswith(f"{user_id}:")}
            self.quiz_attempts = {k: v for k, v in self.quiz_attempts.items() if not k.startswith(f"{user_id}:")}

    # ---------------------------------------------------------------------------
    # Sessions & Bookmarks
    # ---------------------------------------------------------------------------
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

    def save_session(self, user_id: str, refresh_token_hash: str, expires_at: datetime):
        self.create_session(user_id, refresh_token_hash, expires_at)

    def get_session(self, refresh_token_hash: str) -> Optional[dict]:
        return self.get_active_session(refresh_token_hash)

    def delete_session(self, refresh_token_hash: str):
        self.revoke_session(refresh_token_hash)

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
        prefix = f"{user_id}:"
        items = [v for k, v in self.bookmarks.items() if k.startswith(prefix)]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return items

    # ---------------------------------------------------------------------------
    # Comments & Moderation
    # ---------------------------------------------------------------------------
    def add_comment(
        self,
        note_id: str,
        user_id: str,
        content: str,
        parent_id: Optional[str] = None,
        status: str = "published",
        moderation_reasons: Optional[List[str]] = None,
        reported_by: Optional[List[str]] = None,
        **kwargs
    ) -> dict:
        comment_id = f"comm_{uuid.uuid4().hex[:12]}"
        now_str = datetime.now(timezone.utc).isoformat()
        author = self.get_user_by_id(user_id) or {}
        author_role = author.get("role", "student")

        comment = {
            "id": comment_id,
            "_id": comment_id,
            "note_id": note_id,
            "user_id": user_id,
            "content": content,
            "parent_id": parent_id,
            "score": 0,
            "upvoted_by": [],
            "downvoted_by": [],
            "status": status,
            "moderation_reasons": moderation_reasons or [],
            "reported_by": [],
            "report_history": [],
            "created_at": now_str,
            "updated_at": now_str,
            "username": author.get("username"),
            "avatar_url": author.get("avatar_url"),
            "author_role": author_role,
        }
        self.comments[comment_id] = comment
        return comment

    def get_comments(self, note_id: str, include_quarantined: bool = False) -> List[dict]:
        results = []
        for c in self.comments.values():
            if c["note_id"] == note_id:
                if c["status"] in ("published", "reported"):
                    results.append(c)
                elif include_quarantined and c["status"] == "quarantined":
                    results.append(c)
        results.sort(key=lambda x: x["created_at"])
        return results

    def get_comment_by_id(self, comment_id: str) -> Optional[dict]:
        return self.comments.get(comment_id)

    def vote_comment(self, comment_id: str, user_id: str, action: str) -> dict:
        c = self.comments.get(comment_id)
        if not c:
            raise KeyError("Comment not found")

        upvoted = set(c.get("upvoted_by", []))
        downvoted = set(c.get("downvoted_by", []))

        if action == "upvote":
            if user_id in upvoted:
                upvoted.remove(user_id)
            else:
                upvoted.add(user_id)
                downvoted.discard(user_id)
        elif action == "downvote":
            if user_id in downvoted:
                downvoted.remove(user_id)
            else:
                downvoted.add(user_id)
                upvoted.discard(user_id)

        c["upvoted_by"] = list(upvoted)
        c["downvoted_by"] = list(downvoted)
        c["score"] = len(upvoted) - len(downvoted)
        c["updated_at"] = datetime.now(timezone.utc).isoformat()
        return c

    def delete_comment(self, comment_id: str, user_id: str, is_admin: bool = False) -> bool:
        c = self.comments.get(comment_id)
        if not c:
            return False
        if not is_admin and c["user_id"] != user_id:
            return False
        c["status"] = "deleted"
        c["content"] = "[This comment has been deleted]"
        c["updated_at"] = datetime.now(timezone.utc).isoformat()
        return True

    def report_comment(self, comment_id: str, user_id: str, reason: str) -> dict:
        c = self.comments.get(comment_id)
        if not c:
            raise KeyError("Comment not found")
        if user_id not in c.get("reported_by", []):
            c.setdefault("reported_by", []).append(user_id)
            c.setdefault("moderation_reasons", []).append(reason)
            now_str = datetime.now(timezone.utc).isoformat()
            c.setdefault("report_history", []).append({
                "user_id": user_id,
                "reason": reason,
                "reported_at": now_str
            })

            cutoff = datetime.now(timezone.utc) - timedelta(hours=settings.AUTO_QUARANTINE_WINDOW_HOURS)
            recent_count = 0
            for r in c.get("report_history", []):
                try:
                    r_dt = datetime.fromisoformat(r["reported_at"])
                    if r_dt.tzinfo is None:
                        r_dt = r_dt.replace(tzinfo=timezone.utc)
                    if r_dt >= cutoff:
                        recent_count += 1
                except Exception:
                    pass

            if recent_count >= settings.AUTO_QUARANTINE_REPORT_THRESHOLD:
                c["status"] = "quarantined"
            elif c["status"] == "published":
                c["status"] = "reported"

            c["updated_at"] = now_str
        return c

    def get_moderation_queue(self) -> List[dict]:
        return [c for c in self.comments.values() if c.get("status") in ("quarantined", "reported")]

    def resolve_moderation(self, comment_id: str, action: str) -> dict:
        c = self.comments.get(comment_id)
        if not c:
            raise KeyError("Comment not found")
        if action == "approve":
            c["status"] = "published"
            c["reported_by"] = []
            c["report_history"] = []
            c["moderation_reasons"] = []
        elif action == "delete":
            c["status"] = "deleted"
            c["content"] = "[This comment was removed by moderation]"
        c["updated_at"] = datetime.now(timezone.utc).isoformat()
        return c

    def add_audit_log(
        self,
        action: str,
        comment_id: str,
        moderator_id: str,
        moderator_name: str,
        moderator_role: str,
        note_id: Optional[str] = None,
        comment_content: Optional[str] = None,
        reason: Optional[str] = None
    ) -> dict:
        log_entry = {
            "id": f"audit_{uuid.uuid4().hex[:12]}",
            "action": action,
            "comment_id": comment_id,
            "note_id": note_id,
            "comment_content": (comment_content[:100] + "...") if comment_content and len(comment_content) > 100 else comment_content,
            "moderator_id": moderator_id,
            "moderator_name": moderator_name,
            "moderator_role": moderator_role,
            "reason": reason,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.audit_logs.insert(0, log_entry)
        return log_entry

    def get_audit_logs(self, limit: int = 50) -> List[dict]:
        return self.audit_logs[:limit]

    # ---------------------------------------------------------------------------
    # Notifications & Scratchpad & Quizzes
    # ---------------------------------------------------------------------------
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

    def get_scratchpad(self, user_id: str, note_id: str) -> Optional[dict]:
        key = f"{user_id}:{note_id}"
        return self.scratchpads.get(key)

    def save_scratchpad(self, user_id: str, note_id: str, content: str) -> dict:
        key = f"{user_id}:{note_id}"
        now_dt = datetime.now(timezone.utc)
        doc = {
            "id": f"scratch_{uuid.uuid4().hex[:12]}",
            "user_id": user_id,
            "note_id": note_id,
            "content": content,
            "updated_at": now_dt
        }
        self.scratchpads[key] = doc
        return doc

    def get_scratchpad_summary(self, user_id: str) -> List[str]:
        prefix = f"{user_id}:"
        note_ids = []
        for k, v in self.scratchpads.items():
            if k.startswith(prefix) and v.get("content", "").strip():
                note_ids.append(v["note_id"])
        return note_ids

    def get_quiz_attempt(self, user_id: str, note_id: str) -> Optional[dict]:
        key = f"{user_id}:{note_id}"
        return self.quiz_attempts.get(key)

    def save_quiz_attempt(self, user_id: str, note_id: str, data: dict) -> dict:
        key = f"{user_id}:{note_id}"
        now_str = datetime.now(timezone.utc).isoformat()
        doc = {
            "user_id": user_id,
            "note_id": note_id,
            "selected_answers": data.get("selected_answers", {}),
            "checked_questions": data.get("checked_questions", {}),
            "is_completed": data.get("is_completed", False),
            "score": data.get("score", 0),
            "total_questions": data.get("total_questions", 0),
            "percentage": data.get("percentage", 0),
            "updated_at": now_str,
        }
        self.quiz_attempts[key] = doc
        return doc

    def delete_quiz_attempt(self, user_id: str, note_id: str) -> bool:
        key = f"{user_id}:{note_id}"
        if key in self.quiz_attempts:
            del self.quiz_attempts[key]
            return True
        return False

    def get_user_quiz_stats(self, user_id: str) -> dict:
        user_attempts = [a for a in self.quiz_attempts.values() if a.get("user_id") == user_id]
        total_attempted = len(user_attempts)
        total_completed = sum(1 for a in user_attempts if a.get("is_completed"))
        total_questions = sum(a.get("total_questions", 0) for a in user_attempts)
        total_correct = sum(a.get("score", 0) for a in user_attempts)
        accuracy = round((total_correct / total_questions) * 100) if total_questions > 0 else 0
        return {
            "quizzes_attempted": total_attempted,
            "quizzes_completed": total_completed,
            "total_questions_answered": total_questions,
            "total_correct": total_correct,
            "accuracy": accuracy,
        }


in_memory_store = InMemoryStore()


# ==============================================================================
# Startup Seeder Function (Phase 2 Requirement)
# ==============================================================================

def seed_initial_notes(db=None) -> int:
    """
    Scans content/fixtures/**/*.json for all lecture notes.
    Seeds notes into in_memory_store (always, so offline dev has all notes immediately).
    If db is provided (MongoDB Atlas connected), performs UpdateOne upserts using
    $setOnInsert so existing database edits are preserved.
    Returns the total count of fixtures processed.
    """
    if not FIXTURES_DIR.exists():
        logger.warning(f"Fixtures directory {FIXTURES_DIR} does not exist.")
        return 0

    fixture_files = list(FIXTURES_DIR.glob("**/*.json"))
    if not fixture_files:
        logger.warning("No JSON fixtures found to seed.")
        return 0

    operations = []
    loaded_count = 0

    for fpath in fixture_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                note_data = json.load(f)

            note_id = note_data.get("note_id")
            if not note_id:
                continue

            if "term_number" not in note_data or not note_data["term_number"]:
                term = note_data.get("term", "")
                match = re.search(r'(\d+)', str(term))
                note_data["term_number"] = int(match.group(1)) if match else 1

            note_data.setdefault("schema_version", 1)
            note_data.setdefault("approval_status", "approved")

            in_memory_store.save_note(note_data)
            loaded_count += 1

            if db is not None:
                from pymongo import UpdateOne
                operations.append(
                    UpdateOne(
                        {"note_id": note_id},
                        {"$setOnInsert": note_data},
                        upsert=True
                    )
                )
        except Exception as exc:
            logger.error(f"Error parsing fixture {fpath}: {exc}")

    if db is not None and operations:
        try:
            res = db.notes.bulk_write(operations, ordered=False)
            logger.info(
                f"[Seeder] MongoDB Atlas notes seeded: {res.upserted_count} new notes inserted."
            )
        except Exception as exc:
            logger.error(f"[Seeder] MongoDB notes bulk_write failed: {exc}")

    logger.info(f"[Seeder] Seeded {loaded_count} lecture notes into InMemoryStore.")
    return loaded_count


# Auto-seed in_memory_store with fixtures upon module import
try:
    seed_initial_notes(None)
except Exception as _e_init:
    logger.warning("Could not auto-seed in_memory_store on import: %s", _e_init)

"""
Database cleanup script for SST Study Platform.
Safely removes all mock/test comments, test users, test sessions, notifications,
and moderation audit records from MongoDB Atlas while strictly preserving 'acca3402'.
"""

import os
import sys

# Auto-detect and switch to the installed project Python if run with an unconfigured interpreter
try:
    import pymongo
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    target_pythons = [
        r"C:\Users\Surya Rawat\AppData\Local\Programs\Python\Python312\python.exe",
        "python",
        "py -3.12"
    ]
    for py_bin in target_pythons:
        if py_bin != sys.executable:
            try:
                check = subprocess.run([py_bin, "-c", "import pymongo, dotenv"], capture_output=True, text=True)
                if check.returncode == 0:
                    res = subprocess.run([py_bin, __file__] + sys.argv[1:])
                    sys.exit(res.returncode)
            except Exception:
                continue

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.core.database import get_mongo_db


def clean_database(dry_run: bool = False):
    db = get_mongo_db()
    if db is None:
        print("[ERROR] Could not connect to MongoDB Atlas. Check MONGODB_URI in .env.")
        return

    print(f"Connected to MongoDB Atlas: {db.name}")

    # 1. Identify acca3402 user record
    acca_user = db.users.find_one({"email": "acca3402@gmail.com"})
    acca_id = str(acca_user["_id"]) if acca_user else None

    if acca_user:
        print(f"[PRESERVED] Found acca3402 user record (ID: {acca_id}). It will NOT be deleted.")
    else:
        print("[INFO] acca3402 has not created an entry in this DB yet. Protected rule is active.")

    # 2. Count items to delete
    comment_filter = {"user_id": {"$ne": acca_id}} if acca_id else {}
    comments_to_delete = db.comments.count_documents(comment_filter)

    user_filter = {"email": {"$ne": "acca3402@gmail.com"}}
    users_to_delete = db.users.count_documents(user_filter)

    session_filter = {"user_id": {"$ne": acca_id}} if acca_id else {}
    sessions_to_delete = db.sessions.count_documents(session_filter)

    notif_filter = {"user_id": {"$ne": acca_id}} if acca_id else {}
    notifs_to_delete = db.notifications.count_documents(notif_filter)

    logs_to_delete = db.moderation_logs.count_documents({})
    reports_to_delete = db.comment_reports.count_documents({})

    print("\n--- Items to be deleted ---")
    print(f"  Users:           {users_to_delete}")
    print(f"  Sessions:        {sessions_to_delete}")
    print(f"  Comments:        {comments_to_delete}")
    print(f"  Comment Reports: {reports_to_delete}")
    print(f"  Audit Logs:      {logs_to_delete}")
    print(f"  Notifications:   {notifs_to_delete}")

    if dry_run:
        print("\n[DRY RUN] No changes were made.")
        return

    print("\nExecuting deletions...")
    res_comments = db.comments.delete_many(comment_filter)
    res_reports = db.comment_reports.delete_many({})
    res_logs = db.moderation_logs.delete_many({})
    res_notifs = db.notifications.delete_many(notif_filter)
    res_users = db.users.delete_many(user_filter)
    res_sessions = db.sessions.delete_many(session_filter)

    print("[SUCCESS] Cleanup complete:")
    print(f"  Deleted {res_users.deleted_count} users")
    print(f"  Deleted {res_sessions.deleted_count} sessions")
    print(f"  Deleted {res_comments.deleted_count} comments")
    print(f"  Deleted {res_reports.deleted_count} comment reports")
    print(f"  Deleted {res_logs.deleted_count} moderation logs")
    print(f"  Deleted {res_notifs.deleted_count} notifications")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    clean_database(dry_run=dry)

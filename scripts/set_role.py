import sys
from pathlib import Path

# Add project root to sys.path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from api.core.database import get_mongo_db
from api.core.config import settings


def print_usage():
    print("""
Usage:
  python scripts/set_role.py <email_or_username> <student|moderator|admin>
  python scripts/set_role.py --list

Examples:
  python scripts/set_role.py surya.25bcs10632@sst.scaler.com admin
  python scripts/set_role.py mod_user moderator
  python scripts/set_role.py --list
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    db = get_mongo_db()
    if db is None:
        print("\n[!] MongoDB Atlas connection is not configured or unavailable.")
        print(f"    Check your MONGODB_URI setting in .env.")
        sys.exit(1)

    if sys.argv[1] == "--list":
        users = list(db.users.find({}, {"email": 1, "username": 1, "display_name": 1, "role": 1}))
        if not users:
            print("\nNo users found in database.")
            return

        print(f"\nFound {len(users)} users in SST Study Platform:")
        print(f"{'Username':<25} {'Role':<12} {'Email':<35} {'Display Name'}")
        print("-" * 90)
        for u in users:
            uname = u.get("username") or "[no username]"
            role = u.get("role") or "student"
            email = u.get("email") or "[no email]"
            dname = u.get("display_name") or ""
            print(f"{uname:<25} {role:<12} {email:<35} {dname}")
        print("-" * 90)
        return

    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    target_identifier = sys.argv[1].strip()
    new_role = sys.argv[2].strip().lower()

    if new_role not in ["student", "moderator", "admin"]:
        print(f"\n[!] Invalid role '{new_role}'. Allowed roles are: student, moderator, admin")
        sys.exit(1)

    query = {
        "$or": [
            {"email": target_identifier.lower()},
            {"username": target_identifier.lower()}
        ]
    }

    user = db.users.find_one(query)
    if not user:
        print(f"\n[!] User not found matching identifier: '{target_identifier}'")
        print("    Ensure the student has logged in at least once via Google GIS.")
        sys.exit(1)

    res = db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"role": new_role}}
    )

    print(f"\n[OK] Successfully updated role for '{user.get('email')}' (@{user.get('username')})")
    print(f"     Old Role: {user.get('role', 'student')}  -->  New Role: {new_role}")


if __name__ == "__main__":
    main()

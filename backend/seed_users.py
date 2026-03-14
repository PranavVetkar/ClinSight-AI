"""
Seed script — creates 3 hardcoded demo users in the local SQLite db.

Usage:
    cd backend
    python seed_users.py
"""
from db.local_db import init_db, get_user_by_email, create_user
from auth.utils import hash_password
import uuid
from datetime import datetime, timezone

SEED_USERS = [
    {"name": "Alice Johnson",  "email": "alice@demo.com",   "password": "alice1234"},
    {"name": "Bob Smith",      "email": "bob@demo.com",     "password": "bob1234"},
    {"name": "Charlie Dev",    "email": "charlie@demo.com", "password": "charlie1234"},
]


def seed():
    init_db()  # ensure tables exist
    created = 0
    skipped = 0

    for u in SEED_USERS:
        if get_user_by_email(u["email"]):
            print(f"  ⚠️  Skipping {u['email']} — already exists")
            skipped += 1
            continue

        uid = str(uuid.uuid4())
        create_user({
            "uid": uid,
            "name": u["name"],
            "email": u["email"],
            "password_hash": hash_password(u["password"]),
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        print(f"  ✅ Created: {u['email']}  (password: {u['password']})")
        created += 1

    print(f"\nDone! {created} created, {skipped} skipped.")
    print("\nDemo credentials:")
    for u in SEED_USERS:
        print(f"  {u['email']}  /  {u['password']}")


if __name__ == "__main__":
    print("🌱 Seeding demo users into local SQLite DB...\n")
    seed()

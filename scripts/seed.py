"""Seed the database with sample users for local development.

Usage:
    python -m scripts.seed          # insert seed data
    python -m scripts.seed --nuke   # wipe and re-seed
"""

import argparse

from api.database import Base, get_engine, session_scope
from api.models import User

SEED_USERS = [
    {"email": "alice@example.com", "name": "Alice Johnson", "bio": "Backend engineer"},
    {"email": "bob@example.com", "name": "Bob Smith", "bio": "Frontend developer"},
    {"email": "carol@example.com", "name": "Carol Williams", "bio": "DevOps lead"},
    {"email": "dave@example.com", "name": "Dave Brown", "bio": "Product manager"},
    {"email": "eve@example.com", "name": "Eve Davis", "bio": "QA engineer"},
]


def seed(nuke: bool = False) -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    with session_scope() as db:
        if nuke:
            count = db.query(User).delete()
            print(f"Deleted {count} existing users")

        existing = {u.email for u in db.query(User.email).all()}

        inserted = 0
        for user_data in SEED_USERS:
            if user_data["email"] in existing:
                print(f"  skip: {user_data['email']} (exists)")
                continue
            db.add(User(**user_data))
            inserted += 1
            print(f"  add:  {user_data['email']}")

        print(f"\nSeeded {inserted} users ({len(existing)} already existed)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed users database")
    parser.add_argument("--nuke", action="store_true", help="Delete all existing data before seeding")
    args = parser.parse_args()

    seed(nuke=args.nuke)

import pytest
from src.backend.app import create_app
from src.backend.app.extensions import db
from src.backend.app.models import User


@pytest.fixture(scope="session")
def app():
    app = create_app()  # uses your real MySQL config from .env / config.py
    with app.app_context():
        yield app


def test_print_all_users(app):
    with app.app_context():
        users = db.session.query(User).all()

        print(f"\n{'─'*50}")
        print(f"  Users table — {len(users)} row(s) found")
        print(f"{'─'*50}")

        if not users:
            print("  (empty)")
        else:
            for u in users:
                print(f"  id:           {u.user_id}")
                print(f"  email:        {u.email}")
                print(f"  display_name: {u.display_name}")
                print(f"  created_at:   {u.created_at}")
                print(f"{'─'*50}")

        print()
        assert True  # always passes — this is just for visibility
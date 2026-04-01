import pytest
from datetime import date
from decimal import Decimal

from src.backend.app import create_app
from src.backend.app.extensions import db
from src.backend.app.models import (
    User, Account, Category, Transaction, Goal, Bill,
    AccountType, CategoryType, CategoryColor,
    TransactionType, GoalStatus, BillFrequency,
)

# ── App fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app():
    test_settings = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret",
    }
    app = create_app(test_config=test_settings)
    with app.app_context():
        from src.backend.app.models import User, Account, Category, Goal, Bill, Transaction
        db.create_all()
        yield app
        db.drop_all()


# ── Model fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def user(app):
    with app.app_context():
        u = User(email="test@example.com", password_hash="hashed")
        db.session.add(u)
        db.session.flush()
        yield u
        db.session.rollback()


@pytest.fixture
def account(app, user):
    with app.app_context():
        a = Account(
            user_id=user.user_id,
            account_name="Chase Checking",
            account_type=AccountType.CHECKING,
        )
        db.session.add(a)
        db.session.flush()
        yield a
        db.session.rollback()


@pytest.fixture
def category(app, user):
    with app.app_context():
        c = Category(
            user_id=user.user_id,
            category_name="Groceries",
            category_type=CategoryType.EXPENSE,
            color=CategoryColor.GREEN,
        )
        db.session.add(c)
        db.session.flush()
        yield c
        db.session.rollback()


@pytest.fixture
def goal(app, user, account):
    with app.app_context():
        g = Goal(
            user_id=user.user_id,
            title="Emergency Fund",
            target_amount=Decimal("5000.00"),
            current_amount=Decimal("1000.00"),
            account_id=account.account_id,
        )
        db.session.add(g)
        db.session.flush()
        yield g
        db.session.rollback()


@pytest.fixture
def bill(app, user, account, category):
    with app.app_context():
        b = Bill(
            user_id=user.user_id,
            account_id=account.account_id,
            category_id=category.category_id,
            bill_name="Netflix",
            amount=Decimal("15.99"),
            frequency=BillFrequency.MONTHLY,
            next_due_date=date(2026, 1, 1),
        )
        db.session.add(b)
        db.session.flush()
        yield b
        db.session.rollback()


@pytest.fixture
def transaction(app, account, category):
    with app.app_context():
        t = Transaction(
            account_id=account.account_id,
            category_id=category.category_id,
            amount=Decimal("-42.50"),
            transaction_date=date(2026, 1, 15),
            transaction_type=TransactionType.EXPENSE,
            transaction_description="Whole Foods",
        )
        db.session.add(t)
        db.session.flush()
        yield t
        db.session.rollback()


# ── User ───────────────────────────────────────────────────────────────────

class TestUser:
    def test_defaults(self, user):
        assert user.display_name is None
        assert isinstance(user.user_id, str)
        assert len(user.user_id) == 36

    def test_unique_ids(self, app):
        with app.app_context():
            u1 = User(email="a@example.com", password_hash="h")
            u2 = User(email="b@example.com", password_hash="h")
            db.session.add_all([u1, u2])
            db.session.flush()
            assert u1.user_id != u2.user_id
            db.session.rollback()

    def test_name_to_show_no_display_name(self, user):
        assert user.name_to_show == "test@example.com"

    def test_name_to_show_with_display_name(self, user):
        user.display_name = "Tom"
        assert user.name_to_show == "Tom"


# ── Account ────────────────────────────────────────────────────────────────

class TestAccount:
    def test_defaults(self, account):
        assert account.balance == Decimal("0.00")

    def test_account_type(self, account):
        assert account.account_type == AccountType.CHECKING

    def test_balance_is_decimal(self, account):
        assert isinstance(account.balance, Decimal)

    def test_unique_ids(self, app, user):
        with app.app_context():
            a1 = Account(user_id=user.user_id, account_name="A", account_type=AccountType.SAVINGS)
            a2 = Account(user_id=user.user_id, account_name="B", account_type=AccountType.SAVINGS)
            db.session.add_all([a1, a2])
            db.session.flush()
            assert a1.account_id != a2.account_id
            db.session.rollback()


# ── Category ───────────────────────────────────────────────────────────────

class TestCategory:
    def test_defaults(self, category):
        assert category.parent_id is None

    def test_color_enum(self, category):
        assert category.color == CategoryColor.GREEN

    def test_color_value(self, category):
        assert category.color.value == "#10B981"

    def test_sub_category(self, app, user, category):
        with app.app_context():
            sub = Category(
                user_id=user.user_id,
                category_name="Organic",
                category_type=CategoryType.EXPENSE,
                color=CategoryColor.GREEN,
                parent_id=category.category_id,
            )
            db.session.add(sub)
            db.session.flush()
            assert sub.parent_id == category.category_id
            db.session.rollback()

    def test_income_type(self, app, user):
        with app.app_context():
            cat = Category(
                user_id=user.user_id,
                category_name="Salary",
                category_type=CategoryType.INCOME,
                color=CategoryColor.BLUE,
            )
            db.session.add(cat)
            db.session.flush()
            assert cat.category_type == CategoryType.INCOME
            db.session.rollback()

    def test_all_colors_available(self):
        colors = list(CategoryColor)
        assert len(colors) == 9


# ── Transaction ────────────────────────────────────────────────────────────

class TestTransaction:
    def test_defaults(self, transaction):
        assert transaction.bill_id is None
        assert isinstance(transaction.transaction_id, str)
        assert len(transaction.transaction_id) == 36

    def test_expense_amount_is_negative(self, transaction):
        assert transaction.amount < 0

    def test_income_amount_is_positive(self, app, account):
        with app.app_context():
            t = Transaction(
                account_id=account.account_id,
                amount=Decimal("3000.00"),
                transaction_date=date(2026, 1, 1),
                transaction_type=TransactionType.INCOME,
            )
            db.session.add(t)
            db.session.flush()
            assert t.amount > 0
            db.session.rollback()


# ── Goal ───────────────────────────────────────────────────────────────────

class TestGoal:
    def test_defaults(self, goal):
        assert goal.goal_status == GoalStatus.ACTIVE
        assert goal.target_date is None

    def test_progress_pct(self, goal):
        assert goal.progress_pct == pytest.approx(20.0)

    def test_progress_pct_zero_target(self, app, user):
        with app.app_context():
            g = Goal(user_id=user.user_id, title="Test", target_amount=Decimal("0"))
            db.session.add(g)
            db.session.flush()
            assert g.progress_pct == 0.0
            db.session.rollback()

    def test_remaining(self, goal):
        assert goal.remaining == Decimal("4000.00")

    def test_remaining_never_negative(self, app, user):
        with app.app_context():
            g = Goal(
                user_id=user.user_id,
                title="Done",
                target_amount=Decimal("100"),
                current_amount=Decimal("200"),
            )
            db.session.add(g)
            db.session.flush()
            assert g.remaining == Decimal("0.00")
            db.session.rollback()

    def test_completed_status(self, goal):
        goal.goal_status = GoalStatus.COMPLETED
        assert goal.goal_status == GoalStatus.COMPLETED


# ── Bill ───────────────────────────────────────────────────────────────────

class TestBill:
    def test_defaults(self, bill):
        assert bill.is_active is True

    def test_advance_due_date_monthly(self, bill):
        bill.next_due_date = date(2026, 1, 31)
        bill.advance_due_date()
        assert bill.next_due_date == date(2026, 2, 28)

    def test_advance_due_date_daily(self, bill):
        bill.frequency = BillFrequency.DAILY
        bill.next_due_date = date(2026, 1, 31)
        bill.advance_due_date()
        assert bill.next_due_date == date(2026, 2, 1)

    def test_advance_due_date_weekly(self, bill):
        bill.frequency = BillFrequency.WEEKLY
        bill.next_due_date = date(2026, 1, 1)
        bill.advance_due_date()
        assert bill.next_due_date == date(2026, 1, 8)

    def test_advance_due_date_yearly(self, bill):
        bill.frequency = BillFrequency.YEARLY
        bill.next_due_date = date(2026, 3, 1)
        bill.advance_due_date()
        assert bill.next_due_date == date(2027, 3, 1)

    def test_advance_due_date_leap_year(self, bill):
        bill.frequency = BillFrequency.YEARLY
        bill.next_due_date = date(2024, 2, 29)
        bill.advance_due_date()
        assert bill.next_due_date == date(2025, 2, 28)
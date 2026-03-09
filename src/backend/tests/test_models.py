import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID

from app.models import (
    User, Account, Category, Transaction, Goal, Bill,
)
from app.models.enums import (
    AccountType, CategoryType, CategoryColor,
    TransactionType, GoalStatus, BillFrequency,
)

# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def user():
    return User(email="test@example.com", password_hash="hashed")

@pytest.fixture
def account(user):
    return Account(
        user_id=user.user_id,
        account_name="Chase Checking",
        account_type=AccountType.CHECKING,
    )

@pytest.fixture
def category(user):
    return Category(
        user_id=user.user_id,
        name="Groceries",
        type=CategoryType.EXPENSE,
        color=CategoryColor.GREEN,
    )

@pytest.fixture
def bill(user, account, category):
    return Bill(
        user_id=user.user_id,
        account_id=account.account_id,
        name="Netflix",
        amount=Decimal("15.99"),
        frequency=BillFrequency.MONTHLY,
        next_due_date=date(2026, 1, 1),
        category_id=category.category_id,
    )

@pytest.fixture
def goal(user, account):
    return Goal(
        user_id=user.user_id,
        title="Emergency Fund",
        target_amount=Decimal("5000.00"),
        current_amount=Decimal("1000.00"),
        account_id=account.account_id,
    )

@pytest.fixture
def transaction(account, category):
    return Transaction(
        account_id=account.account_id,
        amount=Decimal("-42.50"),
        creation_date=date(2026, 1, 15),
        type=TransactionType.EXPENSE,
        category_id=category.category_id,
        description="Whole Foods",
    )


# ── User ───────────────────────────────────────────────────────────────────

class TestUser:
    def test_defaults(self, user):
        assert user.display_name is None
        assert isinstance(user.user_id, UUID)
        assert isinstance(user.creation_date, datetime)

    def test_creation_date_is_utc(self, user):
        assert user.creation_date.tzinfo == timezone.utc

    def test_unique_ids(self):
        u1 = User(email="a@example.com", password_hash="h")
        u2 = User(email="b@example.com", password_hash="h")
        assert u1.user_id != u2.user_id


# ── Account ────────────────────────────────────────────────────────────────

class TestAccount:
    def test_defaults(self, account):
        assert account.balance == Decimal("0.00")

    def test_account_type(self, account):
        assert account.account_type == AccountType.CHECKING

    def test_balance_is_decimal(self, account):
        assert isinstance(account.balance, Decimal)

    def test_unique_ids(self, user):
        a1 = Account(user_id=user.user_id, account_name="A", account_type=AccountType.SAVINGS)
        a2 = Account(user_id=user.user_id, account_name="B", account_type=AccountType.SAVINGS)
        assert a1.account_id != a2.account_id


# ── Category ───────────────────────────────────────────────────────────────

class TestCategory:
    def test_defaults(self, category):
        assert category.parent_id is None

    def test_color_enum(self, category):
        assert category.color == CategoryColor.GREEN
        assert category.color == "#10B981"   # str, Enum equality

    def test_sub_category(self, user, category):
        sub = Category(
            user_id=user.user_id,
            name="Organic",
            type=CategoryType.EXPENSE,
            parent_id=category.category_id,
        )
        assert sub.parent_id == category.category_id

    def test_income_type(self, user):
        cat = Category(user_id=user.user_id, name="Salary", type=CategoryType.INCOME)
        assert cat.type == CategoryType.INCOME

    def test_all_colors_available(self):
        colors = [c for c in CategoryColor]
        assert len(colors) == 9


# ── Transaction ────────────────────────────────────────────────────────────

class TestTransaction:
    def test_defaults(self, transaction):
        assert transaction.bill_id is None
        assert isinstance(transaction.transaction_id, UUID)


    def test_expense_amount_is_negative(self, transaction):
        assert transaction.amount < 0

    def test_income_amount_is_positive(self, account):
        t = Transaction(account_id=account.account_id, amount=Decimal("3000.00"),
                        creation_date=date(2026, 1, 1), type=TransactionType.INCOME)
        assert t.amount > 0


# ── Goal ───────────────────────────────────────────────────────────────────

class TestGoal:
    def test_defaults(self, goal):
        assert goal.status == GoalStatus.ACTIVE
        assert goal.target_date is None

    def test_progress_pct(self, goal):
        # 1000 / 5000 = 20%
        assert goal.progress_pct == pytest.approx(20.0)

    def test_progress_pct_zero_target(self, user):
        g = Goal(user_id=user.user_id, title="Test", target_amount=Decimal("0"))
        assert g.progress_pct == 0.0

    def test_remaining(self, goal):
        assert goal.remaining == Decimal("4000.00")

    def test_remaining_never_negative(self, user):
        g = Goal(user_id=user.user_id, title="Done",
                 target_amount=Decimal("100"), current_amount=Decimal("200"))
        assert g.remaining == Decimal("0.00")

    def test_completed_status(self, goal):
        goal.status = GoalStatus.COMPLETED
        assert goal.status == GoalStatus.COMPLETED


# ── Bill ───────────────────────────────────────────────────────────────────

class TestBill:
    def test_defaults(self, bill):
        assert bill.is_active is True

    def test_advance_due_date_monthly(self, bill):
        bill.next_due_date = date(2026, 1, 31)
        bill.advance_due_date()
        assert bill.next_due_date == date(2026, 2, 28)   # handles short months

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
        bill.next_due_date = date(2024, 2, 29)   # leap day
        bill.advance_due_date()
        assert bill.next_due_date == date(2025, 2, 28)   # non-leap year fallback

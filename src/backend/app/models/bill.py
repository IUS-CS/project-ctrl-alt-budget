import uuid
from calendar import monthrange
from datetime import date
from sqlalchemy.sql import func
from src.backend.app.extensions import db
from src.backend.app.models.enums import BillFrequency


class Bill(db.Model):
    __tablename__ = 'bills'

    bill_id       = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id       = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    account_id    = db.Column(db.String(36), db.ForeignKey('accounts.account_id'), nullable=False)
    category_id   = db.Column(db.String(36), db.ForeignKey('categories.category_id'), default=None)
    bill_name     = db.Column(db.String(50), nullable=False)
    amount        = db.Column(db.Numeric(15, 2), nullable=False)
    frequency     = db.Column(db.Enum(BillFrequency), nullable=False)
    next_due_date = db.Column(db.Date, nullable=False)
    is_active     = db.Column(db.Boolean, nullable=False, default=True)
    created_at    = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # Relationships
    user         = db.relationship('User', back_populates='bills')
    account      = db.relationship('Account', back_populates='bills')
    category     = db.relationship('Category', back_populates='bills')
    transactions = db.relationship('Transaction', back_populates='bill')

    # ── Methods ───────────────────────────────────────────────────────────

    def advance_due_date(self) -> None:
        """Advance next_due_date by one frequency period, handling edge cases."""
        d = self.next_due_date

        if self.frequency == BillFrequency.DAILY:
            from datetime import timedelta
            self.next_due_date = d + timedelta(days=1)

        elif self.frequency == BillFrequency.WEEKLY:
            from datetime import timedelta
            self.next_due_date = d + timedelta(weeks=1)

        elif self.frequency == BillFrequency.MONTHLY:
            month = d.month + 1 if d.month < 12 else 1
            year  = d.year if d.month < 12 else d.year + 1
            # Clamp day to last valid day of target month
            day   = min(d.day, monthrange(year, month)[1])
            self.next_due_date = date(year, month, day)

        elif self.frequency == BillFrequency.YEARLY:
            year = d.year + 1
            # Handle Feb 29 on non-leap years
            day  = min(d.day, monthrange(year, d.month)[1])
            self.next_due_date = date(year, d.month, day)
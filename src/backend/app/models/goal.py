import uuid
from decimal import Decimal
from sqlalchemy.sql import func
from src.backend.app.extensions import db
from src.backend.app.models.enums import GoalStatus


class Goal(db.Model):
    __tablename__ = 'goals'

    goal_id        = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id        = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    account_id     = db.Column(db.String(36), db.ForeignKey('accounts.account_id'), default=None)
    title          = db.Column(db.String(255), nullable=False)
    target_amount  = db.Column(db.Numeric(15, 2), nullable=False)
    current_amount = db.Column(db.Numeric(15, 2), nullable=False, default=Decimal("0.00"))
    target_date    = db.Column(db.Date, default=None)
    goal_status    = db.Column(db.Enum(GoalStatus), nullable=False, default=GoalStatus.ACTIVE)
    created_at     = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # Relationships
    user    = db.relationship('User', back_populates='goals')
    account = db.relationship('Account', back_populates='goals')

    # ── Computed properties ────────────────────────────────────────────────

    @property
    def progress_pct(self) -> float:
        """Percentage of goal completed (0.0 – 100.0)."""
        if not self.target_amount or self.target_amount == 0:
            return 0.0
        return float(self.current_amount / self.target_amount * 100)

    @property
    def remaining(self) -> Decimal:
        """Amount still needed; never goes below zero."""
        diff = self.target_amount - self.current_amount
        return max(Decimal("0.00"), diff)
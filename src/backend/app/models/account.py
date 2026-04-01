import uuid
from decimal import Decimal
from sqlalchemy.sql import func
from src.backend.app.extensions import db
from src.backend.app.models.enums import AccountType


class Account(db.Model):
    __tablename__ = 'accounts'

    account_id   = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id      = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    account_name = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    balance      = db.Column(db.Numeric(15, 2), nullable=False, default=Decimal("0.00"))
    created_at   = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # Relationships
    user         = db.relationship('User', back_populates='accounts')
    goals        = db.relationship('Goal', back_populates='account')
    bills        = db.relationship('Bill', back_populates='account')
    transactions = db.relationship('Transaction', back_populates='account')
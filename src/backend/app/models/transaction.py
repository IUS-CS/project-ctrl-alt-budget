import uuid
from sqlalchemy.sql import func
from src.backend.app.extensions import db
from src.backend.app.models.enums import TransactionType


class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id          = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id              = db.Column(db.String(36), db.ForeignKey('accounts.account_id'), nullable=False)
    category_id             = db.Column(db.String(36), db.ForeignKey('categories.category_id'), default=None)
    bill_id                 = db.Column(db.String(36), db.ForeignKey('bills.bill_id'), default=None)
    amount                  = db.Column(db.Numeric(15, 2), nullable=False)
    transaction_description = db.Column(db.Text, default=None)
    transaction_date        = db.Column(db.Date, nullable=False, server_default=func.current_date())
    transaction_type        = db.Column(db.Enum(TransactionType), nullable=False)
    created_at              = db.Column(db.DateTime, server_default=func.now())

    # Relationships
    account  = db.relationship('Account', back_populates='transactions')
    category = db.relationship('Category', back_populates='transactions')
    bill     = db.relationship('Bill', back_populates='transactions')
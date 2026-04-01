import uuid
from sqlalchemy.sql import func
from src.backend.app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id       = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email         = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name  = db.Column(db.String(50), default=None)
    created_at    = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # Relationships
    accounts    = db.relationship('Account',     back_populates='user')
    goals       = db.relationship('Goal',        back_populates='user')
    categories  = db.relationship('Category',    back_populates='user')
    bills       = db.relationship('Bill',        back_populates='user')

    @property
    def name_to_show(self):
        return self.display_name if self.display_name else self.email
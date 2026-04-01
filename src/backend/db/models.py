from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(50), default=None)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    @property
    def name_to_show(self):
        return self.display_name if self.display_name else self.email
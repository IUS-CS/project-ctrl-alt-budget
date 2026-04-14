import uuid
from src.backend.app.extensions import db
from src.backend.app.models.enums import CategoryType, CategoryColor


class Category(db.Model):
    __tablename__ = 'categories'

    category_id   = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id       = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    parent_id     = db.Column(db.String(36), db.ForeignKey('categories.category_id'), default=None)
    category_name = db.Column(db.String(50), nullable=False)
    category_type = db.Column(db.Enum(CategoryType), nullable=False)
    color         = db.Column(db.Enum(CategoryColor), nullable=False)

    # Relationships
    user          = db.relationship('User', back_populates='categories')
    parent        = db.relationship('Category', remote_side='Category.category_id', back_populates='subcategories')
    subcategories = db.relationship('Category', back_populates='parent')
    bills         = db.relationship('Bill', back_populates='category')
    transactions  = db.relationship('Transaction', back_populates='category')
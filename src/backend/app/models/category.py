from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4
from .enums import CategoryType, CategoryColor


@dataclass
class Category:
    user_id: UUID
    name: str
    type: CategoryType
    parent_id: Optional[UUID] = None # Self reference for sub categories
    color: Optional[CategoryColor] = None 
    category_id: UUID   = field(default_factory=uuid4)

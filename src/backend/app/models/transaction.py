from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from .enums import TransactionType


@dataclass
class Transaction:
    account_id: UUID
    amount: Decimal     
    type: TransactionType
    category_id:     Optional[UUID]   = None
    bill_id:         Optional[UUID]   = None
    description:     Optional[str]    = None
    transaction_id: UUID = field(default_factory=uuid4)
    creation_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

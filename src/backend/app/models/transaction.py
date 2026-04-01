from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from .enums import TransactionType


@dataclass
class Transaction:
    account_id: UUID        # The account this transaction belongs to 
    amount: Decimal         # Transaction amount - negaive = expense, positive = income or transfer
    type: TransactionType
    category_id:     Optional[UUID]   = None    # Optional for organizing transactions
    bill_id:         Optional[UUID]   = None    # Optional for recurring bill
    description:     Optional[str]    = None    # Optional note for transaction
    transaction_id: UUID = field(default_factory=uuid4)
    creation_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

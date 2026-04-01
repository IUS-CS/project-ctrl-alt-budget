from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from .enums import AccountType


@dataclass
class Account:
    user_id: UUID       # Links this account to its owner 
    account_name: str       # Display name for account
    account_type: AccountType       
    balance: Decimal = Decimal("0.00")
    account_id: UUID   = field(default_factory=uuid4)
    creation_date:  datetime   = field(default_factory=lambda: datetime.now(timezone.utc))
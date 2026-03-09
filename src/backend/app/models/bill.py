from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from .enums import BillFrequency


@dataclass
class Bill:
    user_id:       UUID
    account_id:    UUID
    name:          str
    amount:        Decimal
    frequency:     BillFrequency
    next_due_date: date
    category_id:   Optional[UUID]  = None
    is_active:     bool            = True
    bill_id:       UUID            = field(default_factory=uuid4)
    created_at:    datetime        = field(default_factory=lambda: datetime.now(timezone.utc))

    # Potential implementation for auto due date calculation
    # Requires date-util package
    def advance_due_date(self) -> None:
        # Advance next_due_date by one frequency interval
        from dateutil.relativedelta import relativedelta
        intervals = {
            BillFrequency.DAILY: relativedelta(days=1),
            BillFrequency.WEEKLY: relativedelta(weeks=1),
            BillFrequency.MONTHLY: relativedelta(months=1),
            BillFrequency.YEARLY: relativedelta(years=1)
        }
        self.next_due_date += intervals[self.frequency] 
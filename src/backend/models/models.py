from __future__ import annotations # Allows postponed type evaluation 
from dataclasses import dataclass, field # Generates boilerplate code
from datetime import datetime, date, timezone # Used for dates and times
from decimal import Decimal # Used for more precise float values
from typing import Optional # Allows for nullable values 
from uuid import UUID, uuid4 # UUID Generation
from .enums import AccountType, CategoryType, TransactionType, GoalStatus, BillFrequency, CategoryColor


@dataclass
class User:
    email: str
    password_hash: str
    display_name: Optional[str] = None
    user_id: UUID   = field(default_factory=uuid4) 
    creation_date:  datetime   = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Account:
    user_id: UUID
    account_name: str
    account_type: AccountType 
    balance: Decimal = Decimal("0.00")
    account_id: UUID   = field(default_factory=uuid4)
    creation_date:  datetime   = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Category:
    user_id: UUID
    name: str
    type: CategoryType
    parent_id: Optional[UUID] = None # Self reference for sub categories
    color: Optional[CategoryColor] = None 
    category_id: UUID   = field(default_factory=uuid4)

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

@dataclass
class Goal:
    user_id: UUID
    title: str
    target_amount: Decimal
    current_amount: Decimal = Decimal("0.00")
    account_id: Optional[UUID] = None
    target_date: Optional[date] = None
    status: GoalStatus = GoalStatus.ACTIVE
    goal_id: UUID = field(default_factory=uuid4)
    creation_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Methods for mutation and retrieval
    # Calculate Progress Percentage
    @property 
    def progress_pct(self) -> float:
        if self.target_amount == 0:
            return 0.0
        return float(self.current_amount / self.target_amount * 100)
    
    # Calculate Remaining 
    @property 
    def remaining(self) -> Decimal:
        return max(Decimal("0.00"), self.target_amount - self.current_amount)
    
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
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from .enums import GoalStatus

@dataclass
class Goal:
    user_id: UUID       # Links goal to its owner
    title: str      # Display name for goal
    target_amount: Decimal
    current_amount: Decimal = Decimal("0.00")
    account_id: Optional[UUID] = None   # Optional account linked to goal
    target_date: Optional[date] = None  # Optional deadline for reaching goal
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
    # Returns 0 if goal is exceeded
    @property 
    def remaining(self) -> Decimal:
        return max(Decimal("0.00"), self.target_amount - self.current_amount)
    
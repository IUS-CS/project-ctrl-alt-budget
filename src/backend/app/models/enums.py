from enum import Enum

class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"

class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class CategoryColor(str, Enum):
    RED    = "#EF4444"
    ORANGE = "#F97316"
    YELLOW = "#F59E0B"
    GREEN  = "#10B981"
    BLUE   = "#3B82F6"
    PURPLE = "#A855F7"
    PINK   = "#EC4899"
    TEAL   = "#14B8A6"
    GRAY   = "#6B7280"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"

class BillFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    
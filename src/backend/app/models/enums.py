from enum import Enum

# Defines allowed account types a user can create
class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"

# Defines whether a category tracks income or expenses
class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

# Defines a set of colors for category labels
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

# Defines the type of financial transaction
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

# Defines the possible states of a savings goal
class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"

# Defines how often a recurring bill is charged
class BillFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    
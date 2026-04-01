from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    email: str      # Unique Email  
    password_hash: str      # Hashed password
    display_name: Optional[str] = None      # Optional name for ui
    user_id: UUID   = field(default_factory=uuid4)      # Auto generated unique ID
    creation_date:  datetime   = field(default_factory=lambda: datetime.now(timezone.utc))      # Timestamps of account creation

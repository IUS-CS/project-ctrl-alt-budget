from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    email: str
    password_hash: str
    display_name: Optional[str] = None
    user_id: UUID   = field(default_factory=uuid4) 
    creation_date:  datetime   = field(default_factory=lambda: datetime.now(timezone.utc))

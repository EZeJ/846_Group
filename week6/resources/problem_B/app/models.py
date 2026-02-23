from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(str, Enum):
    open = "open"
    closed = "closed"
    triage = "triage"


@dataclass(frozen=True)
class Issue:
    id: int
    title: str
    status: Status
    priority: int  # 1 (low) .. 5 (high)
    created_at: datetime
    assignee: Optional[str] = None
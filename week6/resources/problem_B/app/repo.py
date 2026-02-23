from __future__ import annotations
from datetime import datetime, timezone
from typing import Iterable, List, Optional

from .models import Issue, Status


class InMemoryIssueRepo:
    """
    Fake repository (pretend DB).
    """

    def __init__(self) -> None:
        now = datetime(2026, 2, 1, tzinfo=timezone.utc)
        self._issues: List[Issue] = [
            Issue(id=1, title="Login button misaligned", status=Status.open, priority=2, created_at=now),
            Issue(id=2, title="Crash on export", status=Status.triage, priority=5, created_at=now),
            Issue(id=3, title="Add dark mode", status=Status.closed, priority=3, created_at=now),
            Issue(id=4, title="Slow search query", status=Status.open, priority=4, created_at=now),
            Issue(id=5, title="Broken link on help page", status=Status.closed, priority=1, created_at=now),
        ]

    def list_all(self) -> List[Issue]:
        # Return a copy to prevent accidental external mutation
        return list(self._issues)

    def add(self, issue: Issue) -> None:
        self._issues.append(issue)

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        for issue in self._issues:
            if issue.id == issue_id:
                return issue
        return None
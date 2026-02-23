from __future__ import annotations
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from .models import Issue, Status
from .repo import InMemoryIssueRepo


class IssueService:
    def __init__(self, repo: InMemoryIssueRepo) -> None:
        self.repo = repo

    def list_issues(
        self,
        status: Optional[str] = None,
        q: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns list of dicts for API response.
        """
        issues = self.repo.list_all()

        # --- BUG: status filter is wrong in a subtle way ---
        if status:
            # Intended: filter by exact status.
            # Actual: includes items incorrectly when `status` is a substring of the enum repr.
            issues = [i for i in issues if status in str(i.status)]

        if q:
            q_lower = q.lower()
            issues = [i for i in issues if q_lower in i.title.lower()]

        return [self._to_public(i) for i in issues]

    def _to_public(self, issue: Issue) -> Dict[str, Any]:
        d = asdict(issue)
        d["status"] = issue.status.value
        d["created_at"] = issue.created_at.isoformat()
        return d
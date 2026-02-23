from __future__ import annotations
from fastapi import FastAPI, Query

from .repo import InMemoryIssueRepo
from .service import IssueService

app = FastAPI(title="Mini Issues")

_repo = InMemoryIssueRepo()
_service = IssueService(_repo)


@app.get("/issues")
def list_issues(
    status: str | None = None,
    q: str | None = None,
):
    """
    Returns a list of issues.

    TODO (exercise): add pagination and sorting while keeping response format stable.
    """
    items = _service.list_issues(status=status, q=q)
    return {"items": items, "total": len(items), "limit": len(items), "offset": 0}
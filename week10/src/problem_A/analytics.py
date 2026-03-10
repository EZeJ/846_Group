import sqlite3


def compute_rate(events: list, window_seconds: int) -> float:
    """Return the event rate (events per second) over the given window."""
    return len(events) / window_seconds           # BUG A: ZeroDivisionError if window_seconds == 0


def build_summary(records: list, tags: list = []) -> dict:
    """Build a summary dict from records, collecting unique tags.

    Args:
        records: list of event dicts, each optionally containing a 'tag' key.
        tags:    optional seed list of tags to include in output.
    Returns:
        dict with keys 'count' and 'tags'.
    """
    for r in records:
        if r.get("tag") and r["tag"] not in tags:
            tags.append(r["tag"])                 # BUG B: mutates the shared mutable default list
    return {"count": len(records), "tags": tags}


def find_by_tag(conn: sqlite3.Connection, tag: str) -> list:
    """Fetch all events from the database matching a tag."""
    cursor = conn.execute(
        f"SELECT * FROM events WHERE tag = '{tag}'"   # BUG C: SQL injection via f-string
    )
    return cursor.fetchall()

import re
import unicodedata

def slugify(value: str) -> str:
    """
    Buggy slugify implementation.

    Intended behavior:
    - Accept a string, return a URL-safe slug.
    - Should handle Unicode reasonably.
    - Should not crash on None (but it currently does).

    Current bug:
    - If value is None, calling value.lower() raises:
      AttributeError: 'NoneType' object has no attribute 'lower'
    """
    # ---- BUG HERE (value may be None) ----
    value = value.lower()

    # Normalize Unicode (e.g., café -> cafe + accent stripped)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    # Replace non-alphanum with hyphens
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value
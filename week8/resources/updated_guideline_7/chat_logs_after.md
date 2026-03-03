User: in starter_code_after, CI fails on a unit test. Start debugging from the FAILURE entry point (topmost frame in our code from the stack trace), not from main.py.
Failing test: tests/test_slug.py::test_slugify_none_is_handled
Error: AttributeError: 'NoneType' object has no attribute 'lower'
Relevant frame: utils/text.py:18 in slugify
Propose the smallest safe fix. Keep edge cases in mind.

GitHub Copilot: Read [](file:///Users/lilianahotsko/Desktop/846_Group/starter_code_after/utils/text.py)

Let's see test file.

Read [](file:///Users/lilianahotsko/Desktop/846_Group/starter_code_after/tests/test_slug.py)

Using "Multi-Replace String in Files"


```

```


Ran terminal command:  cd /Users/lilianahotsko/Desktop/846_Group/starter_code_after && pytest tests/test_slug.py::test_slugify_none_is_handled -q

Ran terminal command:  pytest -q

✅ **Debugging from the Failure Frame**

The CI failure points straight at this frame:

```
utils/text.py:18 in slugify
AttributeError: 'NoneType' object has no attribute 'lower'
```

and the test expecting:

```python
assert slugify(None) == ""
```

So the fix should live in `slugify` – not in `main.py` – and be the **smallest safe change**.

---

### 🔧 What changed

I updated `slugify` to:

1. **Return an empty string immediately if the input is `None`.**
2. Coerce any non‑string value to `str` before calling `.lower()`  
   (defensive, handles edge cases like integers, objects, etc.).

This prevents the crash and still lets the rest of the normalization logic run on real text.

---

### ✅ Updated text.py

```python
def slugify(value: str) -> str:
    """
    Buggy slugify implementation.

    Intended behavior:
    - Accept a string, return a URL-safe slug.
    - Should handle Unicode reasonably.
    - Should not crash on None (but it currently does).
    """
    # ---- BUG HERE (value may be None) ----
    if value is None:
        # return empty slug for missing input
        return ""
    # ensure we have a string in case callers pass something else
    value = str(value)
    value = value.lower()

    # Normalize Unicode (e.g., café -> cafe + accent stripped)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")

    # Replace non-alphanum with hyphens
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value
```

---

### 📦 Results

- `pytest tests/test_slug.py::test_slugify_none_is_handled` now passes.
- Full test suite (`pytest -q`) reports **all tests OK**.
- No changes were made elsewhere; this is the minimal safe fix.



Made changes.
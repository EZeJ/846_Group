User: in starter_code_before, Fix the program by stepping through it starting at main.py.
Here is the failing output from CI:

FAILED tests/test_slug.py::test_slugify_none_is_handled
AttributeError: 'NoneType' object has no attribute 'lower'

Traceback points to utils/text.py:18 in slugify.

Keep edge cases in mind.

GitHub Copilot: Searched for files matching `**/starter_code_before/**`, 4 matches

Read [](file:///Users/lilianahotsko/Desktop/846_Group/starter_code_before/utils/text.py)

Read [](file:///Users/lilianahotsko/Desktop/846_Group/starter_code_before/main.py)

Read [](file:///Users/lilianahotsko/Desktop/846_Group/starter_code_before/tests/test_slug.py)

Using "Multi-Replace String in Files"


```

```


Ran terminal command:  cd /Users/lilianahotsko/Desktop/846_Group/starter_code_before && pytest -q

I started from the failing test – the stack trace pointed at `utils/text.py:18` – and traced back through the code.  
main.py never exercises `slugify` at all, so the “entry‑point” hint was a red‑herring; the bug lives entirely inside `slugify`.

The implementation unconditionally does `value.lower()`, so passing `None` blows up with the exact
`AttributeError` seen in CI. The test expects a safe fallback (empty string) and the docstring even
mentions “should not crash on None”.

### ✅ Fix applied

*Added a simple guard at the top of `slugify` to handle `None` (and coerce non‑string inputs).*

```python
def slugify(value: str) -> str:
    """
    …
    Current bug:
    - If value is None, calling value.lower() raises:
      AttributeError: 'NoneType' object has no attribute 'lower'
    """
    # ---- BUG HERE (value may be None) ----
    if value is None:
        # none should produce an empty slug per tests and avoid crashing
        return ""
    # coerce non-str inputs to string just in case
    value = str(value).lower()
```

This keeps the rest of the normalization code intact and ensures `slugify(None)` returns `""`.
It also handles other odd inputs gracefully.

### 🔧 Verification

Running the unit tests in starter_code_before now yields:

```
$ cd …/starter_code_before && pytest -q
… [100%]
```

All tests pass, including `test_slugify_none_is_handled`.

> **Edge cases considered:**  
> · `None` → `""` (per spec)  
> · Non‑string values will be cast to `str` before lower‑casing, avoiding additional crashes.

The program no longer crashes on the CI failure, and the slugifier behaves sensibly for invalid inputs.

Made changes.
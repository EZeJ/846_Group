## Proposed behavior groups:

1. Response type handling  – str, bytes, dict/JSON, tuples
2. make_response()         – valid inputs, invalid types
3. Error handling          – 404, 405, 500, custom handlers
4. Request context         – setup and teardown
5. URL building (url_for)  – valid routes, missing params, unknown endpoint
6. Request hooks           – before_request, after_request, teardown_request
7. Static files            – send_static_file, open_resource

## Proposed test groups:

For every described behavior, branch, and edge case include:
  - 1 happy-path test
  - 1 boundary test (None, empty, zero, min/max)
  - 1 negative/exception test (invalid input, wrong type, missing route)


## Proposed Constraints:
  - pytest with app/client fixtures
  - never call internal methods directly — use test_client() or
    test_request_context() only
  - do not test blueprints, CLI, or async
  - all tests must pass with: pytest test_app_py.py

## Proposed pipeline for the test fixing:

For each failure:
  1. Identify the root cause from the error message only
  2. Fix only the failing test — do not modify passing tests
  3. Regenerate only the fixed test methods
```


### Guideline 5(Extended G2+G4): Use a structured 3-step prompt to maximise test coverage

**Description:**
Instead of asking an LLM to generate tests in one shot, use a fixed three-step prompt sequence that combines scope, intention, decomposition, edge cases, and a repair loop:

**Step 1 — Describe intention per behavior group (no code yet)**
Scope the target module into its distinct behavior groups, then ask the LLM to describe the intended behavior of each group — what it does, what inputs it accepts, what it returns or raises, and any conditional branches. Do not ask for code yet.

**Step 2 — Generate tests using the description**
Using the Step 1 output, ask the LLM to write one test group per behavior, and for every described behavior, branch, and edge case require different types of tests.

Also, include explicit constraints, like test framework, what not to test, and how methods must be invoked (e.g. always via the test client, never by calling internals directly).

**Step 3 — Repair failures**
Run the tests, paste the exact `pytest --tb=short` output back to the LLM, and ask it to fix only the failing tests (not the code) using only the error message as evidence. Repeat until all tests pass (or the ones that don't pass are testing the functionality that naturally fails due to the bug).

**Reasoning:**
- Without scope, the LLM picks shallow happy-path cases
- Without decomposition, it loses track of responsibilities in large modules
- Without boundary/negative requests, it skips edge cases entirely
- Without intention-first, it writes assertions that misrepresent actual behavior — over 85% of execution failures stem from incorrect assertions, not bugs [5]
- Without a repair loop, compilation and runtime errors stay unfixed

**Bad Example:**
```
"Write tests for app.py. Make sure they pass."
```

**Good Example:**

*Step 1 prompt:* (make the model reason based on the cpntent)
```
Read the "Project/file". Describe the intended behavior — inputs, return values, exceptions, branches: 

1. Response type handling
2. Error handling
3. Request context
4. URL building (valid routes, missing params, unknown endpoint)
...

Do not write any code yet.
```

*Step 2 prompt:* (List the requirements and constrains)
```
Using the descriptions above, write pytest tests for "file".

For each of the group write a separate test group. For every described behavior, branch, and edge case include: (and list the categories of the tests to include). Constraints: (list constrains)
```

*Step 3 prompt:* (Fixing the errors)
```
For each failure:
  1. Identify the root cause from the error message only
  2. Fix only the failing test — do not modify passing tests
  3. Regenerate only the fixed test methods
```

##### P.S. The guideline and the prompt examples where rephrased and improved by GPT-5.
---



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

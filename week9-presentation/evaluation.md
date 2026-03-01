# Week 9 Evaluation: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

## 1. General Evaluation Criteria

Students should evaluate their testing approach based on these criteria:

- **Bug Discovery Rate:** How effectively the tests identify defects in the code.
- **Test Coverage:** The extent to which tests cover critical paths, edge cases, and requirements.

- **Assertion density:** Number of assertions per test.

---

## 2. Evaluation for Specific Example Problems

## Problem A: Checkout Service Testing

**Evaluation Description:**
Students should discover **all 9 intentional bugs** when applying both guidelines properly. A vague one-shot prompt will miss most bugs. The bugs span interacting features (item-level discounts, three coupon types, loyalty points, shipping) so only a prompt that explicitly decomposes each business rule and tests boundary/combination cases will uncover them all.

**Applicable Guidelines:**
* Guideline 1: Specify the Testing Goal and Scope in the Prompt
* Guideline 2: Use a Generate–Validate–Repair Loop Instead of One-Shot Generation

**Possible Bug Discovery Checklist:**

| Bug # | Description                                   | Actual Behavior                                                                         | Expected Behavior                                                                                    |
| ----- | --------------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1     | Empty cart is not validated                   | Proceeds to checkout with 0 subtotal, returns "success"                                 | Raises `CheckoutError("Cart is empty")`                                                              |
| 2     | Stock check logic is inverted                 | Raises `CheckoutError` when item **is** in stock; allows checkout when out of stock     | Raises `CheckoutError` only when item is **not** in stock                                            |
| 3     | Bundle discount threshold off-by-one          | Bundle 5% discount only triggers when `quantity > 3` (i.e., quantity 4+)                | Should trigger when `quantity >= 3` (i.e., quantity 3+)                                              |
| 4     | SUMMER20 cap logic inverted                   | Uses `max(20%, $30)`, flooring the discount at $30 instead of capping it there          | Should use `min(20%, $30)` to cap at $30                                                             |
| 5     | FLASH5 + VIP combination not blocked          | VIP customers can use FLASH5 coupon and receive both discounts                          | Should raise `CheckoutError` when `FLASH5` is requested with a VIP customer                          |
| 6     | Tax calculated on pre-discount subtotal       | Tax is `subtotal * 0.13` instead of `(discounted_subtotal - loyalty_credit) * 0.13`     | Tax base must be the fully-discounted, loyalty-adjusted amount                                       |
| 7     | Shipping threshold uses pre-discount subtotal | Free shipping granted when original `subtotal >= $50`, even if discounts bring it below | Should check `discounted_subtotal >= $50`                                                            |
| 8     | Payment failure not handled                   | `charge()` return value is ignored; checkout returns "success" even on payment failure  | Raises `CheckoutError("Payment failed: <reason>")` when `charge()` returns `{"success": False, ...}` |
| 9     | Total not floored at zero                     | With a large enough discount + loyalty credit, `total` can be negative                  | `total = max(0.0, total)`                                                                            |

**Expected Results:**

- **Without Guideline 3:** Test should find 0-4 bugs (mainly obvious ones)
- **With Guideline 3:** Test should find 6-9 bugs (comprehensive edge case coverage)

**Advice**

- Ask an LLM to help you check how many bugs the generated tests uncover, based on this table and the tests generated from your prompt.

**Good Example (with guidelines):**
First prompt:

```text
Generate pytest unit tests for `CheckoutService.process_checkout` in `checkout_service.py`.

Framework: pytest + `unittest.mock.MagicMock` for `InventoryService` and `PaymentGateway`.
Use `@pytest.mark.parametrize` for boundary values. Use `pytest.raises(CheckoutError)` for all error paths.
Do NOT test the external dependencies themselves.

Cover each rule with at least one test:

- Empty cart -> CheckoutError
- Stock check: error when out of stock, success when in stock
- Flash-sale discount (5%), bundle discount (quantity >= 3, 5%)
- SAVE10 (10%, min $100), SUMMER20 (20% capped at $30, min $75), FLASH5 (5% on flash items)
- VIP discount (15%) incompatible with all coupons; FLASH5 incompatible with VIP
- Loyalty credit applied only when points >= 500
- Shipping: $10 if discounted subtotal < $50, else $0
- Tax: 13% on post-discount, post-loyalty-credit amount
- Payment failure -> CheckoutError
- Total must never be negative

Parametrize: quantity in {2,3,4}; subtotal at $74.99/$75/$99.99/$100; shipping boundary at $49.99/$50/$50.01.
State any assumptions as inline comments. Return only the test file.
```

Second prompt:

```
Running the tests produced these failures:

[ERROR COPIED]

Are these bugs in the tests or the implementation? Explain the root cause
and return a corrected test file. Do not modify checkout_service.py.
```

If needed, continue the Generate–Validate–Repair loop.

**Bad Example (without guidelines):**

- Running a single prompt with text similar to this:

```text
Write tests for this code.
```

---

## Problem B_1: User Validation Testing

**Evaluation Description:**
Students must identify bugs in the provided code. Using Guideline 3, they should find **at least 7 bugs**; the more bugs found, the better.

You should compare bugs found using the checklist below with the bugs.

---

**Applicable Guidelines:**
* Guideline 3: Explicitly Request Boundary and Negative Test Cases

#### **UNGUIDED PROMPT (Before Applying Guidelines)**

```
Write pytest tests for the user_validator.py module. Make sure the tests cover the validation functions and pass.
```

**Expected Output from Unguided Prompt:**

- **Tests Generated:** 4-8 basic tests
- **Bugs Found:** 2-5 bugs (mainly obvious ones like empty strings, simple invalid formats)
- **Missing Coverage:**
  - No None/null input testing
  - Missing boundary conditions (off-by-one errors)
  - No special character edge cases for email
  - No tests for usernames starting with numbers or being all numbers
  - Missing password special character and uppercase requirements
  - No age boundary testing (0, negative, extremely high values)
  
---

#### **GUIDED PROMPT (After Applying Guideline 3)**

```
Generate pytest unit tests for the user validation module in `user_validator.py`.

The module contains four validation functions: validate_email(), validate_age(), validate_username(), and validate_password().

**Required test categories for EACH function (minimum 2 tests per category):**

1. **Boundary Cases:**
   - Empty strings
   - Minimum/maximum length values
   - Off-by-one conditions (e.g., length 2, 3, 30, 31 for username)
   - Edge numeric values (0, negative, very large numbers for age)

2. **Null/Missing Inputs:**
   - None values
   - Missing parameters where applicable

3. **Invalid Format Cases:**
   - For email: consecutive dots, consecutive special chars, starting with special char, no @ symbol, no domain
   - For username: starting with numbers, all numbers, special characters beyond underscore
   - For password: missing uppercase, missing digits, missing special characters, too short

4. **Exception Paths:**
   - TypeError for None inputs
   - Proper True/False returns for valid/invalid inputs

**Framework:** pytest with @pytest.mark.parametrize for efficient testing
**Constraints:**
- Do not modify user_validator.py
- Each test must have clear assertions
- Use descriptive test names that indicate what is being tested

Generate comprehensive tests that will expose validation bugs.
```

**Expected Output from Guided Prompt:**

- **Tests Generated:** 20-30 comprehensive tests
- **Bugs Found:** 7-13 bugs
- **Coverage Includes:**
  - TypeError checks for None inputs across all functions
  - Email edge cases (consecutive dots, special char placement)
  - Username validation flaws (numeric starts, all-numeric usernames)
  - Password missing requirements (uppercase, special characters)
  - Age boundary violations (0, negative, unreasonably high values)
  - Off-by-one errors in length validation

---

#### **Possible Bug Discovery Checklist:**

| Bug # | Description                                                      | Actual Behavior                         | Expected Behavior                                  |
| ----- | ---------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------- |
| 1     | `validate_email()` does not raise a TypeError when given None    | Returns None or fails silently          | Raises TypeError for None input                    |
| 2     | Email validation allows consecutive dots                         | Accepts "user..name@domain.com"         | Rejects emails with consecutive dots               |
| 3     | Email validation allows consecutive special characters           | Accepts "user.@name@domain.com"         | Rejects emails with consecutive special characters |
| 4     | Email validation allows to start from special character          | Accepts ".username@domain.com"          | Rejects emails starting with special character     |
| 5     | `validate_age()` has no upper and lower bound                    | Accepts age 999 and 0                   | Restricts age to reasonable max                    |
| 6     | `validate_username()` does not raise a TypeError when given None | Returns None or fails silently          | Raises TypeError for None input                    |
| 7     | Username length validation off-by-one error                      | Accepts too short/long usernames        | Enforces correct min/max length                    |
| 8     | Username can start with numbers                                  | Accepts "1username"                     | Rejects usernames starting with numbers            |
| 9     | Username can be all numbers                                      | Accepts "123456"                        | Rejects usernames that are all numbers             |
| 10    | `validate_password()` does not raise a TypeError when given None | Returns None or fails silently          | Raises TypeError for None input                    |
| 11    | Password length validation off-by-one error                      | Accepts too short/long passwords        | Enforces correct min/max length                    |
| 12    | Password validation missing special character check              | Accepts passwords without special chars | Requires at least one special character            |
| 13    | Password validation doesn't require uppercase letters            | Accepts all lowercase passwords         | Requires at least one uppercase letter             |

**Expected Results:**

- **Without Guideline 3:** Should find 2-5 bugs (mainly obvious ones)
- **With Guideline 3:** Should find 7-13 bugs (comprehensive edge case coverage)

**Advice**

- Ask an LLM to help you check how many bugs the generated tests uncover, based on this table and the tests generated from your prompt.

---

## Problem B_2: Order Processing Decomposition

**Evaluation Description:**  
Students must find **at least 7** intentional bugs hidden in the complex process_order() method by applying Guideline 4.

Decomposition should reveal logical flaws that black-box testing misses.

You should compare bugs found using the checklist below with the bugs.

---

**Applicable Guidelines:**
* Guideline 4: Decompose Complex Methods Before Asking for Tests

#### **UNGUIDED PROMPT (Before Applying Guidelines)**

```
Write pytest tests for order_processor.py. Test the process_order method to make sure it works correctly.
```

**Expected Output from Unguided Prompt:**

- **Tests Generated:** 3-6 basic tests
- **Bugs Found:** 2-3 bugs (only surface-level issues like missing order_id)
- **Missing Coverage:**
  - No systematic decomposition of sub-behaviors
  - Missing validation for negative quantities/prices
  - No tests for discount edge cases (negative totals, invalid codes)
  - Tax calculation timing not verified
  - Shipping logic not properly tested
  - Payment processing assumed to succeed
  - Error handling not comprehensively tested

---

#### **GUIDED PROMPT (After Applying Guideline 4)**

```
The file `order_processor.py` contains a complex `process_order()` method that handles multiple responsibilities.

**Step 1: Identify Logical Sub-Behaviors**
Analyze the `process_order()` method and list its distinct logical sub-behaviors (validation, calculations, discounts, taxes, shipping, payment, etc.). Describe what each sub-behavior should do. Do not write code yet.

**Step 2: Generate Tests Per Sub-Behavior**
For each sub-behavior identified in Step 1, generate a separate pytest test group. For each sub-behavior, include:

1. **Happy Path Test:** Normal, expected inputs
2. **Boundary Cases:**
   - Zero quantities/prices
   - Minimum/maximum order values
   - Threshold values for shipping (e.g., $99.99, $100, $100.01)
   - Discount boundaries
3. **Negative/Invalid Cases:**
   - Negative quantities or prices
   - Missing required fields (order_id, customer_id, items, payment_method)
   - Invalid discount codes
   - Empty items list
4. **Edge Cases:**
   - Discount making total negative
   - Tax calculation timing (before vs after discount)
   - Shipping cost logic with discounts
   - Payment failures

**Framework:** pytest with @pytest.mark.parametrize
**Constraints:**
- Do not modify order_processor.py
- Test each sub-behavior in isolation where possible
- Use descriptive test class and method names
- Clear assertions for expected vs actual behavior

Generate comprehensive tests that expose hidden bugs through systematic behavior decomposition.
```

**Expected Output from Guided Prompt:**

- **Tests Generated:** 25-40 comprehensive tests organized by sub-behavior
- **Bugs Found:** 7-10 bugs (through systematic testing of each responsibility)
- **Coverage Includes:**
  - Complete validation testing (all required fields, negative values)
  - Subtotal calculation verification
  - Discount logic edge cases (negative totals, invalid codes)
  - Tax timing verification (pre vs post-discount)
  - Shipping threshold testing with boundary values
  - Payment processing validation
  - Error handling across all sub-behaviors

---

#### **Decomposition Quality Assessment:**

Students should identify these logical sub-behaviors:

1. Order data validation
2. Subtotal calculation
3. Discount application
4. Tax calculation
5. Shipping cost determination
6. Payment processing
7. Order state updates
8. Result generation

---

#### **Possible Bug Discovery Checklist:**

| Bug # | Description                                            | Actual Behavior                                       | Expected Behavior                       |
| ----- | ------------------------------------------------------ | ----------------------------------------------------- | --------------------------------------- |
| 1     | Incomplete order validation                            | Missing checks for customer_id, items, payment_method | Validates all required fields           |
| 2     | No validation for negative quantities or prices        | Accepts negative values                               | Rejects negative quantities/prices      |
| 3     | "FREEBIE" discount can make total negative             | Total becomes negative                                | Ensures total is never negative         |
| 4     | Invalid discount codes not handled                     | Ignores invalid codes                                 | Raises error for invalid discount codes |
| 5     | Tax calculated on pre-discount amount                  | Calculates tax before discount                        | Calculates tax after discount           |
| 6     | Free shipping logic broken                             | Charges shipping for orders > $100                    | Free shipping for orders > $100         |
| 7     | Payment processing assumes success                     | No validation of payment                              | Validates payment and handles failures  |
| 8     | Generic error handling loses important failure details | Returns generic error                                 | Returns specific error details          |
| 9     | Payment amount not validated                           | Accepts negative payment amounts                      | Rejects negative payment amounts        |
| 10    | Unknown payment methods not properly rejected          | Accepts unknown methods                               | Rejects unknown payment methods         |

**Expected Results:**

- **Without Guideline 4:** Should find 2-3 bugs (surface-level issues)
- **With Guideline 4:** Should find 7-10 bugs (through systematic behavior testing)

**Advice**

- Ask an LLM to help you check how many bugs the generated tests uncover, based on this table and the tests generated from your prompt.

---

## Problem B_3: Data Parser Edge Cases

**Evaluation Description:**  
Students should discover ** at least 10 bugs** across multiple parsing functions when applying both Guidelines 3 and 4.

You should compare bugs found using the checklist below with the bugs.

---

**Applicable Guidelines:**
* Guideline 3: Explicitly Request Boundary and Negative Test Cases
* Guideline 4: Decompose Complex Methods Before Asking for Tests

#### **UNGUIDED PROMPT (Before Applying Guidelines)**

```
Write pytest tests for data_parser.py. Test all the parsing functions to ensure they work correctly.
```

**Expected Output from Unguided Prompt:**

- **Tests Generated:** 6-10 basic tests
- **Bugs Found:** 3-6 bugs (mainly obvious input errors and crashes)
- **Missing Coverage:**
  - No None input testing across functions
  - Missing empty string/empty file testing
  - No tests for malformed data (invalid JSON, CSV with missing fields)
  - Missing regex pattern edge cases (negative numbers, scientific notation)
  - No whitespace edge cases testing
  - Missing type validation testing
  - No comprehensive error message verification

---

#### **GUIDED PROMPT (After Applying Guidelines 3 & 4)**

```
The file `data_parser.py` contains multiple parsing functions with different responsibilities.

**Step 1: Identify Functions and Their Sub-Behaviors**
List each parsing function and describe its intended behavior:
- parse_csv_data(): CSV parsing with delimiter support
- parse_json_config(): JSON parsing with required field validation
- extract_numbers(): Number extraction from text (integers, floats, scientific notation)
- normalize_whitespace(): Whitespace normalization with line break preservation option

For each function, identify edge cases and error conditions. Do not write code yet.

**Step 2: Generate Comprehensive Tests**
For EACH parsing function, generate separate test classes. For each function, include:

1. **Boundary Cases (minimum 2 tests):**
   - Empty string input
   - Empty files/data structures (header-only CSV, empty JSON object)
   - Minimum/maximum values
   - Single element inputs

2. **Null/Missing Input Cases (minimum 2 tests):**
   - None inputs
   - Missing required fields (for JSON)
   - Rows with missing fields (for CSV)

3. **Invalid Format Cases (minimum 3 tests):**
   - Malformed CSV (inconsistent columns, missing delimiters)
   - Invalid JSON (syntax errors, wrong types)
   - Invalid number formats (standalone dots, special characters)
   - Invalid whitespace patterns

4. **Exception Path Tests (minimum 2 tests):**
   - ParseError conditions and messages
   - TypeError for None inputs
   - Proper exception types for each error condition

5. **Special Edge Cases:**
   - CSV: header-only files, rows with different field counts
   - JSON: non-dictionary parsed results, deeply nested structures
   - Numbers: negative numbers, scientific notation (1e5), decimal edge cases (0.0, .5, 5.)
   - Whitespace: line break preservation logic, mixed whitespace types (tabs, spaces, newlines)

**Framework:** pytest with @pytest.mark.parametrize for efficient testing
**Constraints:**
- Do not modify data_parser.py
- Test each function's edge cases comprehensively
- Verify error messages are informative, not generic
- Use descriptive test names indicating the specific edge case

Generate systematic tests that will expose parsing bugs through comprehensive edge case coverage.
```

**Expected Output from Guided Prompt:**

- **Tests Generated:** 40-60 comprehensive tests organized by function
- **Bugs Found:** 10-24 bugs (comprehensive coverage across all parsing functions)
- **Coverage Includes:**
  - TypeError checks for None inputs across all functions
  - Empty/minimal input handling for all functions
  - CSV edge cases (empty files, missing fields, header-only)
  - JSON validation (non-dict results, missing required fields, decode errors)
  - Number extraction edge cases (negatives, scientific notation, standalone dots)
  - Whitespace handling edge cases (line break preservation, empty strings)
  - Generic error message issues
  - Type validation failures
- **Test Quality:** Highly systematic with parametrized tests covering all edge cases per function

---

#### **Possible Bug Discovery Checklist:**

| Bug # | Description                                                        | Actual Behavior                 | Expected Behavior                            |
| ----- | ------------------------------------------------------------------ | ------------------------------- | -------------------------------------------- |
| 1     | CSV: Crashes on None input                                         | Throws error or fails silently  | Handles None input gracefully                |
| 2     | CSV: Doesn't handle empty string input                             | Throws error or returns invalid | Returns empty result or error                |
| 3     | CSV: Fails on empty files or header-only files                     | Throws error or returns invalid | Handles empty/header-only files gracefully   |
| 4     | CSV: Doesn't handle rows with missing fields                       | Ignores or crashes              | Handles missing fields with error or default |
| 5     | CSV: Generic exception handling hides specific CSV errors          | Returns generic error           | Returns specific CSV error                   |
| 6     | JSON: Crashes on None input                                        | Throws error or fails silently  | Handles None input gracefully                |
| 7     | JSON: Doesn't validate that parsed JSON is a dictionary            | Accepts non-dict                | Validates parsed object is dict              |
| 8     | JSON: Required field validation continues instead of failing       | Continues with missing fields   | Fails if required fields missing             |
| 9     | JSON: Unhelpful error messages for JSON decode errors              | Returns generic error           | Returns informative decode error             |
| 10    | Numbers: Crashes on None input                                     | Throws error or fails silently  | Handles None input gracefully                |
| 11    | Numbers: Doesn't handle empty string                               | Throws error or returns invalid | Returns empty result or error                |
| 12    | Numbers: Regex doesn't capture negative numbers                    | Ignores negatives               | Captures negative numbers                    |
| 13    | Numbers: Doesn't handle scientific notation                        | Ignores scientific notation     | Captures scientific notation                 |
| 14    | Numbers: Fails on standalone dot "."                               | Throws error or returns invalid | Handles standalone dot gracefully            |
| 15    | Numbers: Silently ignores conversion errors                        | Ignores errors                  | Reports conversion errors                    |
| 16    | Whitespace: Crashes on None input                                  | Throws error or fails silently  | Handles None input gracefully                |
| 17    | Whitespace: Improper empty string handling                         | Throws error or returns invalid | Handles empty string gracefully              |
| 18    | Whitespace: Line break preservation logic inverted                 | Breaks lines incorrectly        | Preserves line breaks correctly              |
| 19    | Whitespace: Doesn't handle all whitespace types                    | Ignores some whitespace types   | Handles all whitespace types                 |
| 20    | Whitespace: Inappropriate stripping in some contexts               | Strips needed whitespace        | Strips only unnecessary whitespace           |
| 21    | Data Types: No null checks                                         | Ignores nulls                   | Checks for nulls                             |
| 22    | Data Types: Doesn't validate input is a dictionary                 | Accepts non-dict                | Validates input is dict                      |
| 23    | Data Types: Missing fields silently ignored                        | Ignores missing fields          | Reports missing fields                       |
| 24    | Data Types: Type checking logic flaws (inheritance, None handling) | Incorrect type checks           | Correctly checks types, handles None         |

**Expected Results:**

- **Without Guidelines 3 & 4:** Should find 3-6 bugs (mainly obvious input errors and crashes)
- **With Guidelines 3 & 4:** Should find 10-24 bugs (comprehensive edge case coverage across all parsing functions)

**Advice**

- Ask an LLM to help you check how many bugs the generated tests uncover, based on this table and the tests generated from your prompt.

---

## Problem C

### GUIDED vs. UNGUIDED COVERAGE COMPARISON

**Unguided prompt**:

Write tests for app.py. Make sure they pass.

**Guided Prompt**:

_Step 1 prompt:_

```
Read Flask's app.py. For each of these behavior groups only, describe
the intended behavior — inputs, return values, exceptions, branches:

1. Response type handling  – str, bytes, dict/JSON, tuples
2. make_response()         – valid inputs, invalid types
3. Error handling          – 404, 405, 500, custom handlers
4. Request context         – setup and teardown
5. URL building (url_for)  – valid routes, missing params, unknown endpoint
6. Request hooks           – before_request, after_request, teardown_request
7. Static files            – send_static_file, open_resource

Do not write any code yet.
```

_Step 2 prompt:_

```
Using the descriptions above, write pytest tests for app.py.

For each of the 7 groups write a separate test group. For every described
behavior, branch, and edge case include:
  - 1 happy-path test
  - 1 boundary test (None, empty, zero, min/max)
  - 1 negative/exception test (invalid input, wrong type, missing route)

Assertions must match the described behavior exactly — do not guess.

Constraints:
  - pytest with app/client fixtures
  - never call internal methods directly — use test_client() or
    test_request_context() only
  - do not test blueprints, CLI, or async
  - all tests must pass with: pytest test_app_py.py
```

_Step 3 prompt (after running pytest --tb=short -q):_

```
Here are the pytest failures:

<paste exact pytest output>

For each failure:
  1. Identify the root cause from the error message only
  2. Fix only the failing test — do not modify passing tests
  3. Regenerate only the fixed test methods
```

**Expected Results**:

|           Metric | Unguided | Guided |
| ---------------: | -------: | -----: |
|       Coverage % |    28.3% |  61.6% |
|    Covered lines |      123 |    268 |
|  Uncovered lines |      312 |    167 |
|     Tests passed |        3 |     12 |
|     Tests failed |        0 |      1 |
| Passes threshold |    False |   True |


**Unguided test file**:

```python
import os
from datetime import timedelta

import pytest

from flask import Flask


def test_get_send_file_max_age_various_types():
	app = Flask("testapp")

	# default is None
	app.config["SEND_FILE_MAX_AGE_DEFAULT"] = None
	assert app.get_send_file_max_age("foo.txt") is None

	# integer seconds are returned as-is
	app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600
	assert app.get_send_file_max_age("foo.txt") == 3600

	# timedelta is converted to seconds
	app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=7200)
	assert app.get_send_file_max_age("foo.txt") == 7200


def test_open_resource_modes(tmp_path):
	# create an app with a controlled root_path
	root = tmp_path / "approot"
	root.mkdir()

	fpath = root / "data.txt"
	fpath.write_text("hello\n")

	app = Flask("testapp", root_path=str(root))

	# invalid mode should raise
	with pytest.raises(ValueError):
		app.open_resource("data.txt", mode="w")

	# text read
	with app.open_resource("data.txt", mode="r", encoding="utf-8") as fh:
		assert fh.read() == "hello\n"

	# binary read
	with app.open_resource("data.txt", mode="rb") as fh:
		assert fh.read() == b"hello\n"


def test_make_shell_context_runs_processors():
	app = Flask("testapp")

	@app.shell_context_processor
	def _proc():
		return {"answer": 42}

	ctx = app.make_shell_context()
	assert "app" in ctx and "g" in ctx
	assert ctx["answer"] == 42

```

**Guided test file**:

```python

import os
import sys
from datetime import timedelta

import pytest

# Ensure tests import the local Flask package bundled in the workspace
HERE = os.path.dirname(__file__)
LOCAL_FLASK_SRC = os.path.abspath(os.path.join(HERE, "..", "flask", "src"))
if LOCAL_FLASK_SRC not in sys.path:
    sys.path.insert(0, LOCAL_FLASK_SRC)

from flask import Flask, Blueprint, abort, session


def test_send_static_file_serves_file_and_respects_timedelta_cache(tmp_path):
    from flask import send_from_directory

    app = Flask(__name__, static_folder=str(tmp_path))
    # create a static file
    p = tmp_path / "foo.txt"
    p.write_bytes(b"hello")

    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=60)

    client = app.test_client()
    # ensure a static route exists for testing (some setups may not auto-register)
    app.add_url_rule(
        "/static/<path:filename>",
        endpoint="static",
        view_func=lambda filename: send_from_directory(str(tmp_path), filename, max_age=app.get_send_file_max_age(filename)),
    )

    resp = client.get("/static/foo.txt")
    assert resp.status_code == 200
    assert resp.data == b"hello"
    # Cache-Control should include max-age=60
    cc = resp.headers.get("Cache-Control", "")
    assert "max-age=60" in cc


def test_send_static_file_not_found_returns_404(tmp_path):
    app = Flask(__name__, static_folder=str(tmp_path))
    client = app.test_client()
    resp = client.get("/static/does-not-exist.txt")
    assert resp.status_code == 404


def test_url_for_outside_request_requires_server_name():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "ok"

    # calling url_for outside a request context with _external=True and
    # without SERVER_NAME should raise a RuntimeError
    with pytest.raises(RuntimeError):
        app.url_for("index", _external=True)


def test_url_for_blueprint_relative_inside_request():
    app = Flask(__name__)
    bp = Blueprint("bp", __name__, url_prefix="/bp")

    @bp.route("/x")
    def x():
        return "ok"

    app.register_blueprint(bp)

    with app.test_request_context("/bp/x"):
        # blueprint-relative endpoint should resolve to the blueprint's URL
        u = app.url_for(".x")
        assert u.startswith("/bp")


def test_make_response_handles_various_return_types():
    app = Flask(__name__)

    @app.route("/json")
    def j():
        return {"a": 1}

    @app.route("/tuple")
    def t():
        return ("body", 201, {"X-Test": "yes"})

    client = app.test_client()
    r1 = client.get("/json")
    assert r1.is_json and r1.get_json() == {"a": 1}

    r2 = client.get("/tuple")
    assert r2.status_code == 201
    assert r2.headers.get("X-Test") == "yes"


def test_options_automatic_uses_default_options_response():
    app = Flask(__name__)

    @app.route("/onlyget", methods=("GET",))
    def onlyget():
        return "ok"

    client = app.test_client()
    resp = client.options("/onlyget")
    assert resp.status_code in (200, 204)
    allow = resp.headers.get("Allow", "")
    # Should include GET and OPTIONS
    assert "GET" in allow
    assert "OPTIONS" in allow


def test_before_request_short_circuit():
    app = Flask(__name__)

    @app.before_request
    def short():
        # short-circuit by returning a non-None value
        return "short"

    @app.route("/")
    def index():
        pytest.fail("view should not be called when before_request returns a value")

    client = app.test_client()
    r = client.get("/")
    assert r.data == b"short"


def test_after_request_can_modify_response():
    app = Flask(__name__)

    @app.after_request
    def add_header(resp):
        resp.headers["X-After"] = "yes"
        return resp

    @app.route("/resp")
    def resp():
        return "body"

    client = app.test_client()
    r = client.get("/resp")
    assert r.headers.get("X-After") == "yes"


def test_error_handler_for_http_exception_used():
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(e):
        return "custom404", 404

    client = app.test_client()
    r = client.get("/no-such-route")
    assert r.status_code == 404
    assert b"custom404" in r.data


def test_user_exception_propagates_when_testing_true():
    app = Flask(__name__)
    app.testing = True

    @app.route("/boom")
    def boom():
        raise ValueError("boom")

    client = app.test_client()
    with pytest.raises(ValueError):
        client.get("/boom")


def test_preprocess_request_url_value_preprocessor_modifies_view_args():
    app = Flask(__name__)

    bp = Blueprint("bp2", __name__, url_prefix="/bp2")

    @bp.url_value_preprocessor
    def add_flag(endpoint, values):
        # inject a value used by the view
        if values is not None:
            values.setdefault("injected", "yes")

    @bp.route("/show/<name>")
    def show(name, injected=None):
        # url_value_preprocessor adds the key into the view args,
        # so accept it as a parameter on the view
        return f"{name}-{injected}"

    app.register_blueprint(bp)
    client = app.test_client()
    r = client.get("/bp2/show/alice")
    assert r.data == b"alice-yes"


def test_session_saved_in_response_cookie():
    app = Flask(__name__)
    app.secret_key = "secret"

    @app.route("/set")
    def set():
        session["x"] = "1"
        return "ok"

    client = app.test_client()
    r = client.get("/set")
    # session cookie should be set
    sc = r.headers.get("Set-Cookie")
    assert sc is not None
    assert "session=" in sc.lower()


def test_test_client_context_manager_allows_request_local_access():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "ok"

    with app.test_client() as c:
        c.get("/?vodka=42")
        # inside the client context the request context should be available
        from flask import request

        assert request.args["vodka"] == "42"

```
---

## 3. Problem D Evaluation

### Problem D_1: Baseline Test Generation for Mini Autograd

**Evaluation Description:**  
The output should be a runnable pytest file that checks basic forward/backward behavior and at least one custom autograd function. Good tests should be deterministic and use explicit assertions.

**Marking Criteria (checklist):**
- Test file collects and runs under `pytest` from repo root.
- Covers forward correctness for at least one composed scalar expression.
- Covers backward correctness for both `+` and `*`.
- Includes ≥1 custom function forward/backward test (e.g., `axpy`, `square`, or `clamp01`).
- Uses small deterministic scalar values (no randomness).
- **Reference check:** passes on the new code base (`ProblemD/instructor/solution`) (tests are not asserting the wrong contract).

**Expected Results:**

- **Without structured prompts:** likely collection failures or weak smoke tests only.
- **With structured prompts:** runnable tests with concrete forward/backward assertions.

#### UNGUIDED PROMPT (Baseline)

```text
### Problem D_1: Understand the Mini Autograd API and Generate Baseline Tests

**Task Description:**  
This problem uses a **pure-Python mini autograd engine** (`ProblemD/student/src/mini_autograd.py`) that is inspired by PyTorch autograd, but does not require installing PyTorch.  
In this context, an **autograd function** means a custom operation with an explicit forward computation and backward (gradient) rule. In `ProblemD`, custom operations are implemented using a `Function.apply(...)` API similar to `torch.autograd.Function`.

Use an GPT-5-mini to generate a first pytest test files that checks baseline behavior for the mini engine:
Review and refine the generated tests so they are clean and runnable. 
Run your tests for detecting bugs, but do not change the implementation code yet.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`  
`ProblemD/student/tests/test_examples_smoke.py` (style example only)

---
```

**Expected Output (Unguided):**
- Likely failure mode: model tries to create files/run shell commands; output may include non-code or incorrect assumptions.
- Measured (Copilot CLI `gpt-5-mini`, latest run in `submits_2/problemD_copilot_cli/results/scorecard.md`):
  - original code base: **7 passed / 5 failed**
  - new code base: **11 passed / 1 failed** (baseline included an incorrect contract assertion about initial `grad`)

#### GUIDED PROMPT (Upgraded)

```text
You are generating pytest tests for a class exercise (Problem D_1).

Output contract (must follow exactly):
- return one runnable Python pytest file only
- no prose, no markdown fences, no headings
- do not run commands and do not create files

Execution environment contract:
- tests run from repository root
- use these imports (exactly):
  from ProblemD.student.src.mini_autograd import Tensor
  from ProblemD.student.src import demo_custom_functions as custom

Task:
- write baseline unit tests for the mini autograd engine:
  - forward correctness for simple scalar expressions
  - backward correctness for basic operations (+, *)
  - at least one custom function forward/backward case (use custom.axpy or custom.clamp01 or custom.square)

Fault model (each must be killed by ≥1 test, tag each test with `# targets: FM*`):
- FM1: `Tensor.backward(grad=...)` ignores the explicit upstream grad argument
- FM2: `__add__` sets `requires_grad` with AND instead of OR
- FM3: `__mul__` backward misses the upstream scaling factor for one operand
- FM4: custom function backward returns gradients in the wrong order

Constraints:
- deterministic small scalar values only
- explicit assertions (no smoke tests)
- use pytest only
- do not modify implementation files
```

**Expected Output (Guided):**
- Output is a single runnable pytest file (code-only) with pinned imports and explicit assertions.
- Measured (Copilot CLI `gpt-5-mini`):
  - original code base: **1 passed / 5 failed** (useful failing signals on buggy behaviors)
  - new code base: **6 passed / 0 failed**

---


### Problem D_2: Design Edge-Case Tests for Autograd Graph Semantics

**Evaluation Description:**  
The output should extend testing beyond arithmetic outputs to graph semantics: accumulation, `requires_grad` propagation, `detach()`, `zero_grad()`, upstream gradient scaling, and boundary behavior for a clamp-like op.

**Marking Criteria (checklist):**
- Test file collects and runs under `pytest` from repo root.
- Includes at least one shared-subgraph accumulation test (e.g., reuse an intermediate).
- Includes a `detach()` behavior test with a failure assertion (`pytest.raises(...)`).
- Includes a `zero_grad()` numeric reset test and verifies re-backward works afterward.
- Includes an explicit upstream gradient scaling test (e.g., `out.backward(2.0)`).
- Includes at least one boundary derivative test for `clamp01`.
- **Reference check:** passes on the new code base (`ProblemD/instructor/solution`) (tests reflect the intended contract).

#### UNGUIDED PROMPT (Baseline)

```text
### Problem D_2: Design Edge-Case Tests for Autograd Graph Semantics

**Task Description:**  
Use your LLM to extend the pytest suite and test **graph semantics**, not just arithmetic outputs. Add tests for behavior such as: gradient accumulation through shared subgraphs, etc.


Your tests should be small and deterministic. Avoid hidden dependencies and avoid rewriting the starter code in the test file.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`

---
```

**Expected Output (Unguided):**
- Measured (Copilot CLI `gpt-5-mini`):
  - original code base: **1 passed / 1 failed**
  - new code base: **2 passed / 0 failed**

Note: earlier runs hit collection errors due to top-level importing `demo_custom_functions` (it uses relative imports) and mixed prose/code output; our latest materialization step rewrites imports to `ProblemD.student.src...` and trims trailing non-code so pytest can collect.

#### GUIDED PROMPT (Upgraded)

```text
You are generating pytest tests for a class exercise (Problem D_2).

Output contract (must follow exactly):
- return one runnable Python pytest file only
- no prose, no markdown fences, no headings
- do not run commands and do not create files

Execution environment contract:
- tests run from repository root
- use these imports (exactly):
  import pytest
  from ProblemD.student.src.mini_autograd import Tensor
  from ProblemD.student.src import demo_custom_functions as custom

Goal:
Write small, deterministic tests for autograd *graph semantics* (not just arithmetic).

Mini-engine note (important for correct tests):
- intermediate tensors in this mini engine also store `.grad` and it can accumulate
- to test “two backward calls add to leaf grads” without changing upstream grad, rebuild the graph each time (preferred), or reset the output tensor’s grad before the second backward
- do NOT call `out.backward()` twice on the same `out` tensor for FM2 unless you first reset `out.grad` (prefer rebuilding the graph)

FM2 example pattern (preferred):
- `out1 = x * 3.0; out1.backward(); out2 = x * 3.0; out2.backward(); assert x.grad == 6.0`

Gradient sanity (avoid incorrect expected values):
- do NOT confuse forward values with derivatives
- example: if `out = x * 3.0`, then after `out.backward()` the expected `x.grad` is `3.0` (not `out.data`)

Fault model (each must be killed by ≥1 test, tag each test with `# targets: FM*`):
- FM1: shared subgraph does not accumulate grads (x used twice only counts once)
- FM2: calling backward twice does not accumulate (grads overwritten instead of added)
- FM3: `requires_grad` propagation is too strict/too loose for mixed (Tensor, constant)
- FM4: `detach()` returns a tensor that still requires grad / participates in backprop
- FM5: `zero_grad()` resets grad to None instead of numeric 0.0
- FM6: custom boundary derivative is inverted for clamp-like ops (inside vs outside interval)
- FM7: upstream grad scaling is not respected somewhere in the graph
- FM8: backward on a tensor that does not require grad fails to raise (or raises wrong error)

Required coverage:
- at least one test for shared-subgraph accumulation
- at least one test for repeated backward accumulation
- detach semantics (must include a failure assertion using `pytest.raises(...)` when appropriate)
- zero_grad semantics (numeric reset)
- at least one boundary test for `custom.clamp01`

Constraints:
- deterministic scalar inputs only (no randomness)
- explicit assertions (no print-only debugging)
- use pytest only
- do not modify implementation files
```

**Expected Output (Guided):**
- Output is code-only pytest with pinned imports and “fault-model tagged” tests.
- Measured (Copilot CLI `gpt-5-mini`):
  - original code base: **3 passed / 5 failed**
  - new code base: **8 passed / 0 failed**

---

### Problem D_3: Use an LLM to Generate Tests for the Standardized `axpy` Function

**Evaluation Description:**  
The output should be a runnable pytest file for `axpy(a, x, y)` that checks forward correctness and multiple backward/edge-case behaviors, including upstream-gradient scaling.

**Marking Criteria (checklist):**
- Test file collects and runs under `pytest` from repo root.
- Forward correctness: `axpy(a, x, y) == a*x + y` with explicit scalar assertions.
- Backward correctness for all three inputs (`a`, `x`, `y`) using `.grad`.
- Explicit upstream-gradient scaling test using `out.backward(grad=...)` with `grad != 1.0`.
- Gradient-order correctness is asserted (mapping to `a.grad`, `x.grad`, `y.grad`).
- Includes at least one edge case (zero/negative values or reuse).
- **Reference check:** passes on the new code base (`ProblemD/instructor/solution`).

#### UNGUIDED PROMPT (Baseline)

```text
### Problem D_3: Use an LLM to Generate Tests for the Standardized `axpy` Function

**Task Description:**  
All students will use an LLM to generate pytest tests for the same function: `axpy(a, x, y)` in `ProblemD/student/src/demo_custom_functions.py`.  
Your goal is to produce a clean, runnable test file for `axpy` and improve it through prompt refinement.

You must document and submit:
1. the model used,  
2. the prompt(s) used,  
3. the final generated/refined test code, and  

**Starter Code:**  
`ProblemD/student/src/demo_custom_functions.py`  
`ProblemD/student/src/mini_autograd.py`

---
```

**Expected Output (Unguided):**
- Measured (Copilot CLI `gpt-5-mini`):
  - original code base: **1 passed / 1 failed**
  - new code base: **2 passed / 0 failed**

Note: earlier runs hit collection errors due to mixed prose/code output and fragile import paths; our latest materialization step trims trailing non-code and normalizes imports so pytest can collect.

#### GUIDED PROMPT (Upgraded)

```text
You are generating pytest tests for the standardized class task (Problem D_3).

Target:
- `axpy(a, x, y)` in `ProblemD/student/src/demo_custom_functions.py`

Output contract (must follow exactly):
- return one runnable Python pytest file only
- no prose, no markdown fences, no headings
- do not run commands and do not create files

Execution environment contract:
- tests run from repository root
- use these imports (exactly):
  import pytest
  from ProblemD.student.src.mini_autograd import Tensor
  from ProblemD.student.src.demo_custom_functions import axpy

Contract:
- forward: `axpy(a, x, y) = a * x + y`
- backward (for scalar upstream grad g): grads must be in input order (a, x, y)
  - d/da = g * x
  - d/dx = g * a
  - d/dy = g * 1

Fault model (each must be killed by ≥1 test, tag each test with `# targets: FM*`):
- FM1: gradient order is wrong (a and x swapped)
- FM2: upstream grad argument is ignored (assumes g=1.0)
- FM3: missing scaling factor in one partial derivative (sign/scale error)
- FM4: reuse case does not accumulate correctly when the same Tensor is passed as multiple inputs

Required tests:
- forward correctness
- backward correctness for all three inputs
- explicit upstream scaling check using `out.backward(grad=...)` with grad != 1.0
- gradient-order correctness (assert mapping to a.grad, x.grad, y.grad matches contract)
- at least one edge case (zero or negative values)

Constraints:
- deterministic scalar inputs only
- explicit assertions (no smoke tests)
- use pytest only
- do not modify implementation files
```

**Expected Output (Guided):**
- Output is a single runnable pytest file with pinned imports and multiple discriminative assertions.
- Measured (Copilot CLI `gpt-5-mini`):
  - original code base: **1 passed / 5 failed**
  - new code base: **6 passed / 0 failed**

---

### Problem D_4: Bug-Fix Challenge Using Your Generated Tests

**Evaluation Description:**  
The output should be a single patch that fixes the original code base bugs while preserving the intended API and features. Correctness is verified by the official test suite.

**Marking Criteria (checklist):**
- Output is a single patch block in the required `*** Begin Patch ... *** End Patch` format.
- Patch updates **both** files:
  - `ProblemD/student/src/mini_autograd.py`
  - `ProblemD/student/src/demo_custom_functions.py`
- Fixes core autograd contract issues (upstream grad, `requires_grad` propagation, chain rule scaling).
- Fixes custom function backward contracts (axpy grad order, clamp01 boundary derivative).
- Minimal targeted edits; no broad refactors; public APIs unchanged.
- Passes `pytest -q ProblemD/instructor/tests` (expected **18 passed**).

#### UNGUIDED PROMPT (Baseline)

```text
### Problem D_4: Bug-Fix Challenge Using Your Generated Tests

**Task Description:**  
Use the tests you generated/refined in Problems D_1–D_3 to identify and fix bugs in the starter implementation (you may use an LLM to propose patches, but you must verify them with tests):
- `ProblemD/student/src/mini_autograd.py`
- `ProblemD/student/src/demo_custom_functions.py`

Requirements:
1. Run your own tests first and use failures to guide debugging.
2. Fix implementation bugs without deleting features.
3. Keep your tests (and any LLM-generated tests) as evidence of how you found the bugs.
4. Make sure your pass all your tests.


**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`  
---
```

**Expected Output (Unguided):**
- Likely failure mode: model tries to edit files via tools (or outputs steps) rather than producing a single extractable patch.
- Measured (Copilot CLI `gpt-5-mini`):
  - Patch artifact: **materialize failed** (no patch block to extract reliably)

#### GUIDED PROMPT (Upgraded)

```text
You are fixing bugs in a class exercise implementation (Problem D_4).

Target files:
- `ProblemD/student/src/mini_autograd.py`
- `ProblemD/student/src/demo_custom_functions.py`

Output contract (must follow exactly):
- output only one patch in this format (no prose, no markdown fences):
  *** Begin Patch
  *** Update File: <relative path only>
  @@
  -old
  +new
  *** End Patch
- do not run commands and do not create files
- do not use absolute paths; do not use `..` path traversal
- one patch may include multiple `*** Update File:` sections; keep them within the single Begin/End Patch
- patch must include these two update headers (exactly):
  - `*** Update File: ProblemD/student/src/mini_autograd.py`
  - `*** Update File: ProblemD/student/src/demo_custom_functions.py`

Patch goals (correctness contract):
- respect upstream gradient argument in `Tensor.backward(grad=...)`
- `__add__` should set `requires_grad` if either input requires grad
- `__mul__` backward must multiply by upstream grad for both inputs
- `zero_grad()` should reset leaf grad to `0.0`
- `detach()` should return a tensor with `requires_grad=False`
- `relu()` derivative should be `1.0` for positive input and `0.0` otherwise
- `exp()` backward should use `exp(x)` (the forward output)
- `Axpy.backward` gradient order must match inputs `(a, x, y)`
- `Clamp01.backward` should return gradient `1` only for `0 < x < 1`, else `0`

Constraints:
- keep public APIs unchanged
- preserve feature set
- avoid broad refactors
- make minimal targeted edits only
```

**Expected Output (Guided):**
- Output is a single patch that updates both target files and fixes all contract items.
- Measured (Copilot CLI `gpt-5-mini`):
  - Official test suite (`ProblemD/instructor/tests`): **18 passed / 0 failed**

---
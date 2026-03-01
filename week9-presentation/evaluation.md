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

### Problem B_1: User Validation Testing

**Evaluation Description:**
Students must identify bugs in the provided code. Using Guideline 3, they should find **at least 7 bugs**; the more bugs found, the better.

You should compare bugs found using the checklist below with the bugs.

---

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

**Example of Typical Unguided Test Output:**

```python
def test_validate_email_valid():
    assert validate_email("user@example.com") == True

def test_validate_email_invalid():
    assert validate_email("invalid") == False

def test_validate_username_valid():
    assert validate_username("validuser") == True

def test_validate_password_valid():
    assert validate_password("Password123") == True
```

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

**Example of Typical Unguided Test Output:**

```python
def test_process_order_basic():
    order = Order(
        order_id="ORD001",
        customer_id="CUST001",
        items=[{"product_id": "PROD1", "quantity": 2, "price": 50.0}],
        payment_method="credit_card",
        shipping_address={"street": "123 Main St"}
    )
    processor = OrderProcessor()
    result = processor.process_order(order)
    assert result["status"] == "completed"

def test_process_order_with_discount():
    order = Order(
        order_id="ORD002",
        customer_id="CUST002",
        items=[{"product_id": "PROD1", "quantity": 1, "price": 100.0}],
        payment_method="credit_card",
        shipping_address={"street": "123 Main St"}
    )
    processor = OrderProcessor()
    result = processor.process_order(order, discount_code="SAVE10")
    assert "discount" in result
```

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

**Example of Typical Unguided Test Output:**

```python
def test_parse_csv_basic():
    csv_data = "name,age\nJohn,30\nJane,25"
    result = parse_csv_data(csv_data)
    assert len(result) == 2

def test_parse_json_basic():
    json_data = '{"name": "John", "age": 30}'
    result = parse_json_config(json_data)
    assert result["name"] == "John"

def test_extract_numbers_basic():
    text = "I have 5 apples and 3.5 oranges"
    result = extract_numbers(text)
    assert 5.0 in result

def test_normalize_whitespace_basic():
    text = "Hello   World"
    result = normalize_whitespace(text)
    assert result == "Hello World"
```

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

---

## 3. Problem D Evaluation

### Problem D_1: Baseline Test Generation for Mini Autograd

**Evaluation Description:**  
Students generate an initial pytest suite for a pure-Python mini autograd engine and verify basic forward/backward behavior.

**Possible Behavior Discovery Checklist:**

| Check # | Description                     | Actual Baseline Behavior       | Expected Behavior                                |
| ------- | ------------------------------- | ------------------------------ | ------------------------------------------------ |
| 1       | Runnable imports and collection | Import/collection error        | Tests collect and run directly                   |
| 2       | Forward scalar assertions       | Missing due collection failure | Deterministic forward-value checks               |
| 3       | Backward checks for `+` and `*` | Missing due collection failure | Correct gradients asserted for both ops          |
| 4       | Custom autograd function checks | Missing due collection failure | At least one custom op tested (forward/backward) |
| 5       | Output contract                 | Mixed prose/code in early runs | Single runnable test file, code-only             |

**Expected Results:**

- **Without structured prompts:** likely collection failures or weak smoke tests only.
- **With structured prompts:** runnable tests with concrete forward/backward assertions.

**Measured Results:**

- Baseline prompt: collection/import failure.
- Guided prompt (phase 2): runnable suite, `1 passed / 4 failed`.

---

### Problem D_2: Graph Semantics and Edge-Case Testing

**Evaluation Description:**  
Students extend tests to graph semantics instead of only arithmetic outputs.

**Possible Behavior Discovery Checklist:**

| Check # | Description                           | Actual Baseline Behavior       | Expected Behavior                             |
| ------- | ------------------------------------- | ------------------------------ | --------------------------------------------- |
| 1       | Shared-subgraph gradient accumulation | Missing due collection failure | Explicit accumulation assertions              |
| 2       | `requires_grad` propagation           | Missing due collection failure | Propagation behavior verified                 |
| 3       | `detach()` contract                   | Missing due collection failure | `requires_grad=False` + backward failure path |
| 4       | `zero_grad()` semantics               | Missing due collection failure | Gradient reset behavior asserted              |
| 5       | Boundary case in custom function      | Missing due collection failure | At least one boundary-case gradient test      |
| 6       | Negative/exception assertion          | Missing due collection failure | At least one meaningful `pytest.raises` check |

**Expected Results:**

- **Without structured prompts:** non-runnable output or shallow happy-path tests.
- **With structured prompts:** runnable tests spanning multiple semantic categories.

**Measured Results:**

- Baseline prompt: collection/import failure.
- Guided prompt (phase 2): runnable suite, `2 passed / 4 failed`.

---

### Problem D_3: Standardized `axpy(a, x, y)` Tests

**Evaluation Description:**  
All students generate tests for the same function to support fair in-class comparison.

**Possible Behavior Discovery Checklist:**

| Check # | Description                         | Actual Baseline Behavior       | Expected Behavior                               |
| ------- | ----------------------------------- | ------------------------------ | ----------------------------------------------- |
| 1       | Forward check: `a*x + y`            | Missing due collection failure | Deterministic forward assertion                 |
| 2       | Gradients for `a`, `x`, `y`         | Missing due collection failure | Correct per-input gradient checks               |
| 3       | Gradient-order contract             | Missing due collection failure | Returned gradients mapped to input order        |
| 4       | Upstream grad scaling               | Missing due collection failure | `backward(grad=...)` scaling asserted           |
| 5       | Edge behavior (zero/negative/reuse) | Missing due collection failure | At least one edge case with explicit assertions |
| 6       | Failure-path test                   | Missing due collection failure | At least one exception-path assertion           |

**Expected Results:**

- **Without structured prompts:** often non-runnable output and missed gradient-order checks.
- **With structured prompts:** runnable tests that expose `axpy` contract violations.

**Measured Results:**

- Baseline prompt: collection/import failure.
- Guided prompt (phase 2): runnable suite, `2 passed / 4 failed`.

---

### Problem D_4: Bug-Fix Verification with Official Tests

**Evaluation Description:**  
Students fix starter-code bugs using their generated tests, then validate against official tests.

**Possible Bug Discovery Checklist:**

| Bug # | Description                                    | Actual Starter Behavior            | Expected Behavior                     |
| ----- | ---------------------------------------------- | ---------------------------------- | ------------------------------------- |
| 1     | Root backward ignores upstream gradient        | Uses `1.0` always                  | Uses provided upstream `grad`         |
| 2     | Multiplication second-input gradient wrong     | Misses chain factor                | Uses `out.grad * self.data`           |
| 3     | `__add__` grad propagation with constant wrong | Requires both inputs grad-enabled  | Requires grad if either input does    |
| 4     | `detach()` keeps grad tracking                 | Detached tensor still tracks grad  | Detached tensor should not track grad |
| 5     | `zero_grad()` reset policy wrong               | Sets grad to `None`                | Resets grad to `0.0`                  |
| 6     | `relu()` positive-slope bug (case 1)           | Uses slope `0.5`                   | Uses slope `1.0`                      |
| 7     | `relu()` positive-slope bug (case 2)           | Uses slope `0.5`                   | Uses slope `1.0`                      |
| 8     | `exp()` derivative wrong                       | Uses `x` instead of `exp(x)`       | Uses forward output `exp(x)`          |
| 9     | `axpy` backward gradient order mismatch        | Returns `(grad_x, grad_a, grad_y)` | Returns `(grad_a, grad_x, grad_y)`    |
| 10    | `clamp01` grad for `x < 0` wrong               | Returns `1`                        | Returns `0`                           |
| 11    | `clamp01` grad for `0 < x < 1` wrong           | Returns `0`                        | Returns `1`                           |
| 12    | `clamp01` grad for `x > 1` wrong               | Returns `1`                        | Returns `0`                           |

**Expected Results:**

- **Without structured prompts:** fixes target obvious failures but miss boundary/contract details.
- **With structured prompts:** fixes are more focused with fewer regressions.

**Measured Results:**

- Baseline patch: `14/18` official tests passed.
- Guided patch (phase 1): `10/18` official tests passed.
- Guided patch (phase 2): `14/18` official tests passed.

---

### Problem D: Guided vs. Unguided Summary

| Problem | Baseline Outcome              | Guided Outcome (Phase 2)         | Guided Better? |
| ------- | ----------------------------- | -------------------------------- | -------------- |
| D_1     | collection error              | runnable (`1 passed / 4 failed`) | Yes            |
| D_2     | collection error              | runnable (`2 passed / 4 failed`) | Yes            |
| D_3     | collection error              | runnable (`2 passed / 4 failed`) | Yes            |
| D_4     | `14/18` official tests passed | `14/18` official tests passed    | Tie            |

---

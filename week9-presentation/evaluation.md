# Week 9 Evaluation: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

## 1. General Evaluation Criteria

Students should evaluate their testing approach based on these criteria:

* **Bug Discovery Rate:** How effectively the tests identify defects in the code.
* **Test Coverage:** The extent to which tests cover critical paths, edge cases, and requirements.

---

## 2. Evaluation for Specific Example Problems

### Problem A: Checkout Service Testing

**Evaluation Description:**
Students should discover **all 9 intentional bugs** when applying both guidelines properly. A vague one-shot prompt will miss most bugs. The bugs span interacting features (item-level discounts, three coupon types, loyalty points, shipping) so only a prompt that explicitly decomposes each business rule and tests boundary/combination cases will uncover them all.

**Possible Bug Discovery Checklist:**

| Bug # | Description | Actual Behavior | Expected Behavior |
|-------|-------------|----------------|------------------|
| 1 | Empty cart is not validated | Proceeds to checkout with 0 subtotal, returns "success" | Raises `CheckoutError("Cart is empty")` |
| 2 | Stock check logic is inverted | Raises `CheckoutError` when item **is** in stock; allows checkout when out of stock | Raises `CheckoutError` only when item is **not** in stock |
| 3 | Bundle discount threshold off-by-one | Bundle 5% discount only triggers when `quantity > 3` (i.e., quantity 4+) | Should trigger when `quantity >= 3` (i.e., quantity 3+) |
| 4 | SUMMER20 cap logic inverted | Uses `max(20%, $30)` — gives a **minimum** $30 discount instead of a **maximum** $30 cap; no cap applied when 20% > $30 | Should use `min(20%, $30)` to cap at $30 |
| 5 | FLASH5 + VIP combination not blocked | VIP customers can use FLASH5 coupon and receive both discounts | Should raise `CheckoutError` when `FLASH5` is requested with a VIP customer |
| 6 | Tax calculated on pre-discount subtotal | Tax is `subtotal * 0.13` instead of `(discounted_subtotal - loyalty_credit) * 0.13` | Tax base must be the fully-discounted, loyalty-adjusted amount |
| 7 | Shipping threshold uses pre-discount subtotal | Free shipping granted when original `subtotal >= $50`, even if discounts bring it below | Should check `discounted_subtotal >= $50` |
| 8 | Payment failure not handled | `charge()` return value is ignored; checkout returns "success" even on payment failure | Raises `CheckoutError("Payment failed: <reason>")` when `charge()` returns `{"success": False, ...}` |
| 9 | Total not floored at zero | With a large enough discount + loyalty credit, `total` can be negative | `total = max(0.0, total)` |

**Expected Results:**
- **Without Guideline 3:** Test should find 0-4 bugs (mainly obvious ones)
- **With Guideline 3:** Test should find 6-9 bugs (comprehensive edge case coverage)

### Problem B_1: User Validation Testing

**Evaluation Description:** 
Students must identify bugs in the provided code. Using Guideline 3, they should find **at least 7 bugs**; the more bugs found, the better. 

You should compare bugs found using the checklist below with the bugs.

**Possible Bug Discovery Checklist:**

| Bug # | Description | Actual Behavior | Expected Behavior |
|-------|-------------|----------------|------------------|
| 1 | `validate_email()` does not raise a TypeError when given None | Returns None or fails silently | Raises TypeError for None input |
| 2 | Email validation allows consecutive dots | Accepts "user..name@domain.com" | Rejects emails with consecutive dots |
| 3 | Email validation allows consecutive special characters | Accepts "user.@name@domain.com" | Rejects emails with consecutive special characters |
| 4 | Email validation allows to start from special character | Accepts ".username@domain.com" | Rejects emails starting with special character |
| 5 | `validate_age()` has no upper and lower bound | Accepts age 999 and 0 | Restricts age to reasonable max  |
| 6 | `validate_username()` does not raise a TypeError when given None | Returns None or fails silently | Raises TypeError for None input |
| 7 | Username length validation off-by-one error | Accepts too short/long usernames | Enforces correct min/max length |
| 8 | Username can start with numbers | Accepts "1username" | Rejects usernames starting with numbers |
| 9 | Username can be all numbers | Accepts "123456" | Rejects usernames that are all numbers |
| 10 | `validate_password()` does not raise a TypeError when given None | Returns None or fails silently | Raises TypeError for None input |
| 11 | Password length validation off-by-one error | Accepts too short/long passwords | Enforces correct min/max length |
| 12 | Password validation missing special character check | Accepts passwords without special chars | Requires at least one special character |
| 13 | Password validation doesn't require uppercase letters | Accepts all lowercase passwords | Requires at least one uppercase letter |

**Expected Results:**
- **Without Guideline 3:** Should find 2-5 bugs (mainly obvious ones)
- **With Guideline 3:** Should find 7-13 bugs (comprehensive edge case coverage)

---

### Problem B_2: Order Processing Decomposition

**Evaluation Description:**  
Students must find **at least 7** intentional bugs hidden in the complex process_order() method by applying Guideline 4. 

Decomposition should reveal logical flaws that black-box testing misses. 

You should compare bugs found using the checklist below with the bugs.

**Possible Bug Discovery Checklist:**
| Bug # | Description | Actual Behavior | Expected Behavior |
|-------|-------------|----------------|------------------|
| 1 | Incomplete order validation | Missing checks for customer_id, items, payment_method | Validates all required fields |
| 2 | No validation for negative quantities or prices | Accepts negative values | Rejects negative quantities/prices |
| 3 | "FREEBIE" discount can make total negative | Total becomes negative | Ensures total is never negative |
| 4 | Invalid discount codes not handled | Ignores invalid codes | Raises error for invalid discount codes |
| 5 | Tax calculated on pre-discount amount | Calculates tax before discount | Calculates tax after discount |
| 6 | Free shipping logic broken | Charges shipping for orders > $100 | Free shipping for orders > $100 |
| 7 | Payment processing assumes success | No validation of payment | Validates payment and handles failures |
| 8 | Generic error handling loses important failure details | Returns generic error | Returns specific error details |
| 9 | Payment amount not validated | Accepts negative payment amounts | Rejects negative payment amounts |
| 10 | Unknown payment methods not properly rejected | Accepts unknown methods | Rejects unknown payment methods |

**Decomposition Quality Assessment:**
Students should identify these logical sub-behaviors:
1. Order data validation
2. Subtotal calculation
3. Discount application
4. Tax calculation  
5. Shipping cost determination
6. Payment processing
7. Order state updates
8. Result generation

**Expected Results:**
- **Without Guideline 4:** Should find 2-3 bugs (surface-level issues)
- **With Guideline 4:** Should find 7-10 bugs (through systematic behavior testing)

---

### Problem B_3: Data Parser Edge Cases

**Evaluation Description:**  
Students should discover ** at least 10 bugs** across multiple parsing functions when applying both Guidelines 3 and 4. 

You should compare bugs found using the checklist below with the bugs.

**Possible Bug Discovery Checklist:**

| Bug # | Description | Actual Behavior | Expected Behavior |
|-------|-------------|----------------|------------------|
| 1 | CSV: Crashes on None input | Throws error or fails silently | Handles None input gracefully |
| 2 | CSV: Doesn't handle empty string input | Throws error or returns invalid | Returns empty result or error |
| 3 | CSV: Fails on empty files or header-only files | Throws error or returns invalid | Handles empty/header-only files gracefully |
| 4 | CSV: Doesn't handle rows with missing fields | Ignores or crashes | Handles missing fields with error or default |
| 5 | CSV: Generic exception handling hides specific CSV errors | Returns generic error | Returns specific CSV error |
| 6 | JSON: Crashes on None input | Throws error or fails silently | Handles None input gracefully |
| 7 | JSON: Doesn't validate that parsed JSON is a dictionary | Accepts non-dict | Validates parsed object is dict |
| 8 | JSON: Required field validation continues instead of failing | Continues with missing fields | Fails if required fields missing |
| 9 | JSON: Unhelpful error messages for JSON decode errors | Returns generic error | Returns informative decode error |
| 10 | Numbers: Crashes on None input | Throws error or fails silently | Handles None input gracefully |
| 11 | Numbers: Doesn't handle empty string | Throws error or returns invalid | Returns empty result or error |
| 12 | Numbers: Regex doesn't capture negative numbers | Ignores negatives | Captures negative numbers |
| 13 | Numbers: Doesn't handle scientific notation | Ignores scientific notation | Captures scientific notation |
| 14 | Numbers: Fails on standalone dot "." | Throws error or returns invalid | Handles standalone dot gracefully |
| 15 | Numbers: Silently ignores conversion errors | Ignores errors | Reports conversion errors |
| 16 | Whitespace: Crashes on None input | Throws error or fails silently | Handles None input gracefully |
| 17 | Whitespace: Improper empty string handling | Throws error or returns invalid | Handles empty string gracefully |
| 18 | Whitespace: Line break preservation logic inverted | Breaks lines incorrectly | Preserves line breaks correctly |
| 19 | Whitespace: Doesn't handle all whitespace types | Ignores some whitespace types | Handles all whitespace types |
| 20 | Whitespace: Inappropriate stripping in some contexts | Strips needed whitespace | Strips only unnecessary whitespace |
| 21 | Data Types: No null checks | Ignores nulls | Checks for nulls |
| 22 | Data Types: Doesn't validate input is a dictionary | Accepts non-dict | Validates input is dict |
| 23 | Data Types: Missing fields silently ignored | Ignores missing fields | Reports missing fields |
| 24 | Data Types: Type checking logic flaws (inheritance, None handling) | Incorrect type checks | Correctly checks types, handles None |

**Expected Results:**
- **Without Guidelines 3 & 4:** Should find 3-6 bugs (mainly obvious input errors and crashes)
- **With Guidelines 3 & 4:** Should find 10-24 bugs (comprehensive edge case coverage across all parsing functions)




# Problem C


### GUIDED vs. UNGUIDED COVERAGE COMPARISON

**Unguided prompt**:

Write tests for app.py. Make sure they pass.

**Guided Prompt**:

*Step 1 prompt:*
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

*Step 2 prompt:*
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

*Step 3 prompt (after running pytest --tb=short -q):*
```
Here are the pytest failures:

<paste exact pytest output>

For each failure:
  1. Identify the root cause from the error message only
  2. Fix only the failing test — do not modify passing tests
  3. Regenerate only the fixed test methods
```

**Expected Results**:

| Metric            | Unguided | Guided |
|------------------:|---------:|-------:|
| Coverage %        | 28.3%    | 61.6%  |
| Covered lines     | 123      | 268    |
| Uncovered lines   | 312      | 167    |
| Tests passed      | 3        | 12     |
| Tests failed      | 0        | 1      |
| Passes threshold  | False    | True   |

---



## 3. Problem D Evaluation

### Problem D_1: Baseline Test Generation for Mini Autograd

**Evaluation Description:**  
Students generate an initial pytest suite for a pure-Python mini autograd engine and verify basic forward/backward behavior.

**Possible Behavior Discovery Checklist:**

| Check # | Description | Actual Baseline Behavior | Expected Behavior |
|-------|-------------|--------------------------|------------------|
| 1 | Runnable imports and collection | Import/collection error | Tests collect and run directly |
| 2 | Forward scalar assertions | Missing due collection failure | Deterministic forward-value checks |
| 3 | Backward checks for `+` and `*` | Missing due collection failure | Correct gradients asserted for both ops |
| 4 | Custom autograd function checks | Missing due collection failure | At least one custom op tested (forward/backward) |
| 5 | Output contract | Mixed prose/code in early runs | Single runnable test file, code-only |

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

| Check # | Description | Actual Baseline Behavior | Expected Behavior |
|-------|-------------|--------------------------|------------------|
| 1 | Shared-subgraph gradient accumulation | Missing due collection failure | Explicit accumulation assertions |
| 2 | `requires_grad` propagation | Missing due collection failure | Propagation behavior verified |
| 3 | `detach()` contract | Missing due collection failure | `requires_grad=False` + backward failure path |
| 4 | `zero_grad()` semantics | Missing due collection failure | Gradient reset behavior asserted |
| 5 | Boundary case in custom function | Missing due collection failure | At least one boundary-case gradient test |
| 6 | Negative/exception assertion | Missing due collection failure | At least one meaningful `pytest.raises` check |

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

| Check # | Description | Actual Baseline Behavior | Expected Behavior |
|-------|-------------|--------------------------|------------------|
| 1 | Forward check: `a*x + y` | Missing due collection failure | Deterministic forward assertion |
| 2 | Gradients for `a`, `x`, `y` | Missing due collection failure | Correct per-input gradient checks |
| 3 | Gradient-order contract | Missing due collection failure | Returned gradients mapped to input order |
| 4 | Upstream grad scaling | Missing due collection failure | `backward(grad=...)` scaling asserted |
| 5 | Edge behavior (zero/negative/reuse) | Missing due collection failure | At least one edge case with explicit assertions |
| 6 | Failure-path test | Missing due collection failure | At least one exception-path assertion |

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

| Bug # | Description | Actual Starter Behavior | Expected Behavior |
|-------|-------------|------------------------|------------------|
| 1 | Root backward ignores upstream gradient | Uses `1.0` always | Uses provided upstream `grad` |
| 2 | Multiplication second-input gradient wrong | Misses chain factor | Uses `out.grad * self.data` |
| 3 | `__add__` grad propagation with constant wrong | Requires both inputs grad-enabled | Requires grad if either input does |
| 4 | `detach()` keeps grad tracking | Detached tensor still tracks grad | Detached tensor should not track grad |
| 5 | `zero_grad()` reset policy wrong | Sets grad to `None` | Resets grad to `0.0` |
| 6 | `relu()` positive-slope bug (case 1) | Uses slope `0.5` | Uses slope `1.0` |
| 7 | `relu()` positive-slope bug (case 2) | Uses slope `0.5` | Uses slope `1.0` |
| 8 | `exp()` derivative wrong | Uses `x` instead of `exp(x)` | Uses forward output `exp(x)` |
| 9 | `axpy` backward gradient order mismatch | Returns `(grad_x, grad_a, grad_y)` | Returns `(grad_a, grad_x, grad_y)` |
| 10 | `clamp01` grad for `x < 0` wrong | Returns `1` | Returns `0` |
| 11 | `clamp01` grad for `0 < x < 1` wrong | Returns `0` | Returns `1` |
| 12 | `clamp01` grad for `x > 1` wrong | Returns `1` | Returns `0` |

**Expected Results:**
- **Without structured prompts:** fixes target obvious failures but miss boundary/contract details.
- **With structured prompts:** fixes are more focused with fewer regressions.

**Measured Results:**
- Baseline patch: `14/18` official tests passed.
- Guided patch (phase 1): `10/18` official tests passed.
- Guided patch (phase 2): `14/18` official tests passed.

---

### Problem D: Guided vs. Unguided Summary

| Problem | Baseline Outcome | Guided Outcome (Phase 2) | Guided Better? |
|-------|-------------------|--------------------------|----------------|
| D_1 | collection error | runnable (`1 passed / 4 failed`) | Yes |
| D_2 | collection error | runnable (`2 passed / 4 failed`) | Yes |
| D_3 | collection error | runnable (`2 passed / 4 failed`) | Yes |
| D_4 | `14/18` official tests passed | `14/18` official tests passed | Tie |

---


## 3. References

[1]  
[2] 

---


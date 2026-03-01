# Week 9 Guidelines: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

**Readings Assigned:**  
* Software Testing With Large Language Models: Survey, Landscape, and Vision [1]
* On the Evaluation of Large Language Models in Unit Test Generation [2]
* Software Testing with Large Language Models: An Interview Study with Practitioners [3]
* Using Large Language Models to Generate JUnit Tests: An Empirical Study [4]
* Evaluating and Improving ChatGPT for Unit Test Generation [5]
* Large Language Models for Software Testing: A Research Roadmap [6]

## Relevant Guidelines per Problem

| Question | Guidelines |
|---------|------------|
|   A | 1, 2 |
|   B_1| 3 |
|   B_2 | 4      |
|   B_3 |  3 , 4 |
|   С |  2, 4 (combined version in `notes.md`) |  
| D | 2, 3, 6 |
| D_1 | 2, 6 |
| D_2 | 2, 3, 6 |
| D_3 | 2, 3, 6 |
| D_4 | 2, 3|

## 1. Guidelines for Testing

### Guideline 1: Specify the Testing Goal and Scope in the Prompt
**Description:**  
When asking an LLM to generate or improve tests, explicitly state:
* test level (unit / integration / API / E2E),
* target function/module,
* expected behavior,
* constraints (framework, style, mocks, side effects),
* what not to test

**Reasoning:**  
Clear scope reduces ambiguity, so the model produces more relevant and accurate tests instead of generic or off-target output. LLM testing results depend heavily on prompt quality/prompt engineering and that prompt design [6].

**Good Example:**
```
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

**Bad Example:** 
```
Generate tests for this code.
```

---

### Guideline 2: Use a Generate–Validate–Repair Loop Instead of One-Shot Generation
**Description:**  
Adopt a QA workflow where LLM-generated tests go through an automated repair loop:
1. Generate tests
2. Compile and run
3. Parse failures (imports, mocks, wrong API usage, assertion mismatch)
4. Feed specific failure feedback back to the model
5. Regenerate/fix
6. Re-validate
Stop after a small number of iterations and escalate to human review.

**Reasoning:**  
A generate–validate–repair loop is more effective than  one-shot generation because test creation is an iterative quality-control task, not a single prediction task: even when generated output looks plausible, hidden issues such as incorrect assumptions, weak assertions, incompatibilities with the local codebase, or syntactic/runtime failures may remain undetected until execution and validation. Prior work shows that LLM-generated unit tests frequently suffer from compilation errors and execution/correctness issues, and that iterative refinement can improve outcomes [4], [5]. By explicitly validating the output and feeding back concrete failures, the process converts vague generation into a controlled refinement cycle, which improves reliability, reduces silent errors, and makes the final tests better aligned with actual behavior and project constraints [5].

**Good Example:**  
```
Running the tests produced these failures:

[ERROR COPIED]

Are these bugs in the tests or the implementation? Explain the root cause
and return a corrected test file. Do not modify checkout_service.py.
```

**Bad Example**
* Generating tests once, seeing compile errors, and discarding AI testing entirely.
* Re-prompting with “fix it” but without providing concrete error messages.
* Running infinite regeneration loops until something passes by chance.

---

### Guideline 3: Explicitly Request Boundary and Negative Cases, Strong Assertions

**Description:**  

Do not rely on the LLM to independently enumerate edge cases. In the prompt, explicitly require categories of non-happy-path tests with (ideally) minimum counts and strong assertions. At a minimum, request:

* Boundary values: min/max, zero, empty string/collection, single-element, off-by-one

* Null / missing inputs: null, absent keys/fields, optional values missing

* Invalid formats: malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding

* Exception/error paths: inputs that must trigger validation failures or thrown exceptions (use `pytest.raises` or equivalent)

* State/contract violations: precondition breaches, invalid state transitions (if applicable)

* Invariant/property checks: conditions that must always hold regardless of input

* Strong assertions: not just "test runs without crashing", but verify exact expected outputs, state changes, and side effects

**Reasoning:**  
LLMs usually generate "happy-path" tests first. They often don't invent the weird or extreme inputs that actually trigger validation errors and exception branches. The papers [2] [5] show that many bugs are missed because the tests don't hit those paths, so you need to tell the model directly to create boundary and negative cases.

**Example:**  

**Good Example:**
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

**Bad Example:**
```
“Write tests for `parseInvoice`. Make sure it covers the main cases and passes.”
```

##### P.S. The guideline and the prompt examples where rephrased and improved by GPT-4.1.
---

### Guideline 4: Decompose Complex Methods Before Asking for Tests

**Description:**  

If a method does multiple things (e.g., validate → transform → persist → log), don’t ask the LLM to “write tests” in one shot. Instead:
* Ask the LLM to identify the method’s logical sub-behaviors (a short list).
* Generate separate focused tests per sub-behavior (one responsibility per test group).
* Keep categories explicit inside each sub-behavior.

This keeps the model from mixing concerns and makes it easier to audit coverage.

**Reasoning:**  

When there are many responsibilities in one method, the model can lose track of what it’s testing and produce shallow or unfocused tests.  Wang et al. (IEEE Survey) [1] note that LLM test quality degrades significantly on long, multi-responsibility methods — the model loses track of which behavior it's testing. So this previous work [1] shows that prompt/context choices strongly affect test generation results.

**Example:**  

**Good Example:**

```
“Here is `processOrder(Order o)`.

Step 1: List the distinct behaviors in this method (validation rules, price calculation, discount logic, persistence, error handling).

Step 2: For each behavior, generate **JUnit 5** tests focusing only on that behavior.

Step 3: For each behavior, include boundary + negative cases (nulls, invalid inputs, exception paths).

Constraints: don’t test DB/network; use mocks; clear assertions.”
```

**Bad Example:**
```
“Write tests for `processOrder`. Generate unit tests for processOrder(Order o) that ensure it works correctly. Cover the main functionality and make sure the tests pass. Use standard assertions.”
```
##### P.S. The guideline and the prompt examples where rephrased and improved by GPT-4.1.
---



### Guideline 6: Specify Testing Scope and Execution Contract in the Prompt
**Description:**  
When asking an LLM to generate tests, always define:
* target module/function,
* test framework (`pytest`, `JUnit`),
* required behavior categories (happy path, boundaries, failures),
* import root/path assumptions,
* output format (code-only, single file),
* strict constraints (do not edit implementation files).

**Reasoning:**  
Prompt quality strongly affects test quality and executability [1], [2], [5], [6]. Explicit execution constraints reduce non-runnable output and improve reproducibility in team evaluation settings [9].

**Good Example:**
```text
Generate pytest tests for `billing/discounts.py::apply_coupon`.
Assume execution from repository root.
Use: `from billing.discounts import apply_coupon`.
Include: happy path + boundary values + invalid-input exceptions.
Do not modify implementation files. Return one runnable test file only.
```

**Bad Example:**
```text
Write tests for this file. Make sure they pass.
```

---

## 2. References

[1] Wang, J., et al. "Software Testing with Large Language Models: Survey, Landscape, and Vision" IEEE Transactions on Software Engineering (2024). DOI: 10.1109/TSE.2024.3368208.

[2] Yang, L., et al. "On the Evaluation of Large Language Models in Unit Test Generation" Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE) (2024). DOI: 10.1145/3691620.3695529.

[3] Santana, M. D., Magalhaes, C., and de Souza Santos, R. "Software Testing with Large Language Models: An Interview Study with Practitioners" AIware 2025 (2025).

[4] Siddiq, M. L., et al. "Using Large Language Models to Generate JUnit Tests: An Empirical Study" (2024). DOI: 10.1145/3661167.3661216.

[5] Yuan, Z., et al. "Evaluating and Improving ChatGPT for Unit Test Generation" Proceedings of the ACM on Software Engineering 1(FSE), 1703–1726 (2024). DOI: 10.1145/3660783.

[6] Augusto, C., Bertolino, A., De Angelis, G., Lonetti, F., and Morán, J. "Large Language Models for Software Testing: A Research Roadmap" arXiv preprint (2025).

[7] pytest docs: Assertions and expected exceptions (`https://docs.pytest.org/en/stable/how-to/assert.html`).

[8] Python docs: `py_compile` (`https://docs.python.org/3/library/py_compile.html`).

[9] GitHub Docs: Adding repository custom instructions for GitHub Copilot (`https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions`).

---


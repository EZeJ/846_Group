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
|   С |  5 |
| D | 6, 7, 8 |
| D_1 | 6, 7 |
| D_2 | 6, 7, 8 |
| D_3 | 6, 7, 8 |
| D_4 | 7, 8 |


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

### Guideline 3: Explicitly Request Boundary and Negative Test Cases 

**Description:**  

Do not rely on the LLM to independently enumerate edge cases. In the prompt, explicitly require categories of non-happy-path tests and (ideally) minimum counts. At a minimum, request:

* Boundary values: min/max, zero, empty string/collection, single-element, off-by-one

* Null / missing inputs: null, absent keys/fields, optional values missing

* Invalid formats: malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding

* Exception/error paths: inputs that must trigger validation failures or thrown exceptions

* State/contract violations: precondition breaches, invalid state transitions (if applicable)

**Reasoning:**  
LLMs usually generate “happy-path” tests first. They often don’t invent the weird or extreme inputs that actually trigger validation errors and exception branches. The papers [2] [5] show that many bugs are missed because the tests don’t hit those paths, so you need to tell the model directly to create boundary and negative cases.

**Example:**  

**Good Example:**
```
“Generate **JUnit 5 unit tests** for `parseInvoice(String json)`.

Required categories (at least **2 tests each**):

1. Boundary: empty string, very large numeric fields, empty items list
2. Null/Missing: missing required keys (`invoiceId`, `items`), null values where allowed/disallowed
3. InvalidFormat: malformed JSON, wrong field types (string instead of number)
4. ExceptionPath: inputs that must throw `InvalidInvoiceException`
    
Constraints: no database/network; use parameterized tests”
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

### Guideline 5: Use a structured 3-step prompt to maximise test coverage

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

### Guideline 7: Use a Generate–Validate–Repair Loop Instead of One-Shot Generation
**Description:**  
Treat generated tests as drafts:
1. generate test code,
2. run syntax/import gate (`py_compile`, `pytest --collect-only`),
3. run tests and capture short failures,
4. ask for targeted fixes to failing parts only,
5. re-run with bounded iterations.

**Reasoning:**  
Empirical work and practitioner reports show one-shot outputs often contain execution and assertion issues; iterative repair materially improves usefulness [3], [4], [5], [7], [8].

**Good Example:**
```text
These tests fail with:
[PASTE SHORT TRACEBACK]

Patch only failing tests/imports.
Do not rewrite passing tests.
Do not edit implementation code.
Return code only.
```

**Bad Example:**
```text
Fix it.
```

---

### Guideline 8: Require Strong Coverage + Strong Assertions, Then Verify with an Independent Suite
**Description:**  
Require both coverage breadth and assertion strength:
* boundary values and off-by-one cases,
* null/missing and malformed inputs,
* explicit exception-path checks (`pytest.raises`),
* invariant/property checks where applicable.

Then verify against an independent oracle (official tests, hidden grader, or reference suite).

**Reasoning:**  
LLM-generated suites often overfit happy paths and miss critical failure behavior [2], [5]. Independent verification is needed to avoid false confidence from weak or redundant assertions [1], [6].

**Good Example:**
```text
For `parse_record`, include:
- 2 boundary tests,
- 2 malformed-input tests with `pytest.raises`,
- 1 invariant test.

After generation, run the independent grader and report missed categories.
```

**Bad Example:**
```text
Generate a few basic tests that run.
```


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


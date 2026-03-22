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
|   D | 5, 6, 7 |
|   D_1 | 5, 6, 7 |
|   D_2 | 5, 6, 7 |
|   D_3 | 5, 6, 7 |
|   D_4 | 5, 6, 7 |

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

### Guideline 3: Explicitly Request Boundary and Negative Cases, Strong Assertions — Aligned with the Code's Contract

**Description:**

When asking an LLM to generate tests, explicitly require categories of non-happy-path tests with minimum counts and strong assertions. At a minimum, request:

- **Boundary values:** min/max, zero, empty string/collection, single-element, off-by-one
- **Null / missing inputs:** null, absent keys/fields, optional values missing
- **Invalid formats:** malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding
- **Exception/error paths:** inputs that must trigger validation failures or thrown exceptions (use `pytest.raises` or equivalent)
- **Invariant/property checks:** conditions that must always hold regardless of input
- **Strong assertions:** verify exact expected outputs, state changes, and side effects — not just "test runs without crashing"

**Critical addition:** Only request edge-case categories that the code is actually designed to handle. Before listing categories, review the function's documented contract or spec. If the code does not validate a certain input (e.g., `None` owner, negative initial balance), do not generate tests asserting behavior for that case — these become false alarms and obscure real coverage gaps.

Additionally, generic category labels (null, boundary) are a starting point only. For each function, also consider **domain-specific weird inputs** that the generic list does not cover: Unicode characters, `NaN`/`inf` floats, floating-point precision quirks, locale-sensitive formats, idempotency under repeated application, and similar domain-relevant edge cases.

**Reasoning:**

LLMs default to happy-path tests and rarely invent the extreme or domain-specific inputs that trigger validation errors and exception branches [2][5]. Explicitly requesting categories forces coverage. However, if categories are applied without checking the code's contract, the LLM generates tests for non-existent validation logic, producing false failures that waste debugging time. Student work showed that for a bank module with no input validation, applying the original guideline produced four failing tests asserting behavior the code never claimed to have — the tests were wrong, not the code. The same work showed that domain-specific edge cases (Unicode normalization, `NaN`/`inf`, sign of `-0.0`, float rounding) must be named explicitly to be covered; the LLM will not invent them from a generic category label.

**Example:**

**Good:**
```
Generate pytest tests for `calculate_discount(price, discount_pct)` in `example.py`.

Contract (from docstring): discount_pct must be in [0, 100]; raises ValueError otherwise.
price has no documented validation — do NOT invent tests for invalid price types.

Required categories (aligned with contract):
1. Boundary: discount_pct = 0 and 100 exactly; off-by-one values -1 and 101
2. Exception paths: discount_pct outside [0, 100] must raise ValueError

Use @pytest.mark.parametrize. Strong assertions on every test.
Return one runnable pytest file only.
```

**Bad:**
```
Write tests for calculate_discount. Cover null inputs, boundary values, and exception paths.
```

---
* The description was improved by refining my thoughts and structure in GitHub Copilot.
---

### Guideline 4: Decompose Complex Methods Before Asking for Tests — Match Structure to Complexity, Then Add Pipeline Integration Tests

**Description:**

Before decomposing, assess whether the method genuinely has multiple distinct responsibilities.

**Single-responsibility code** (one clear behavior, no distinct steps):
Do **not** decompose. Just ask for focused tests with boundary and negative cases (Guideline 3). If you ask the LLM to "list distinct behaviors" on simple code, it will invent them — and miss the real bugs.

**Rule of thumb:** If you cannot write 2–3 distinct sentences describing what the method does, skip decomposition.

**Multi-responsibility code** (validate → compute → persist → log):
Apply three steps:

1. Ask the LLM to identify distinct sub-behaviors.
2. Generate focused tests per sub-behavior with boundary and negative cases.
3. **Generate integration tests.** Run steps together and check that values flow correctly between them. Cover two cases:
   - A value updated in one step is actually used by the next (stale variable).
   - A rule changes an intermediate value that another rule uses as a threshold (rule interaction). Include at least one threshold-crossing test.

**Reasoning:**

We found two problems with the original guideline. First, it does not say when *not* to decompose. If you ask the model to list distinct behaviors for a simple function, it will invent them. It creates fake sub-behaviors, adds tests for inputs the function never handles, and misses the actual bugs. Second, decomposition alone is not enough for multi-step methods. In multiple problems, all unit tests passed but the bug was still there — because it lived between steps, not inside one. These bugs only showed up when we tested the steps running together [1].

**Example:**

**Good (multi-responsibility — apply decomposition + pipeline integration):**
```
Here is `process_reorder(...)` with six sequential steps:
  1. Reorder decision
  2. Quantity calculation
  3. Volume discount lookup
  4. Cost computation
  5. Safety-stock adjustment
  6. Approval check

Step 1: List the distinct behaviors in this method.

Step 2: Generate focused pytest tests for each behavior and
include boundary and negative cases within each group.

Step 3: Generate integration tests that run steps together.
- Add a test where safety-stock (Step 5) bumps the quantity, and assert that
  cost fields (Step 4) and approval flag (Step 6) reflect the new quantity.
- Add a test where a discount changes an intermediate value that a later step
  uses as a threshold — assert the later step uses the updated value.

Constraints: do not modify source code.
```

**Bad (single-responsibility — do not decompose):**
```
List the distinct behaviors in clamp(value, lo, hi) and generate separate test groups for each.
```

**Bad (multi-responsibility — decomposition without integration):**
```
Here is process_order(db, order).
Step 1: List the distinct behaviors.
Step 2: Generate focused tests for each behavior.
```
---
* The description was improved by refining my thoughts and structure in GitHub Copilot.
---

### Guideline 5: Use a Fault Model (Mutation Mindset) to Drive Test Adequacy
**Description:**  
Instead of asking an LLM for “more tests”, define a short **fault model** (plausible bug classes) and require at least one test that would fail for each bug class. Treat “mutants” as plausible wrong implementations when mutation tooling is unavailable, and label each test by the fault-model item it targets.

**Reasoning:**  
LLM-generated tests can run successfully but still miss defect-revealing behaviors. The readings emphasize adequacy tied to bug detection (including mutation-oriented thinking), not just execution success [1], [2], [5], [6]. A fault model makes it explicit what the tests must distinguish.

**How to apply (checklist):**
* Write 6–10 fault-model items (plausible “near-correct” bugs), not vague goals.
* Make each item testable: “if this bug exists, what observable behavior changes?”
* Require **at least one explicit assertion per item** (value, exception, state/side-effect).
* Prefer minimal counterexamples (small scalars/small arrays) so failures are easy to debug.
* Add a short tag/comment in each test (e.g., `# targets: FM3 swapped-arg-order`) so adequacy is auditable.

**Prompt template (copy/paste):**
```text
Generate pytest unit tests for <TARGET> (file/function/class below).

Contract (what is correct): <1–5 bullets>.

Fault model (each must be “killed” by ≥1 test):
- FM1: <plausible wrong behavior>
- FM2: <plausible wrong behavior>
...

Requirements:
- For each FM*, include at least one test with a clear assertion that would FAIL if FM* exists.
- Add a comment `# targets: FM*` in each test.
- Use small inputs and deterministic assertions.
- Return code only.
```

**Good Example:**
```text
Fault model (general examples):
- off-by-one at boundary (e.g., `<=` vs `<`)
- wrong exception type or missing exception
- swapped argument order / wrong return ordering
- missing scaling factor / sign error

Fault model (Problem D / mini-autograd examples):
- missing chain-rule factor in backward
- gradient order swapped vs inputs
- requires-grad propagation too strict/too loose
- detach does not stop gradient tracking
- wrong boundary derivative (e.g., clamp-like op)

Requirement: add at least one test that would fail for each item above.
```

**Bad Example:**
```text
Write several tests that call the function and check it does not crash.
```

#### Problem D Showcase (D_2, D_3)
Problem D is intentionally full of “near-correct” gradient bugs in `ProblemD/student/src/mini_autograd.py` and `ProblemD/student/src/demo_custom_functions.py`, so a fault model is an efficient way to force discriminative tests.

```text
Fault model to kill (Problem D):
- FM1: Tensor.backward(grad=...) ignores the explicit upstream grad argument
- FM2: add() sets requires_grad with AND instead of OR (mixing tensor + constant)
- FM3: mul() backward misses upstream scaling for one operand (chain rule factor)
- FM4: shared subgraph does not accumulate grads (x used twice only counts once)
- FM5: detach() returns a tensor that still requires grad / participates in backprop
- FM6: zero_grad() resets grad to None instead of 0.0 (breaks repeated backward)
- FM7: relu() backward uses wrong slope for x>0 (should be 1.0)
- FM8: exp() backward uses x instead of exp(x) as derivative
- FM9: Axpy.backward returns grads in wrong order (a/x swapped)
- FM10: Clamp01.backward returns grad_out outside (0,1) and 0 inside (inverted)

Requirement: one pytest test per FM*, each tagged `# targets: FM*`,
with an explicit assertion that would FAIL if FM* exists.
```

**Why it helped:** it prevented “smoke tests” and forced tests to kill specific plausible bugs (especially gradient scaling, ordering, and accumulation).

---

### Guideline 6: Use a Prompt Card + Run Record (Traceability Protocol)
**Description:**  
For every AI-assisted test run, record:
* model name + version,
* prompt ID + exact prompt (or prompt-file path),
* target code under test,
* run command,
* generated artifact paths,
* 1-line outcome summary.

**Reasoning:**  
Small prompt/context changes can materially change generated tests. Tooling guidance encourages prompt files and repository instructions to make outcomes reproducible and comparable across a team [10], [9]. A minimal record makes evaluation fair and debuggable.

**How to apply (checklist):**
* Save the prompt text in a file (not only in chat history), e.g., `prompt_<ID>.txt`.
* Save generated tests as a separate artifact, e.g., `generated_<ID>_tests.py`.
* Save the run output (`pytest -q ...`) as a log (or paste it into notes) so you can compare runs.
* Keep “run records” short: enough to reproduce the run in < 1 minute.

**Prompt Card template:**
```text
Prompt ID:
Model:
Target:
Prompt (saved):
Command:
Artifacts:
Result summary:
Notes:
```

**Good Example:**
```text
Prompt ID: D2_graph_semantics_v1
Model: Copilot CLI gpt-5-mini (2026-02-27)
Target: ProblemD/student/src/mini_autograd.py::Tensor.backward (graph semantics)
Prompt (saved): exact prompt text captured for reruns
Command: pytest -q <generated_test_file>
Artifacts: <generated_test_file>; <pytest_log>
Result: 2 passed, 4 failed (useful failing signals)
```

**Bad Example:**
```text
I generated tests yesterday; I don’t remember the prompt or model version.
```

#### Problem D Showcase (D_1, D_4)
In Problem D, we got more runnable and comparable outputs by pinning the output contract and imports, and by recording a minimal run record (prompt + command + result summary).

```text
Output contract:
- return one runnable Python pytest file only (no prose / no markdown fences)

Use these imports (exactly):
from ProblemD.student.src.mini_autograd import Tensor, Function
from ProblemD.student.src import demo_custom_functions as custom

Run record (fill during the run):
Prompt ID: <short name>
Model: <model + version>
Target: mini_autograd.py and/or demo_custom_functions.py
Prompt (saved): <exact prompt text captured>
Command: pytest -q <generated_test_file>
Result summary: <X passed, Y failed>
```

**Why it helped:** it reduced “non-runnable” generations (wrong imports/prose output) and made baseline vs guided comparisons reproducible.

---

### Guideline 7: Counterexample-First Prompting to Generate Discriminative Tests
**Description:**  
Before generating final tests, first ask the model to propose plausible wrong variants and minimal counterexamples. Then generate tests that pass for the intended contract and would fail for each wrong variant.

**Reasoning:**  
Counterexample-first prompts force the model to surface discriminators and reduce tests that accidentally pass buggy implementations. This matches findings that LLM-generated tests can be shallow/misaligned and that prompt structure affects test effectiveness [1], [2], [5]. This is especially useful when multiple near-correct variants exist (e.g., correct forward but wrong backward order).

**How to apply (2-step sequence):**
1. **Enumerate wrong variants + counterexamples** (no test code yet). Ask for a short table: `wrong_variant | symptom | minimal inputs`.
2. **Generate tests from that table.** Require one test per wrong variant, each tagged with the variant it targets.

**Counterexample-first prompt (copy/paste):**
```text
You are helping me write discriminative pytest unit tests.

Target: <FUNCTION or METHOD>.
Contract summary: <1–5 bullets>.

Task: list 4–6 plausible wrong variants that are easy to accidentally implement.
For each wrong variant, provide the smallest counterexample inputs that would expose it.
Return a table: wrong_variant | symptom | counterexample_inputs.
```

**Discriminative test prompt (copy/paste):**
```text
Using the table above, write pytest tests such that:
1) they pass for the intended contract, and
2) each test would fail for its corresponding wrong_variant.

Constraints:
- Prefer minimal inputs from the table.
- Add a comment `# targets: <wrong_variant>` per test.
- Return code only.
```

**Good Example:**
```text
Step 1: List 4 plausible wrong variants and minimal counterexamples.
Step 2: Write pytest tests that would fail for each wrong variant.
Return code only.
```

**Bad Example:**
```text
Generate tests without considering how a buggy-but-plausible implementation might still pass.
```

#### Problem D Showcase (D_2, D_3)
In Problem D, counterexample-first prompting is a fast way to get discriminative gradient tests (small numeric inputs, strong assertions) for both graph semantics and custom ops.

```text
List wrong variants + minimal counterexamples (examples):
- V1 (upstream grad ignored):
  out = (Tensor(2.0, True) * 3.0); out.backward(4.0) => x.grad == 12.0
- V2 (mul missing chain factor):
  x=2.0,y=3.0; out=(x*y)*4.0; out.backward() => x.grad==12.0,y.grad==8.0
- V3 (shared-subgraph not accumulated):
  x=3.0; out=(x*x)+x; out.backward() => x.grad == 7.0
- V4 (axpy grad order wrong):
  a=2.0,x=3.0,y=4.0; out=axpy(a,x,y); out.backward() => (a=3,x=2,y=1)
- V5 (clamp01 boundary derivative wrong):
  x in {-0.25, 0.25, 1.5}; grads should be {0.0, 1.0, 0.0}

Then: write one pytest test per V*, tagged `# targets: V*`, return code only.
```

**Why it helped:** it pushed the model to propose discriminators first, then encode them as assertions, reducing tests that accidentally pass buggy implementations.

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

[10] GitHub Docs: Prompt files for GitHub Copilot (`https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files`).

---


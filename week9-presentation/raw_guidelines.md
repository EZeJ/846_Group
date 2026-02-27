# Week 9 Raw Guidelines: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia
**Readings Assigned:**  
* Software Testing With Large Language Models: Survey, Landscape, and Vision [1]
* On the Evaluation of Large Language Models in Unit Test Generation [2]
* Software Testing with Large Language Models: An Interview Study with Practitioners [3]
* Using Large Language Models to Generate JUnit Tests: An Empirical Study [4]
* Evaluating and Improving ChatGPT for Unit Test Generation [5]
* Large Language Models for Software Testing: A Research Roadmap [6]

## 1. Guidelines from Readings
### Guideline 1.1: Explicitly Request Boundary and Negative Test Cases

**Description:**  
Do not rely on the LLM to independently enumerate edge cases. In the prompt, explicitly require categories of non-happy-path tests and (ideally) minimum counts. At a minimum, request:

* Boundary values: min/max, zero, empty string/collection, single-element, off-by-one
* Null / missing inputs: null, absent keys/fields, optional values missing
* Invalid formats: malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding
* Exception/error paths: inputs that must trigger validation failures or thrown exceptions
* State/contract violations: precondition breaches, invalid state transitions (if applicable)

**Reasoning:**  
LLMs default to generating "happy-path" tests first and often fail to invent the weird or extreme inputs that trigger validation errors and exception branches. Yuan et al. [5] show that ChatGPT-generated tests suffer from low branch coverage precisely because edge cases are not exercised; Yang et al. [2] confirm that LLM-generated test suites miss many bugs due to insufficient boundary and null-input coverage. Wang et al. [1] further note that prompt design choices — including whether edge-case categories are named explicitly — are among the strongest determinants of final test quality.

**Example:**

*Good prompt:*
```
"Generate JUnit 5 unit tests for `parseInvoice(String json)`.

Required categories (at least 2 tests each):
1. Boundary: empty string, very large numeric fields, empty items list
2. Null/Missing: missing required keys (`invoiceId`, `items`), null values where allowed/disallowed
3. InvalidFormat: malformed JSON, wrong field types (string instead of number)
4. ExceptionPath: inputs that must throw `InvalidInvoiceException`

Constraints: no database/network; use parameterized tests"
```

*Bad prompt:*
```
"Write tests for `parseInvoice`. Make sure it covers the main cases and passes."
```

---

### Guideline 1.2: Decompose Complex Methods Before Asking for Tests

**Description:**  
If a method does multiple things (e.g., validate → transform → persist → log), do not ask the LLM to "write tests" in one shot. Instead:

* Ask the LLM to identify the method's logical sub-behaviors (a short list).
* Generate separate focused tests per sub-behavior (one responsibility per test group).
* Keep boundary/negative categories explicit inside each sub-behavior.

This keeps the model from mixing concerns and makes it easier to audit coverage.

**Reasoning:**  
Wang et al. [1] note that LLM test quality degrades significantly on long, multi-responsibility methods — the model loses track of which behavior it is testing and produces shallow, overlapping, or redundant assertions. Yuan et al. [5] observe the same pattern: tests for complex methods generated in a single prompt tend to cluster around the most visible code path and miss internal branching logic entirely. Decomposing first forces the LLM to treat each sub-behavior as an independent unit under test, which directly maps to how well-structured unit tests should be written.

**Example:**

*Good prompt:*
```
"Here is `processOrder(Order o)`.

Step 1: List the distinct behaviors in this method (validation rules, price
        calculation, discount logic, persistence, error handling).

Step 2: For each behavior, generate JUnit 5 tests focusing only on that behavior.

Step 3: For each behavior, include boundary + negative cases
        (nulls, invalid inputs, exception paths).

Constraints: don't test DB/network; use mocks; clear assertions."
```

*Bad prompt:*
```
"Write tests for `processOrder`. Generate unit tests for processOrder(Order o)
that ensure it works correctly. Cover the main functionality and make sure the
tests pass. Use standard assertions."
```

---

### Guideline 1.3: Provide the Full Method Signature and Contract, Not Just the Name

**Description:**  
When prompting an LLM to generate tests, always include the complete method signature, its documented pre- and post-conditions, and any relevant type information. Do not refer to the method by name alone and expect the model to infer its contract.

**Reasoning:**  
Yang et al. [2] identify "insufficient context" as one of the primary causes of incorrect or vacuous LLM-generated tests — when the model does not know what a function is supposed to do, it writes tests that merely assert the function runs without error rather than verifying its actual contract. Yuan et al. [5] show that adding explicit contract information (parameter types, expected exceptions, return semantics) to the prompt significantly increases the number of meaningful assertions in the output. Wang et al. [1] classify context richness as a key prompt-quality dimension that directly predicts test correctness.

**Example:**

*Good prompt:*
```
"Generate pytest tests for this function:

def calculate_discount(price: float, code: str) -> float:
    \"\"\"
    Apply a discount code to a price.
    - price must be > 0; raises ValueError otherwise
    - code must be one of: 'SAVE10', 'SAVE20'; raises ValueError for unknown codes
    - returns the discounted price (never negative)
    \"\"\"
```

*Bad prompt:*
```
"Write tests for calculate_discount."
```
---

### Guideline 1.4: Use a structured 3-step prompt to maximise test coverage

**Description:**
Instead of asking an LLM to generate tests in one shot, use a fixed three-step prompt sequence that combines scope, intention, decomposition, edge cases, and a repair loop:

**Step 1 — Describe intention per behavior group (no code yet)**
Scope the target module into its distinct behavior groups, then ask the LLM to describe the intended behavior of each group.

**Step 2 — Generate tests using the description**
For every described behavior, branch, and edge case require different types of tests.

Also, include explicit constraints, like test framework, what not to test, and how methods must be invoked.

**Step 3 — Repair failures**
Ask LLM to fix only the failing tests (not the code) using only the error message as evidence.

**Reasoning:**
- Without intention-first, it writes assertions that misrepresent actual behavior — over 85% of execution failures stem from incorrect assertions, not bugs [5]
- Without decomposition, it loses track of responsibilities in large modules


## 2. Guidelines from from any related research/grey literature like practitioner or developer tool blogs

### Guideline 1: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).

---

### Guideline 2: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

## 3. Guidelines from LLMs

### Guideline 1: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).

---

### Guideline 2: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)


## 4. Problem D Raw Guidelines

### 4.1 Guidelines from Readings

#### Guideline 4.1.1: Explicitly Require Boundary, Negative, and Exception Tests
**Description:**  
In the first prompt, explicitly request non-happy-path categories:
* boundaries (min/max/empty/off-by-one),
* null/missing fields,
* malformed input,
* exception-triggering inputs.

**Reasoning:**  
Assigned readings show LLMs default to easy happy-path tests and miss bug-revealing inputs unless these categories are required explicitly [1], [2], [5].

**Example:**
*Good prompt:*  
```text
Generate pytest tests for `parse_invoice`.
Include: 2 boundary tests, 2 malformed-input tests, and 2 exception-path tests.
Return code only.
```
*Bad prompt:*  
```text
Write tests for parse_invoice.
```

---

#### Guideline 4.1.2: Decompose Complex Functions Before Test Generation
**Description:**  
Use a two-step workflow for large functions:
1. ask the model to list behavior groups,  
2. generate tests per behavior group.

**Reasoning:**  
For multi-responsibility functions, one-shot generation reduces focus and branch coverage. Decomposition improves alignment between behavior and assertions [1], [5], [6].

**Example:**
*Good prompt:*  
```text
Step 1: List behavior groups in `process_order` (validation, pricing, discount, errors).
Step 2: Generate pytest tests per group, including one boundary and one failure case each.
```
*Bad prompt:*  
```text
Generate all tests for process_order in one shot.
```

---

### 4.2 Guidelines from Related Research / Grey Literature

#### Guideline 4.2.1: Gate on Syntax and Collection Before Semantic Debugging
**Description:**  
Run a lightweight executability gate first:
* `python -m py_compile <test_file.py>`
* `pytest --collect-only -q <test_file.py>`

Then repair imports/syntax/path issues before assertion tuning.

**Reasoning:**  
Practitioner workflows emphasize isolating structural failures early to avoid wasting iterations on semantic debugging when tests cannot run [7], [8].

**Example:**
*Good prompt:*  
```text
Collection fails with ImportError.
Patch only imports/path assumptions. Keep assertions unchanged.
```
*Bad prompt:*  
```text
Ignore import errors; focus on expected values first.
```

---

#### Guideline 4.2.2: Standardize Prompt Constraints at Repository Level
**Description:**  
Define shared constraints once for the team (framework, output format, forbidden edits, deterministic inputs) and reuse in every prompt.

**Reasoning:**  
Repository-level instructions reduce prompt drift and improve comparability during class-wide evaluation [9].

**Example:**
*Good prompt header:*  
```text
Team constraints:
- pytest only
- one code file, no prose
- do not edit implementation
- include happy, edge, and failure tests
```
*Bad prompt header:*  
```text
No team constraints; each student writes ad-hoc prompts.
```

---

### 4.3 Guidelines from LLM Prompting Interactions

**Model(s) used:** GitHub Copilot CLI (`gpt-5-mini`) and GPT-5.2 (Codex CLI)  
**Prompt interaction pattern:** baseline prompt → constrained prompt → failure-log repair prompt

#### Guideline 4.3.1: Force Code-Only Output with Fixed Import Root
**Description:**  
Constrain output and imports:
* code-only response,
* fixed project-root import style,
* no command execution in response,
* no implementation edits.

**Reasoning:**  
In our runs, non-runnable output (mixed prose/code, wrong imports) was a frequent failure source. Tight output constraints improved executability and scoring consistency.

**Example:**
*Good prompt:*  
```text
Return one runnable pytest file only.
Assume repository-root execution.
Use `from package.module import ...`.
No markdown fences and no prose.
```
*Bad prompt:*  
```text
Explain your approach first, then provide test ideas.
```

---

#### Guideline 4.3.2: Use Failure-Scoped Repair Prompts (Minimal Diff)
**Description:**  
After a failed run, request a minimal patch to only failing imports/tests/assertions instead of regenerating the full suite.

**Reasoning:**  
Failure-scoped repair preserved passing tests and reduced regressions during iterative refinement.

**Example:**
*Good prompt:*  
```text
Here is the failing traceback:
[PASTE SHORT LOG]
Patch only failing tests/imports. Do not rewrite passing tests.
```
*Bad prompt:*  
```text
Rewrite the entire test suite from scratch.
```

---

## 4. References

[1] Wang, J., et al. "Software Testing with Large Language Models: Survey, Landscape, and Vision" IEEE Transactions on Software Engineering (2024). DOI: 10.1109/TSE.2024.3368208.

[2] Yang, L., et al. "On the Evaluation of Large Language Models in Unit Test Generation" Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE) (2024). DOI: 10.1145/3691620.3695529.

[3] Santana, M. D., Magalhaes, C., and de Souza Santos, R. "Software Testing with Large Language Models: An Interview Study with Practitioners" AIware 2025 (2025).

[4] Siddiq, M. L., et al. "Using Large Language Models to Generate JUnit Tests: An Empirical Study" (2024). DOI: 10.1145/3661167.3661216.

[5] Yuan, Z., et al. "Evaluating and Improving ChatGPT for Unit Test Generation" Proceedings of the ACM on Software Engineering 1(FSE), 1703–1726 (2024). DOI: 10.1145/3660783.

[6] Augusto, C., Bertolino, A., De Angelis, G., Lonetti, F., and Morán, J. "Large Language Models for Software Testing: A Research Roadmap" arXiv preprint (2025).

[7] pytest docs: Good integration practices (`https://docs.pytest.org/en/stable/explanation/goodpractices.html`).

[8] Python docs: `py_compile` (`https://docs.python.org/3/library/py_compile.html`).

[9] GitHub Docs: Adding repository custom instructions for GitHub Copilot (`https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions`).

---





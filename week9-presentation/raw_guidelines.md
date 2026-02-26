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

## 2. Guidelines from from any related research/grey literature like practitioner or developer tool blogs

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

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

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

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

## 4. References

[1] Wang, J., et al. "Software Testing with Large Language Models: Survey, Landscape, and Vision" IEEE Transactions on Software Engineering (2024). DOI: 10.1109/TSE.2024.3368208.

[2] Yang, L., et al. "On the Evaluation of Large Language Models in Unit Test Generation" Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE) (2024). DOI: 10.1145/3691620.3695529.

[3] Santana, M. D., Magalhaes, C., and de Souza Santos, R. "Software Testing with Large Language Models: An Interview Study with Practitioners" AIware 2025 (2025).

[4] Siddiq, M. L., et al. "Using Large Language Models to Generate JUnit Tests: An Empirical Study" (2024). DOI: 10.1145/3661167.3661216.

[5] Yuan, Z., et al. "Evaluating and Improving ChatGPT for Unit Test Generation" Proceedings of the ACM on Software Engineering 1(FSE), 1703–1726 (2024). DOI: 10.1145/3660783.

[6] Augusto, C., Bertolino, A., De Angelis, G., Lonetti, F., and Morán, J. "Large Language Models for Software Testing: A Research Roadmap" arXiv preprint (2025).

---


---


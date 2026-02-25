# Week 9 Guidelines: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia
**Readings Assigned:**  
* Software Testing With Large Language Models: Survey, Landscape, and Vision [1]
* On the Evaluation of Large Language Models in Unit Test Generation [2]
* Software Testing with Large Language Models: An Interview Study with Practitioners [3]
* Using Large Language Models to Generate JUnit Tests: An Empirical Study [4]
* Evaluating and Improving ChatGPT for Unit Test Generation [5]
* Large Language Models for Software Testing: A Research Roadmap [6]

## 1. Guidelines

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

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
“Generate pytest unit tests for parse_invoice(json_str) only. Cover valid input, missing required fields, malformed JSON, and currency normalization. Do not test database calls or network retries. Use parameterized tests and clear assertion messages.”

**Bad Example:**  
“Write tests for this.”

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
Generate JUnit 5 tests for the calculateDiscount(Customer c, Order o) method.
Use only the provided method and class interfaces.
Return compilable tests with meaningful assertions for normal cases, edge cases, and invalid inputs.
If assumptions are needed, state them explicitly in comments.
```

After compile errors:
```
Here are the compiler errors from your previous tests:

CustomerType enum not found

wrong method signature for getTotal()
Please fix the tests using these exact errors and regenerate only the failing test methods.
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
---

### Guideline x: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).


### Guideline 2: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---


## 2. References

[1] Wang, J., et al. "Software Testing with Large Language Models: Survey, Landscape, and Vision" IEEE Transactions on Software Engineering (2024). DOI: 10.1109/TSE.2024.3368208.

[2] Yang, L., et al. "On the Evaluation of Large Language Models in Unit Test Generation" Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE) (2024). DOI: 10.1145/3691620.3695529.

[3] Santana, M. D., Magalhaes, C., and de Souza Santos, R. "Software Testing with Large Language Models: An Interview Study with Practitioners" AIware 2025 (2025).

[4] Siddiq, M. L., et al. "Using Large Language Models to Generate JUnit Tests: An Empirical Study" (2024). DOI: 10.1145/3661167.3661216.

[5] Yuan, Z., et al. "Evaluating and Improving ChatGPT for Unit Test Generation" Proceedings of the ACM on Software Engineering 1(FSE), 1703–1726 (2024). DOI: 10.1145/3660783.

[6] Augusto, C., Bertolino, A., De Angelis, G., Lonetti, F., and Morán, J. "Large Language Models for Software Testing: A Research Roadmap" arXiv preprint (2025).

---


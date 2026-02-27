# Week 9 Example Problems: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

## 1. Example Problems

> All tasks should be completed in Python using pytest. Use the GPT-4.1 model. For testing, use the `@pytest.mark.parametrize` decorator to efficiently check multiple input cases and uncover bugs in the functions.

### Problem A: Checkout Service Testing

**Task Description:**
You have a checkout service module for an online store. This service handles item-level discounts (flash sales, bundle deals), three distinct coupon types (`SAVE10`, `SUMMER20`, `FLASH5`), a loyalty-points redemption system, shipping cost rules, tax calculation, and payment processing. You need to create unit tests that uncover if the implementation has any bugs.

**Starter Code:**
See `checkout_service.py` in the `problem_A` folder.
---

### Problem B_1: User Validation Testing

**Task Description:**  
You are given a user validation module with functions that validate email addresses, ages, usernames and passwords. Your task is to write comprehensive unit tests using pytest that will reveal bugs in the validation logic.

**Starter Code:**  
See `user_validator.py` in the Problem_B_1 folder.
---

### Problem B_2: Order Processing Decomposition (Guideline 4 Focus)

**Task Description:**  
You are given a complex `process_order()` method that handles validation, calculations, discounts, taxes, payment processing, and confirmation generation all in one function. Your task is to write comprehensive tests that expose the hidden bugs in this complex method.

**Starter Code:**  
See `order_processor.py` in the Problem_B_2 folder.
---

### Problem B_3: Data Parser Edge Cases (Combined Guidelines 3 & 4)

**Task Description:**  
You are given a data parsing module with functions for CSV parsing, JSON configuration validation, number extraction, and data type validation. Each function has multiple edge cases that need thorough testing.

**Starter Code:**  
See `data_parser.py` in the Problem_B_3 folder.

**Expected Discovery:** The combination of both guidelines will reveal numerous edge case bugs and parsing failures that simple testing approaches miss.

---

### Problem C: Reach target test coverage

Generate tests for FLASK `app.py` file and 
use `eval_test_coverage.py` to measure how well LLM-generated tests cover the functionality in it. 

**Target source file:** `flask/src/flask/app.py` (435 executable lines)
**Coverage goal:** ≥ 60%

Additional details in `week9-presentation/problems/problem_C/README.md`


## Problem D: 

### 1. Example Problems

**Setup (pytest):** Before starting, install `pytest` with `python3 -m pip install -r ProblemD/requirements.txt` (or `python3 -m pip install pytest`).

#### Problem D_1: Understand the Mini Autograd API and Generate Baseline Tests

**Task Description:**  
This problem uses a **pure-Python mini autograd engine** (`ProblemD/student/src/mini_autograd.py`) that is inspired by PyTorch autograd, but does not require installing PyTorch.  
In this context, an **autograd function** means a custom operation with an explicit forward computation and backward (gradient) rule. In `ProblemD`, custom operations are implemented using a `Function.apply(...)` API similar to `torch.autograd.Function`.

Use an LLM to generate a first pytest test file that checks baseline behavior for the mini engine:
- forward correctness for simple scalar expressions,
- backward correctness for basic operations (`+`, `*`),
- at least one custom function forward/backward case.

Review and refine the generated tests so they are clean and runnable. Do not change the implementation code yet.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`  
`ProblemD/student/tests/test_examples_smoke.py` (style example only)

---

#### Problem D_2: Design Edge-Case Tests for Autograd Graph Semantics

**Task Description:**  
Use your LLM workflow (prompt + critique + revision) to extend the pytest suite and test **graph semantics**, not just arithmetic outputs. Add tests for behavior such as:
- gradient accumulation through shared subgraphs,
- `requires_grad` propagation,
- `detach()` behavior,
- `zero_grad()` behavior,
- boundary cases for custom operations (for example, a clamp-like function).

Your tests should be small and deterministic. Avoid hidden dependencies and avoid rewriting the starter code in the test file.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`

---

#### Problem D_3: Use an LLM to Generate Tests for the Standardized `axpy` Function

**Task Description:**  
All students will use an LLM to generate pytest tests for the same function: `axpy(a, x, y)` in `ProblemD/student/src/demo_custom_functions.py`.  
Your goal is to produce a clean, runnable test file for `axpy` and improve it through prompt refinement.

Use an LLM to generate tests, run them, and refine your prompts at least once. Your final test file must include checks for:
- forward correctness for `axpy(a, x, y) = a * x + y`,
- backward gradients for all three inputs (`a`, `x`, `y`),
- gradient order correctness (the returned gradients must match the input order),
- at least one edge case (for example: zero values, negative values, or reused values).

You must document and submit:
1. the model used,  
2. the prompt(s) used,  
3. the final generated/refined test code, and  
4. a short note describing what your first generated tests missed and what changed after prompt refinement.

**Starter Code:**  
`ProblemD/student/src/demo_custom_functions.py`  
`ProblemD/student/src/mini_autograd.py`

---

#### Problem D_4: Bug-Fix Challenge Using Your Generated Tests

**Task Description:**  
Use the tests you generated/refined in Problems D_1–D_3 to identify and fix bugs in the starter implementation (you may use an LLM to propose patches, but you must verify them with tests):
- `ProblemD/student/src/mini_autograd.py`
- `ProblemD/student/src/demo_custom_functions.py`

Requirements:
1. Run your own tests first and use failures to guide debugging.
2. Fix implementation bugs without deleting features.
3. Keep your tests (and any LLM-generated tests) as evidence of how you found the bugs.
4. After the official `ProblemD` tests are provided/run, write a short comparison between your test suite and the official tests:
   - identify at least 3 bug patterns or behaviors the official tests caught that your tests missed (if any),
   - explain what your tests caught early,
   - explain where LLM-generated tests missed coverage and how you would improve the prompts.

**Important:** After you finish `ProblemD`, we will provide/run **official tests** to verify whether your tests were strong enough to expose the bugs and whether your fixes resolve all intended defects.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`  
Run helper scripts (if `pytest` is installed):  
`ProblemD/scripts/run_student_tests.sh`  
`ProblemD/scripts/run_official_tests_student.sh`

---


## 2. References

[1] `submits/example_formats.md` (format reference)  
[2] `ProblemD/README.md` (exercise packaging and run instructions)  
[3] `ProblemD/instructor/tests/test_official_autograd_contract.py` (official test suite used after submission)

---

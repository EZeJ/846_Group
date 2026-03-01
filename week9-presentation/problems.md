# Week 9 Example Problems: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

## Instructions
**GitHub Repository:** https://github.com/sonyaaat/CS846-Week9-Testing

## 1. Example Problems

### Problem A: Checkout Service Testing

Use the GPT-4 model as the preferred option.

**Task Description:**
You have a checkout service module for an online store. This service handles item-level discounts (flash sales, bundle deals), three distinct coupon types (`SAVE10`, `SUMMER20`, `FLASH5`), a loyalty-points redemption system, shipping cost rules, tax calculation, and payment processing. You need to create unit tests that uncover if the implementation has any bugs.

**Starter Code:**
See `checkout_service.py` in the `problem_A` folder.
---

## Problem B 

> All tasks should be completed in Python using pytest. Use the GPT-4 model as the preferred option. For testing, use the `@pytest.mark.parametrize` decorator to efficiently check multiple input cases and uncover bugs in the functions.

### Problem B_1: User Validation Testing

**Task Description:**  
You are given a user validation module with functions that validate email addresses, ages, usernames and passwords. Your task is to write comprehensive unit tests using pytest that will reveal bugs in the validation logic.

**Starter Code:**  
See `user_validator.py` in the ProblemB/Problem_B_1 folder.
---

### Problem B_2: Order Processing Decomposition (Guideline 4 Focus)

**Task Description:**  
You are given a complex `process_order()` method that handles validation, calculations, discounts, taxes, payment processing, and confirmation generation all in one function. Your task is to write comprehensive tests that expose the hidden bugs in this complex method.

**Starter Code:**  
See `order_processor.py` in the ProblemB/Problem_B_2 folder.
---

### Problem B_3: Data Parser Edge Cases (Combined Guidelines 3 & 4)

**Task Description:**  
You are given a data parsing module with functions for CSV parsing, JSON configuration validation, number extraction, and data type validation. Each function has multiple edge cases that need thorough testing.

**Starter Code:**  
See `data_parser.py` in the ProblemB/Problem_B_3 folder.

**Expected Discovery:** The combination of both guidelines will reveal numerous edge case bugs and parsing failures that simple testing approaches miss.

---

### Problem C: Reach target test coverage

Use the GPT-5-mini model as the preferred option.

Generate tests for FLASK `app.py` file and 
use `eval_test_coverage.py` to measure how well LLM-generated tests cover the functionality in it. 

**Target source file:** `ProblemC/flask/src/flask/app.py` (435 executable lines)
**Coverage goal:** ≥ 60%

Additional details in `problem_C/README.md`

### Problem D

**Setup (pytest):** Before starting, install `pytest` with `python3 -m pip install -r ProblemD/requirements.txt` (or `python3 -m pip install pytest`).

#### Problem D_1: Understand the Mini Autograd API and Generate Baseline Tests

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

#### Problem D_2: Design Edge-Case Tests for Autograd Graph Semantics

**Task Description:**  
Use your LLM to extend the pytest suite and test **graph semantics**, not just arithmetic outputs. Add tests for behavior such as: gradient accumulation through shared subgraphs, etc.


Your tests should be small and deterministic. Avoid hidden dependencies and avoid rewriting the starter code in the test file.

**Starter Code:**  
`ProblemD/student/src/mini_autograd.py`  
`ProblemD/student/src/demo_custom_functions.py`

---

#### Problem D_3: Use an LLM to Generate Tests for the Standardized `axpy` Function

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

#### Problem D_4: Bug-Fix Challenge Using Your Generated Tests

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





---

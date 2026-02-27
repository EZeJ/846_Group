# Problem C: Test Coverage Evaluator

## Overview


Generate tests for FLASK `app.py` file and 
use `test_coverage.py` to measure how well LLM-generated tests cover the functionality in it. 

**Target source file:** `flask/src/flask/app.py` (435 executable lines)
**Coverage goal:** ≥ 60%

---

## Setup

```bash
pip3 install pytest pytest-cov
cd week9-presentation/problems/problem_C
```
---

## STEP 1: Write the prompt and generate the tests

## STEP 2: Evaluate a test file

```bash
python3 eval_test_coverage.py \
  --source-file flask/src/flask/app.py \
  --test-file "your test file" \
  --work-dir flask
```


## STEP 3: Review the Guideline

## STEP 4: Rewrite the prompt and generate the tests

## STEP 5: Compare 2 test files and their test coverage

```bash
python3 compare_coverage.py --src flask/src/flask/app.py \
  --unguided "your test file created with unguided prompt" \
  --guided "your test file created with guided prompt" \
  --work-dir flask
```

### Helpers:

**See failing tests**:

Run from inside the `flask/` directory:
```bash
cd flask
python3 -m pytest your_test_file.py --tb=short -q
```
---
# Problem C: Test Coverage Evaluator

## Overview

Generate tests for FLASK `app.py` file and 
use `test_coverage.py` to measure how well LLM-generated tests cover the functionality in it. 

**Target source file:** `flask/src/flask/app.py` (435 executable lines)
**Coverage goal:** ≥ 60%

---

## Setup

```bash
pip3 install pytest pytest-cov flask
cd problem_C
git clone https://github.com/pallets/flask.git
```
---

## STEP 1: Write the prompt and generate the tests

Place the test file into the problem_C folder root and name it "test_flask1.py".

## STEP 2: Evaluate a test file

```bash
python3 eval_test_coverage.py \
  --source-file flask/src/flask/app.py \
  --test-file "test_flask1.py" \
  --work-dir flask
```


## STEP 3: Review the Guideline

## STEP 4: Rewrite the prompt and generate the tests

Place the test file into the problem_C folder root and name it "test_flask2.py".

## STEP 5: Compare 2 test files and their test coverage

```bash
python3 compare_coverage.py --src flask/src/flask/app.py \
  --unguided "test_flask1.py" \
  --guided "test_flask2.py" \
  --work-dir flask
```


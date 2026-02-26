# Problem C: Test Coverage Evaluator

## Overview

This problem uses `test_coverage.py` to measure how well LLM-generated test suites cover Flask's `app.py`. You will generate test files using different prompting strategies, evaluate their coverage, and compare the results.

**Target source file:** `flask/src/flask/app.py` (435 executable lines)
**Coverage goal:** ≥ 60%

---

## Setup

```bash
pip3 install pytest pytest-cov
```
All commands below assume you are running from the `problem_C/` directory:
```bash
cd week9-presentation/problems/problem_C
```

---

## Evaluate a test file

```bash
python3 eval_test_coverage.py
```

---

## See failing tests

Run from inside the `flask/` directory:
```bash
cd flask
python3 -m pytest ../your_test_file.py --tb=short -q
```

---

## Compare two runs

```bash
python3 compare_coverage.py
```

---
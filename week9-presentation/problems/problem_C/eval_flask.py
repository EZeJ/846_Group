"""
Evaluates test coverage for several Flask source modules using test_coverage.py.
Run from problem_C/:  python eval_flask.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from test_coverage import evaluate_test_coverage, generate_coverage_report, compare_coverage

FLASK_ROOT = os.path.join(os.path.dirname(__file__), "flask")
FLASK_SRC  = os.path.join(FLASK_ROOT, "src", "flask")
FLASK_TESTS = os.path.join(FLASK_ROOT, "tests")

# (source module, test file) pairs to evaluate
PAIRS = [
    ("helpers.py",   "test_helpers.py"),
    ("config.py",    "test_config.py"),
    ("sessions.py",  "test_session_interface.py"),
    ("views.py",     "test_views.py"),
    ("templating.py","test_templating.py"),
]

results = {}

for src_name, tst_name in PAIRS:
    src  = os.path.join(FLASK_SRC,   src_name)
    tst  = os.path.join(FLASK_TESTS, tst_name)
    label = src_name.replace(".py", "")

    print(f"\nEvaluating: {src_name} <-> {tst_name} ...")
    result = evaluate_test_coverage(src, tst, min_coverage=80.0, work_dir=FLASK_ROOT)
    results[label] = result
    print(generate_coverage_report(result))

# Summary table
print("\n" + "=" * 60)
print(f"  {'Module':<20} {'Coverage':>10}  {'Pass/Fail':>12}  {'Threshold':>10}")
print("  " + "-" * 56)
for label, r in results.items():
    tr = r["test_results"]
    pf = f"{tr['passed']}P / {tr['failed']}F"
    ok = "PASS" if r["passes_threshold"] else "FAIL"
    print(f"  {label:<20} {r['coverage_percent']:>9.1f}%  {pf:>12}  {ok:>10}")
print("=" * 60)

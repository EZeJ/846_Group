import sys, os
sys.path.insert(0, ".")
from test_coverage import evaluate_test_coverage, compare_coverage

src      = "flask/src/flask/app.py"
unguided = evaluate_test_coverage(src, os.path.abspath("test_worse.py"), work_dir="flask") # <- change this
guided   = evaluate_test_coverage(src, os.path.abspath("test_after_5_2_guidelines/test_app_py.py"), work_dir="flask") # <- change this

print(compare_coverage(guided=guided, unguided=unguided))
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from test_coverage import evaluate_test_coverage, generate_coverage_report

result = evaluate_test_coverage(
    source_file=os.path.join(HERE, "flask", "src", "flask", "app.py"),
    test_file=os.path.join(HERE, "test_before_guidelines", "test_app_llm.py"),  # <- change this
    min_coverage=60.0,
    work_dir=os.path.join(HERE, "flask"),
)
print(generate_coverage_report(result))
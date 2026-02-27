import sys, os
import argparse
sys.path.insert(0, ".")
from test_coverage import evaluate_test_coverage, compare_coverage

def main():
	parser = argparse.ArgumentParser(description="Compare test coverage for guided vs unguided tests")
	parser.add_argument("--src", default="flask/src/flask/app.py",
						help="source file to measure coverage for (default: flask/src/flask/app.py)")
	parser.add_argument("--unguided", default="test_worse.py",
						help="path to the unguided test file (default: test_worse.py)")
	parser.add_argument("--guided", default="test_after_5_2_guidelines/test_app_py.py",
						help="path to the guided test file (default: test_after_5_2_guidelines/test_app_py.py)")
	parser.add_argument("--work-dir", default="flask",
						help="working directory to run coverage in (default: flask)")

	args = parser.parse_args()

	src = args.src
	unguided = evaluate_test_coverage(src, os.path.abspath(args.unguided), work_dir=args.work_dir)
	guided = evaluate_test_coverage(src, os.path.abspath(args.guided), work_dir=args.work_dir)

	print(compare_coverage(guided=guided, unguided=unguided))

if __name__ == "__main__":
	main()
import os
import argparse

from test_coverage import evaluate_test_coverage, generate_coverage_report


def main():
    parser = argparse.ArgumentParser(description="Evaluate test coverage for a source file")
    parser.add_argument(
        "--source-file",
        default=os.path.join("flask", "src", "flask", "app.py"),
        help="source file to measure coverage for (relative to current working directory)",
    )
    parser.add_argument(
        "--test-file",
        default=os.path.join("test_before_guidelines", "test_app_llm.py"),
        help="path to the test file (relative to current working directory)",
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=60.0,
        help="minimum coverage threshold (float)",
    )
    parser.add_argument(
        "--work-dir",
        default="flask",
        help="working directory to run coverage in (relative to current working directory)",
    )

    args = parser.parse_args()

    result = evaluate_test_coverage(
        source_file=args.source_file,
        test_file=args.test_file,
        min_coverage=args.min_coverage,
        work_dir=args.work_dir,
    )

    print(generate_coverage_report(result))


if __name__ == "__main__":
    main()
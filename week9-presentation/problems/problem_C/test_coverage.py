"""
Test Coverage Evaluator - Problem C
Week 9: Testing / QA with LLMs

This module provides utilities for evaluating the coverage quality of
LLM-generated test suites. Students use this to compare results from
guided vs. unguided prompting approaches.
"""

import subprocess
import sys
import os
import json
import re
from typing import Dict


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def evaluate_test_coverage(
    source_file: str,
    test_file: str,
    min_coverage: float = 60.0,
    work_dir: str = None,
) -> Dict:
    """
    Runs pytest with coverage on `test_file` and measures how well it covers
    `source_file`.

    Args:
        source_file (str): Absolute or relative path to the module under test.
        test_file   (str): Absolute or relative path to the pytest test file.
        min_coverage (float): Minimum acceptable line-coverage percentage
                              (default 80.0).
        work_dir (str): Directory to run pytest from. Defaults to the directory
                        containing source_file. Override when tests and source
                        live in different subdirectories (e.g. src/ layout).

    Returns:
        Dict with keys:
            coverage_percent  (float)      – line coverage as a percentage
            covered_lines     (List[int])  – line numbers that were executed
            uncovered_lines   (List[int])  – line numbers that were NOT executed
            total_lines       (int)        – total number of executable lines
            passes_threshold  (bool)       – True if coverage_percent >= min_coverage
            min_coverage      (float)      – the threshold that was applied
            test_results      (Dict)       – pytest pass / fail / error counts
            raw_output        (str)        – combined stdout + stderr from pytest
    """
    source_file = os.path.abspath(source_file)
    test_file = os.path.abspath(test_file)
    work_dir = os.path.abspath(work_dir) if work_dir else os.path.dirname(source_file)
    module_name = _module_name(source_file)
    # Derive the importable dotted name (e.g. flask.helpers) so that
    # pytest-cov can locate the module whether it lives in a src/ layout
    # or is a top-level file.
    cov_target = _dotted_module_name(source_file)

    coverage_json = os.path.join(work_dir, "coverage.json")

    cmd = [
        sys.executable, "-m", "pytest",
        test_file,
        "--tb=short", "-q",
        f"--cov={cov_target}",
        "--cov-report=json",
        "--cov-report=term-missing",
    ]

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=work_dir,
    )
    raw_output = proc.stdout + proc.stderr

    coverage_data = _parse_coverage_json(coverage_json, module_name)
    test_results = _parse_test_results(raw_output)

    # Clean up temporary coverage artefacts
    _cleanup(work_dir, coverage_json)

    pct = coverage_data.get("percent_covered", 0.0)

    return {
        "coverage_percent": pct,
        "covered_lines": coverage_data.get("covered_lines", []),
        "uncovered_lines": coverage_data.get("uncovered_lines", []),
        "total_lines": coverage_data.get("total_lines", 0),
        "passes_threshold": pct >= min_coverage,
        "min_coverage": min_coverage,
        "test_results": test_results,
        "raw_output": raw_output,
    }


def generate_coverage_report(coverage_result: Dict) -> str:
    """
    Formats the dict returned by `evaluate_test_coverage` into a
    human-readable report.

    Args:
        coverage_result (Dict): Return value of evaluate_test_coverage().

    Returns:
        str: A formatted multi-line report string.
    """
    sep = "=" * 52
    lines = [
        sep,
        "  TEST COVERAGE REPORT",
        sep,
        f"  Coverage       : {coverage_result.get('coverage_percent', 0.0):.1f}%",
        f"  Total lines    : {coverage_result.get('total_lines', 0)}",
        f"  Covered        : {len(coverage_result.get('covered_lines', []))}",
        f"  Not covered    : {len(coverage_result.get('uncovered_lines', []))}",
        "",
    ]

    uncovered = coverage_result.get("uncovered_lines", [])
    if uncovered:
        lines.append(f"  Uncovered lines: {uncovered}")
    else:
        lines.append("  All executable lines are covered.")

    lines.append("")

    tr = coverage_result.get("test_results", {})
    lines += [
        "  TEST RESULTS",
        "  " + "-" * 30,
        f"  Passed  : {tr.get('passed', 0)}",
        f"  Failed  : {tr.get('failed', 0)}",
        f"  Errors  : {tr.get('errors', 0)}",
        f"  Total   : {tr.get('total', 0)}",
        "",
    ]

    threshold = coverage_result.get("min_coverage", 80.0)
    status = "PASS" if coverage_result.get("passes_threshold", False) else "FAIL"
    lines.append(f"  Threshold ({threshold}%) : {status}")
    lines.append(sep)

    return "\n".join(lines)


def compare_coverage(guided: Dict, unguided: Dict) -> str:
    """
    Compares coverage results from a guided prompt run and an unguided run.

    Useful for demonstrating the impact of applying the week's guidelines.

    Args:
        guided   (Dict): evaluate_test_coverage() result with guidelines applied.
        unguided (Dict): evaluate_test_coverage() result without guidelines.

    Returns:
        str: Side-by-side comparison report.
    """
    sep = "=" * 52
    lines = [
        sep,
        "  GUIDED vs. UNGUIDED COVERAGE COMPARISON",
        sep,
        f"  {'Metric':<25} {'Unguided':>10} {'Guided':>10}",
        "  " + "-" * 48,
        f"  {'Coverage %':<25} {unguided.get('coverage_percent', 0.0):>9.1f}%"
        f" {guided.get('coverage_percent', 0.0):>9.1f}%",
        f"  {'Covered lines':<25} {len(unguided.get('covered_lines', [])):>10}"
        f" {len(guided.get('covered_lines', [])):>10}",
        f"  {'Uncovered lines':<25} {len(unguided.get('uncovered_lines', [])):>10}"
        f" {len(guided.get('uncovered_lines', [])):>10}",
        f"  {'Tests passed':<25} {unguided.get('test_results', {}).get('passed', 0):>10}"
        f" {guided.get('test_results', {}).get('passed', 0):>10}",
        f"  {'Tests failed':<25} {unguided.get('test_results', {}).get('failed', 0):>10}"
        f" {guided.get('test_results', {}).get('failed', 0):>10}",
        f"  {'Passes threshold':<25} {str(unguided.get('passes_threshold', False)):>10}"
        f" {str(guided.get('passes_threshold', False)):>10}",
        sep,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _module_name(source_file: str) -> str:
    """Returns the bare module name (no extension) from a file path."""
    return os.path.splitext(os.path.basename(source_file))[0]


def _dotted_module_name(source_file: str) -> str:
    """
    Derives the importable dotted module name by walking up the directory
    tree while __init__.py files exist.

    Examples:
        /project/src/flask/helpers.py  ->  flask.helpers
        /project/user_validator.py     ->  user_validator
    """
    source_file = os.path.abspath(source_file)
    parts = [os.path.splitext(os.path.basename(source_file))[0]]
    d = os.path.dirname(source_file)
    while os.path.exists(os.path.join(d, "__init__.py")):
        parts.insert(0, os.path.basename(d))
        d = os.path.dirname(d)
    return ".".join(parts)


def _parse_coverage_json(json_path: str, module_name: str) -> Dict:
    """
    Reads the coverage.json file produced by pytest-cov and extracts
    line-level coverage data for the target module.

    Returns an empty dict if the file does not exist or the module is not
    found inside it.
    """
    if not os.path.exists(json_path):
        return {}

    with open(json_path, "r") as fh:
        data = json.load(fh)

    for file_path, file_data in data.get("files", {}).items():
        if module_name in os.path.basename(file_path):
            executed = sorted(file_data.get("executed_lines", []))
            missing = sorted(file_data.get("missing_lines", []))
            total = len(executed) + len(missing)
            percent = (len(executed) / total * 100) if total > 0 else 0.0
            return {
                "percent_covered": round(percent, 2),
                "covered_lines": executed,
                "uncovered_lines": missing,
                "total_lines": total,
            }

    return {}


def _parse_test_results(output: str) -> Dict:
    """
    Extracts pass / fail / error counts from pytest's terminal output.

    Handles the compact summary line that pytest prints at the end, e.g.
    '5 passed, 2 failed, 1 error in 0.42s'.
    """
    def _find(pattern: str) -> int:
        m = re.search(pattern, output)
        return int(m.group(1)) if m else 0

    passed = _find(r"(\d+) passed")
    failed = _find(r"(\d+) failed")
    errors = _find(r"(\d+) error")

    return {
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": passed + failed + errors,
    }


def _cleanup(work_dir: str, coverage_json: str) -> None:
    """Removes coverage artefacts created during the run."""
    for path in [coverage_json, os.path.join(work_dir, ".coverage")]:
        if os.path.exists(path):
            os.remove(path)


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python test_coverage.py <source_file> <test_file> [min_coverage]")
        sys.exit(1)

    src = sys.argv[1]
    tst = sys.argv[2]
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0

    result = evaluate_test_coverage(src, tst, min_coverage=threshold)
    print(generate_coverage_report(result))

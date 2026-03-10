import pytest
from analytics import compute_rate, build_summary


def test_compute_rate_normal():
    assert compute_rate([1, 2, 3], 10) == 0.3


def test_compute_rate_zero_window():
    # Currently passes because ZeroDivisionError is raised.
    # The test only asserts that *some* exception is raised on window_seconds=0.
    with pytest.raises(ZeroDivisionError):
        compute_rate([], 0)


def test_build_summary_basic():
    records = [{"tag": "error", "msg": "oops"}]
    result = build_summary(records)
    assert result["count"] == 1
    assert "error" in result["tags"]
    # NOTE: No test for repeated calls — the mutable-default bug is invisible here.

# file: tests/test_math_utils.py
from math_utils import normalize

def test_normalize_basic():
    out = normalize([1, 1, 2])
    assert out == [0.25, 0.25, 0.5]

def test_normalize_all_zeros():
    assert normalize([0, 0, 0]) == [0, 0, 0]
import pytest
from utils.text import slugify

def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"

def test_slugify_unicode():
    # unicode -> ascii normalized
    assert slugify("Café crème") == "cafe-creme"

def test_slugify_none_is_handled():
    # This is the counterexample: should not crash, but it does right now.
    # Expect a safe fallback (empty slug).
    assert slugify(None) == ""
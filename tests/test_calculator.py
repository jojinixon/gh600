import pytest

from app.calculator import add, average

def test_add():
    assert add(2, 3) == 5

def test_average():
    assert average([2, 4]) == 3

def test_average_empty_list():
    with pytest.raises(ValueError, match="at least one number"):
        average([])
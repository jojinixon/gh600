from app.calculator import add, average, divide
import pytest

def test_add():
    assert add(2, 3) == 5

def test_average():
    assert average([2, 4]) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)
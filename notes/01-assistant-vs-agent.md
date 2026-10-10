An empty list has no mathematical average, so raise a clear `ValueError` rather than returning `0`, which could be mistaken for a real result. In [app/calculator.py](app/calculator.py), check for emptiness before dividing:

```python
def average(numbers):
	if not numbers:
		raise ValueError("average() requires at least one number")
	return sum(numbers) / len(numbers)
```

Add a test in [tests/test_calculator.py](tests/test_calculator.py) to make that behavior explicit:

```python
import pytest

def test_average_empty_list():
	with pytest.raises(ValueError, match="at least one number"):
		average([])
```

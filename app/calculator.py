def add(a, b):
    return a + b

def divide(a, b):
    return a / b   # BUG: no zero-division handling

def average(numbers):
    if not numbers:
        raise ValueError("average() requires at least one number")
    return sum(numbers) / len(numbers)
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def average(numbers):
    return sum(numbers) / len(numbers)   # BUG: crashes on empty list
def add(a, b):
    return a + b

def divide(a, b):
    return a / b   # BUG: no zero-division handling

def average(numbers):
    return sum(numbers) / len(numbers)   # BUG: crashes on empty list
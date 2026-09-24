def fibonacci(number: int) -> int:
    a, b = 0, 1
    for _ in range(number):
        a, b = b, a + b
    return a


def fibonacci_list(number: int) -> list[int]:
    fib_numbers = []
    a, b = 0, 1
    for _ in range(number):
        fib_numbers.append(a)
        a, b = b, a + b
    return fib_numbers


def factorial(number: int) -> int:
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result

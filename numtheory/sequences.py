from numtheory._validation import check_int


def fibonacci(number: int) -> int:
    '''
    Возвращает число Фибоначчи с номером number.
    Нумерация с нуля: F(0) = 0, F(1) = 1, F(n) = F(n - 1) + F(n - 2), считается циклом.
    Для отрицательных номеров последовательность продолжается по тому же правилу в обратную
    сторону: F(-n) = (-1)^(n + 1) · F(n), например F(-1) = 1, F(-2) = -1. В этом случае функция
    один раз вызывает сама себя с положительным номером.
    Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number (int): номер числа в последовательности, любое целое

        Возвращаемое значение:
            fib_number (int): число Фибоначчи F(number)
    '''
    check_int(number, "number")
    if number < 0:
        fib_number = fibonacci(-number)
        return fib_number if number % 2 != 0 else -fib_number

    a, b = 0, 1
    for _ in range(number):
        a, b = b, a + b
    return a


def fibonacci_list(number: int) -> list[int]:
    '''
    Возвращает первые number чисел Фибоначчи, начиная с F(0) = 0.
    Список длины number заканчивается на F(number - 1). При number, равном 0, список пустой.
    Количество не может быть отрицательным, для отрицательного number выбрасывается ValueError,
    для нецелого аргумента TypeError.

        Параметры:
            number (int): сколько чисел вернуть, неотрицательное целое

        Возвращаемое значение:
            fib_numbers (list[int]): числа F(0), F(1), ..., F(number - 1)
    '''
    check_int(number, "number")
    if number < 0:
        raise ValueError("количество чисел не может быть отрицательным")

    fib_numbers = []
    a, b = 0, 1
    for _ in range(number):
        fib_numbers.append(a)
        a, b = b, a + b
    return fib_numbers


def factorial(number: int) -> int:
    '''
    Вычисляет факториал n! = 1 · 2 · ... · n, по определению 0! = 1.
    Факториал отрицательного числа не определён, для него выбрасывается ValueError,
    для нецелого аргумента TypeError.

        Параметры:
            number (int): неотрицательное целое число

        Возвращаемое значение:
            result (int): факториал number
    '''
    check_int(number, "number")
    if number < 0:
        raise ValueError("факториал отрицательного числа не определён")

    result = 1
    for i in range(2, number + 1):
        result *= i
    return result

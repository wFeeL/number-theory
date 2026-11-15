from numtheory._validation import ints_only
from numtheory.primes import factorize


@ints_only
def gcd(number1: int, number2: int) -> int:
    '''
    Находит наибольший общий делитель двух целых чисел алгоритмом Евклида.
    Пара (a, b) заменяется на (b, a mod b), пока b не станет нулём. Знаки аргументов не влияют
    на результат. Если один аргумент равен 0, результат равен модулю другого, gcd(0, 0) равен 0.
    Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number1 (int): первое целое число
            number2 (int): второе целое число

        Возвращаемое значение:
            divisor (int): неотрицательный наибольший общий делитель number1 и number2
    '''
    number1, number2 = abs(number1), abs(number2)
    while number2 != 0:
        number1, number2 = number2, number1 % number2
    return number1


@ints_only
def lcm(number1: int, number2: int) -> int:
    '''
    Находит наименьшее общее кратное двух целых чисел по формуле |a · b| / gcd(a, b).
    Знаки аргументов не влияют на результат. Если хотя бы один аргумент равен 0, результат равен 0.
    Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number1 (int): первое целое число
            number2 (int): второе целое число

        Возвращаемое значение:
            multiple (int): неотрицательное наименьшее общее кратное number1 и number2
    '''
    if number1 == 0 or number2 == 0:
        return 0
    return abs(number1 * number2) // gcd(number1, number2)


@ints_only
def divisors(number: int) -> list[int]:
    '''
    Возвращает все натуральные делители целого числа.
    Перебирает d до корня из числа: каждый найденный делитель d сразу даёт парный number // d.
    У отрицательного числа те же натуральные делители, что и у его модуля. У нуля делителем
    является любое число, поэтому для 0 выбрасывается ValueError, для нецелого аргумента TypeError.

        Параметры:
            number (int): целое число, не равное 0

        Возвращаемое значение:
            divisors_list (list[int]): делители по возрастанию, от 1 до модуля number
    '''
    if number == 0:
        raise ValueError("у 0 бесконечно много делителей")
    number = abs(number)

    small = []
    large = []
    d = 1

    while d * d <= number:
        if number % d == 0:
            small.append(d)
            if d != number // d:
                large.append(number // d)
        d += 1

    return small + large[::-1]


@ints_only
def is_perfect(number: int) -> bool:
    '''
    Проверяет, является ли число совершенным.
    Совершенное число равно сумме своих делителей без самого себя, например 6 = 1 + 2 + 3.
    Совершенными бывают только натуральные числа, поэтому для 0, 1 и отрицательных чисел
    ответ False. Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number (int): проверяемое целое число

        Возвращаемое значение:
            result (bool): True, если number совершенное, иначе False
    '''
    if number < 2:
        return False
    return sum(divisors(number)) - number == number


@ints_only
def euler_phi(number: int) -> int:
    '''
    Вычисляет функцию Эйлера: количество чисел от 1 до number, взаимно простых с number.
    Раскладывает число на простые множители и для каждого различного простого p умножает
    результат на (1 - 1 / p), то есть заменяет его на result // p * (p - 1). Для единицы
    ответ равен 1: число 1 взаимно просто с самим собой. Функция определена только для
    натуральных чисел, поэтому для 0 и отрицательных чисел выбрасывается ValueError,
    для нецелого аргумента TypeError.

        Параметры:
            number (int): натуральное число

        Возвращаемое значение:
            result (int): количество чисел от 1 до number, взаимно простых с number
    '''
    if number < 1:
        raise ValueError("функция Эйлера определена только для натуральных чисел")

    result = number
    previous = 0
    for p in factorize(number):
        if p != previous:
            result = result // p * (p - 1)
            previous = p
    return result

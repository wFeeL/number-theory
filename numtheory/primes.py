from numtheory._validation import ints_only


@ints_only
def is_prime(number: int) -> bool:
    '''
    Проверяет, является ли число простым.
    Перебирает делители от 2, пока квадрат делителя не превысит число. Простыми считаются
    только натуральные числа больше 1, поэтому для 0, 1 и отрицательных чисел ответ False.
    Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number (int): проверяемое целое число

        Возвращаемое значение:
            result (bool): True, если number простое, иначе False
    '''
    if number < 2:
        return False
    d = 2
    while number % d != 0 and d * d <= number:
        d += 1
    return d * d > number


@ints_only
def primes_up_to(number: int) -> list[int]:
    '''
    Возвращает все простые числа от 2 до number включительно.
    Демонстрационная медленная версия для проверки теста производительности: каждое число k
    проверяется по определению, у простого числа ровно два делителя. Делители считаются
    перебором d от 1 до корня из k (пары d и k // d) без досрочного выхода, поэтому время
    растет примерно как number в степени 1.5. Если number меньше 2, простых в диапазоне нет
    и список пустой. Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            number (int): верхняя граница поиска, включительно

        Возвращаемое значение:
            prime_numbers (list[int]): простые числа по возрастанию
    '''
    if number < 2:
        return []

    prime_numbers = []
    for k in range(2, number + 1):
        divisors_count = 0
        d = 1
        while d * d <= k:
            if k % d == 0:
                divisors_count += 1
                if d != k // d:
                    divisors_count += 1
            d += 1

        if divisors_count == 2:
            prime_numbers.append(k)

    return prime_numbers

    # Прежняя реализация (решето Эратосфена): вычеркивает кратные каждого найденного простого,
    # начиная с его квадрата.
    #
    # if number < 2:
    #     return []
    #
    # is_prime = [True] * (number + 1)
    # d = 2
    # while d * d <= number:
    #     if is_prime[d]:
    #         for i in range(d * d, number + 1, d):
    #             is_prime[i] = False
    #
    #     d += 1
    #
    # prime_numbers = []
    # for i in range(2, number + 1):
    #     if is_prime[i]:
    #         prime_numbers.append(i)
    #
    # return prime_numbers


@ints_only
def factorize(number: int) -> list[int]:
    '''
    Раскладывает целое число на простые множители.
    Делит число на наименьший делитель, пока это возможно, затем берёт следующий. У отрицательного
    числа первым множителем идёт -1, у единицы множителей нет. Ноль разложить нельзя, для него
    выбрасывается ValueError, для нецелого аргумента TypeError.

        Параметры:
            number (int): раскладываемое целое число, не равное 0

        Возвращаемое значение:
            factors (list[int]): простые множители по возрастанию с повторениями, их произведение равно number
    '''
    if number == 0:
        raise ValueError("0 нельзя разложить на простые множители")

    factors = []
    if number < 0:
        factors.append(-1)
        number = -number

    d = 2
    while d * d <= number:
        if number % d == 0:
            factors.append(d)
            number //= d
        else:
            d += 1

    if number > 1:
        factors.append(number)
    return factors

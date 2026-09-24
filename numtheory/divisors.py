def gcd(number1: int, number2: int) -> int:
    number1, number2 = abs(number1), abs(number2)
    while number2 != 0:
        number1, number2 = number2, number1 % number2
    return number1


def lcm(number1: int, number2: int) -> int:
    if number1 == 0 or number2 == 0:
        return 0
    return abs(number1 * number2) // gcd(number1, number2)


def divisors(number: int) -> list[int]:
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


def is_perfect(number: int) -> bool:
    if number < 2:
        return False
    return sum(divisors(number)) - number == number

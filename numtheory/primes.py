def is_prime(number: int) -> bool:
    if number < 2:
        return False
    d = 2
    while number % d != 0 and d * d <= number:
        d += 1
    return d * d > number


def primes_up_to(number: int) -> list[int]:
    is_prime = [True] * (number + 1)
    d = 2
    while d * d <= number:
        if is_prime[d]:
            for i in range(d * d, number + 1, d):
                is_prime[i] = False
                
        d += 1

    prime_numbers = []
    for i in range(2, number + 1):
        if is_prime[i]:
            prime_numbers.append(i)

    return prime_numbers


def factorize(number: int) -> list[int]:
    factors = []
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

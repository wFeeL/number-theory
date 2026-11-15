import re
import time
import unittest

from numtheory.primes import is_prime, primes_up_to, factorize

NOT_INTEGERS = (2.5, "7", None)
BOOLEANS = (True, False)

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 97, 7919)
LARGE_PRIMES = (10**9 + 7, 998244353, 2**31 - 1, 10**12 + 39)

TIME_LIMIT_SECONDS = 3.0


def brute_force_is_prime(n):
    return n >= 2 and all(n % d != 0 for d in range(2, n))


class IsPrimeTestCase(unittest.TestCase):
    def test_small_primes(self):
        '''TC-PRI-01. is_prime: малые простые числа'''
        for number in SMALL_PRIMES + (17, 19, 23, 29, 31, 37, 41, 43, 47):
            with self.subTest(number=number):
                result = is_prime(number)
                self.assertIsInstance(result, bool)
                self.assertIs(result, True)

    def test_composites(self):
        '''TC-PRI-02. is_prime: составные числа дают False'''
        for number in (4, 6, 8, 9, 10, 15, 21, 25, 27, 33, 49, 91, 100, 121, 1000, 7917):
            with self.subTest(number=number):
                result = is_prime(number)
                self.assertIsInstance(result, bool)
                self.assertIs(result, False)

    def test_zero_one_and_negative_are_not_prime(self):
        '''TC-PRI-03. is_prime: 0, 1 и отрицательные дают False'''
        for number in (0, 1, -1, -2, -3, -7, -97, -(10**9 + 7)):
            with self.subTest(number=number):
                self.assertIs(is_prime(number), False)

    def test_boundaries_two_three_four(self):
        '''TC-PRI-04. is_prime: границы 1, 2, 3, 4'''
        self.assertIs(is_prime(1), False)
        self.assertIs(is_prime(2), True)
        self.assertIs(is_prime(3), True)
        self.assertIs(is_prime(4), False)

    def test_squares_and_products_of_primes(self):
        '''TC-PRI-05. is_prime: квадраты и произведения простых'''
        cases = [4, 9, 25, 49, 121, 169, 7919**2, 15, 35, 77, 10007 * 10009, 999979 * 999983]
        for number in cases:
            with self.subTest(number=number):
                self.assertIs(is_prime(number), False)

    def test_pseudoprimes_are_composite(self):
        '''TC-PRI-06. is_prime: числа Кармайкла и 2047 составные'''
        for number in (561, 1105, 1729, 2465, 2047, 3277):
            with self.subTest(number=number):
                self.assertIs(is_prime(number), False)

    def test_large_numbers(self):
        '''TC-PRI-07. is_prime: большие простые и составные'''
        for number in LARGE_PRIMES:
            with self.subTest(prime=number):
                self.assertIs(is_prime(number), True)
        for number in (10**12, 10**12 + 1, 2**40, (10**6 + 3) ** 2, (10**9 + 7) * 3):
            with self.subTest(composite=number):
                self.assertIs(is_prime(number), False)

    def test_matches_brute_force_oracle(self):
        '''TC-PRI-08. is_prime: оракул перебором для n от -20 до 600'''
        for n in range(-20, 601):
            with self.subTest(n=n):
                self.assertEqual(is_prime(n), brute_force_is_prime(n))

    def test_count_of_primes_below_thousand(self):
        '''TC-PRI-09. is_prime: ровно 168 простых до 1000'''
        found = [n for n in range(-5, 1001) if is_prime(n)]
        self.assertEqual(len(found), 168)
        self.assertEqual(found[:5], [2, 3, 5, 7, 11])
        self.assertEqual(found[-1], 997)

    def test_type_error(self):
        '''TC-PRI-10. is_prime: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    is_prime(bad)

    def test_type_error_bool(self):
        '''TC-PRI-11. is_prime: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    is_prime(flag)

    def test_performance_large_prime(self):
        '''TC-PRI-12. is_prime: простое 10**12 + 39 быстрее 3 с'''
        started = time.perf_counter()
        result = is_prime(10**12 + 39)
        elapsed = time.perf_counter() - started
        self.assertIs(result, True)
        self.assertLess(elapsed, TIME_LIMIT_SECONDS)


class PrimesUpToTestCase(unittest.TestCase):
    def test_known_lists(self):
        '''TC-PRI-13. primes_up_to: известные списки'''
        cases = [
            (20, [2, 3, 5, 7, 11, 13, 17, 19]),
            (10, [2, 3, 5, 7]),
            (30, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
            (50, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(primes_up_to(number), expected)

    def test_upper_bound_is_inclusive(self):
        '''TC-PRI-14. primes_up_to: граница number включена'''
        cases = [(13, 13), (14, 13), (12, 11), (97, 97), (96, 89), (7919, 7919)]
        for number, last in cases:
            with self.subTest(number=number):
                self.assertEqual(primes_up_to(number)[-1], last)

    def test_below_two_gives_empty_list(self):
        '''TC-PRI-15. primes_up_to: number меньше 2 дает пустой список'''
        for number in (1, 0, -1, -2, -100, -(10**12)):
            with self.subTest(number=number):
                result = primes_up_to(number)
                self.assertIsInstance(result, list)
                self.assertEqual(result, [])

    def test_boundaries_two_three_four(self):
        '''TC-PRI-16. primes_up_to: границы 2, 3, 4'''
        self.assertEqual(primes_up_to(2), [2])
        self.assertEqual(primes_up_to(3), [2, 3])
        self.assertEqual(primes_up_to(4), [2, 3])

    def test_prime_counting_values(self):
        '''TC-PRI-17. primes_up_to: количество простых до 10**k'''
        cases = [(10, 4), (100, 25), (1000, 168), (10**4, 1229), (10**5, 9592)]
        for number, count in cases:
            with self.subTest(number=number):
                self.assertEqual(len(primes_up_to(number)), count)

    def test_result_is_sorted_list_of_ints(self):
        '''TC-PRI-18. primes_up_to: список int по возрастанию без повторов'''
        result = primes_up_to(500)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIs(type(item), int)
        self.assertEqual(result, sorted(set(result)))
        self.assertEqual(result[0], 2)

    def test_matches_is_prime_oracle(self):
        '''TC-PRI-19. primes_up_to: сверка с is_prime для n до 1000'''
        for limit in (2, 3, 10, 99, 100, 101, 500, 1000):
            with self.subTest(limit=limit):
                expected = [n for n in range(-5, limit + 1) if is_prime(n)]
                self.assertEqual(primes_up_to(limit), expected)

    def test_matches_brute_force_oracle(self):
        '''TC-PRI-20. primes_up_to: оракул перебором для границ до 120'''
        for limit in range(-3, 121):
            with self.subTest(limit=limit):
                expected = [n for n in range(2, limit + 1) if brute_force_is_prime(n)]
                self.assertEqual(primes_up_to(limit), expected)

    def test_type_error(self):
        '''TC-PRI-21. primes_up_to: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    primes_up_to(bad)

    def test_type_error_bool(self):
        '''TC-PRI-22. primes_up_to: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    primes_up_to(flag)

    def test_performance_one_million(self):
        '''TC-PRI-23. primes_up_to: решето до 10**6 быстрее 3 с'''
        started = time.perf_counter()
        result = primes_up_to(10**6)
        elapsed = time.perf_counter() - started
        self.assertEqual(len(result), 78498)
        self.assertEqual(result[-1], 999983)
        self.assertLess(elapsed, TIME_LIMIT_SECONDS)


class FactorizeTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-PRI-24. factorize: известные разложения'''
        cases = [
            (60, [2, 2, 3, 5]),
            (12, [2, 2, 3]),
            (100, [2, 2, 5, 5]),
            (360, [2, 2, 2, 3, 3, 5]),
            (91, [7, 13]),
            (1001, [7, 11, 13]),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                result = factorize(number)
                self.assertIsInstance(result, list)
                self.assertEqual(result, expected)

    def test_negative_numbers_start_with_minus_one(self):
        '''TC-PRI-25. factorize: у отрицательных первым идет -1'''
        cases = [(-12, [-1, 2, 2, 3]), (-60, [-1, 2, 2, 3, 5]), (-7, [-1, 7]), (-2, [-1, 2]), (-91, [-1, 7, 13])]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(factorize(number), expected)

    def test_one_and_minus_one(self):
        '''TC-PRI-26. factorize: 1 без множителей, -1 только -1'''
        self.assertEqual(factorize(1), [])
        self.assertEqual(factorize(-1), [-1])

    def test_primes_give_single_factor(self):
        '''TC-PRI-27. factorize: простое число раскладывается в себя'''
        for p in SMALL_PRIMES + LARGE_PRIMES:
            with self.subTest(prime=p):
                self.assertEqual(factorize(p), [p])

    def test_prime_powers(self):
        '''TC-PRI-28. factorize: степени простых'''
        for p, k in [(2, 1), (2, 10), (3, 5), (7, 4), (97, 3)]:
            with self.subTest(p=p, k=k):
                self.assertEqual(factorize(p**k), [p] * k)

    def test_large_numbers(self):
        '''TC-PRI-29. factorize: большие числа'''
        cases = [
            (10**12, [2] * 12 + [5] * 12),
            (10**12 + 39, [10**12 + 39]),
            (999979 * 999983, [999979, 999983]),
            (2**40, [2] * 40),
            (-(10**12), [-1] + [2] * 12 + [5] * 12),
            (10**9 + 7, [10**9 + 7]),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(factorize(number), expected)

    def test_product_of_factors_equals_number(self):
        '''TC-PRI-30. factorize: произведение множителей равно числу'''
        numbers = [n for n in range(-300, 301) if n != 0] + [10**6, 123456789, 10**12 - 1]
        for number in numbers:
            with self.subTest(number=number):
                product = 1
                for factor in factorize(number):
                    product *= factor
                self.assertEqual(product, number)

    def test_all_factors_prime_and_non_decreasing(self):
        '''TC-PRI-31. factorize: множители простые и не убывают'''
        for number in range(-300, 301):
            if number == 0:
                continue
            with self.subTest(number=number):
                factors = factorize(number)
                body = factors[1:] if number < 0 else factors
                for factor in body:
                    self.assertIs(type(factor), int)
                    self.assertTrue(is_prime(factor))
                self.assertEqual(body, sorted(body))

    def test_minus_one_only_for_negative_and_only_first(self):
        '''TC-PRI-32. factorize: -1 есть только у отрицательных, один'''
        for number in range(1, 201):
            with self.subTest(number=number):
                positive = factorize(number)
                negative = factorize(-number)
                self.assertNotIn(-1, positive)
                self.assertEqual(negative[0], -1)
                self.assertEqual(negative[1:], positive)
                self.assertEqual(negative.count(-1), 1)

    def test_zero_raises_value_error(self):
        '''TC-PRI-33. factorize: ValueError на ноль'''
        with self.assertRaisesRegex(ValueError, "0 нельзя разложить"):
            factorize(0)

    def test_type_error(self):
        '''TC-PRI-34. factorize: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    factorize(bad)

    def test_type_error_bool(self):
        '''TC-PRI-35. factorize: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    factorize(flag)

    def test_consistent_with_primes_up_to(self):
        '''TC-PRI-36. factorize: множители лежат среди primes_up_to'''
        known = set(primes_up_to(1000))
        for number in range(2, 1001):
            with self.subTest(number=number):
                self.assertTrue(set(factorize(number)) <= known)

    def test_performance_large_prime(self):
        '''TC-PRI-37. factorize: простое 10**12 + 39 быстрее 3 с'''
        started = time.perf_counter()
        result = factorize(10**12 + 39)
        elapsed = time.perf_counter() - started
        self.assertEqual(result, [10**12 + 39])
        self.assertLess(elapsed, TIME_LIMIT_SECONDS)


def load_tests(loader, standard_tests, pattern):
    '''Расставляет тесты по номеру кейса TC-PRI-NN из docstring.'''
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        found = re.match(r"TC-PRI-(\d+)\.", test.shortDescription() or "")
        if found is None:
            raise ValueError("у теста %s нет номера TC-PRI-NN в docstring" % test.id())
        return int(found.group(1))

    return unittest.TestSuite(sorted(flatten(standard_tests), key=case_number))


if __name__ == "__main__":
    unittest.main()

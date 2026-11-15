import math
import re
import time
import unittest

from numtheory.sequences import fibonacci, fibonacci_list, factorial

NOT_INTEGERS = (2.5, "7", None)
BOOLEANS = (True, False)

TIME_LIMIT_SECONDS = 5.0


class FibonacciTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-SEQ-01. fibonacci: табличные значения F(n)'''
        cases = [
            (3, 2), (4, 3), (5, 5), (6, 8), (7, 13), (10, 55), (15, 610), (20, 6765),
            (30, 832040), (40, 102334155), (50, 12586269025), (60, 1548008755920),
            (90, 2880067194370816120), (100, 354224848179261915075),
        ]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), expected)

    def test_base_cases(self):
        '''TC-SEQ-02. fibonacci: границы 0, 1 и 2'''
        cases = [(0, 0), (1, 1), (2, 1)]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), expected)

    def test_recurrence_positive(self):
        '''TC-SEQ-03. fibonacci: F(n) = F(n-1) + F(n-2), n до 200'''
        for n in range(2, 201):
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), fibonacci(n - 1) + fibonacci(n - 2))

    def test_negative_known_values(self):
        '''TC-SEQ-04. fibonacci: отрицательные номера из документации'''
        cases = [(-1, 1), (-2, -1), (-3, 2), (-4, -3), (-5, 5), (-6, -8), (-10, -55)]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), expected)

    def test_negative_index_formula(self):
        '''TC-SEQ-05. fibonacci: F(-n) = (-1)^(n+1) * F(n), n до 60'''
        for n in range(1, 61):
            with self.subTest(n=n):
                self.assertEqual(fibonacci(-n), (-1) ** (n + 1) * fibonacci(n))

    def test_recurrence_across_zero(self):
        '''TC-SEQ-06. fibonacci: F(n) = F(n+2) - F(n+1) через ноль'''
        for n in range(-40, 41):
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n), fibonacci(n + 2) - fibonacci(n + 1))

    def test_cassini_identity(self):
        '''TC-SEQ-07. fibonacci: тождество Кассини для n от -30 до 100'''
        for n in range(-30, 101):
            with self.subTest(n=n):
                self.assertEqual(fibonacci(n - 1) * fibonacci(n + 1) - fibonacci(n) ** 2, (-1) ** n)

    def test_gcd_property(self):
        '''TC-SEQ-08. fibonacci: gcd(F(m), F(n)) = F(gcd(m, n))'''
        pairs = [(12, 18), (10, 15), (7, 13), (30, 45), (24, 36), (100, 75), (64, 48), (17, 17)]
        for m, n in pairs:
            with self.subTest(m=m, n=n):
                self.assertEqual(math.gcd(fibonacci(m), fibonacci(n)), fibonacci(math.gcd(m, n)))

    def test_large_argument_no_recursion_error(self):
        '''TC-SEQ-09. fibonacci: аргумент 5000 и формулы удвоения'''
        half = 2500
        self.assertEqual(fibonacci(2 * half), fibonacci(half) * (2 * fibonacci(half + 1) - fibonacci(half)))
        self.assertEqual(fibonacci(2 * half + 1), fibonacci(half + 1) ** 2 + fibonacci(half) ** 2)
        self.assertEqual(fibonacci(-2 * half), -fibonacci(2 * half))
        self.assertEqual(fibonacci(-2 * half + 1), fibonacci(2 * half - 1))

    def test_result_type(self):
        '''TC-SEQ-10. fibonacci: результат всегда int'''
        for n in (-100, -7, 0, 1, 2, 50, 3000):
            with self.subTest(n=n):
                result = fibonacci(n)
                self.assertIsInstance(result, int)
                self.assertNotIsInstance(result, bool)

    def test_type_error_not_integer(self):
        '''TC-SEQ-11. fibonacci: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    fibonacci(bad)

    def test_type_error_bool(self):
        '''TC-SEQ-12. fibonacci: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    fibonacci(flag)

    def test_performance_large_argument(self):
        '''TC-SEQ-13. fibonacci: 10**5 укладывается в лимит времени'''
        started = time.perf_counter()
        result = fibonacci(10 ** 5)
        elapsed = time.perf_counter() - started
        self.assertGreater(result.bit_length(), 69000)
        self.assertLess(elapsed, TIME_LIMIT_SECONDS)


class FibonacciListTestCase(unittest.TestCase):
    def test_small_boundaries(self):
        '''TC-SEQ-14. fibonacci_list: границы 0, 1, 2 и 3'''
        cases = [(0, []), (1, [0]), (2, [0, 1]), (3, [0, 1, 1])]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(fibonacci_list(n), expected)

    def test_documentation_example(self):
        '''TC-SEQ-15. fibonacci_list: пример из документации'''
        self.assertEqual(fibonacci_list(8), [0, 1, 1, 2, 3, 5, 8, 13])
        self.assertEqual(
            fibonacci_list(16),
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610],
        )

    def test_length_equals_argument(self):
        '''TC-SEQ-16. fibonacci_list: длина списка равна number'''
        for n in (0, 1, 2, 5, 10, 50, 300):
            with self.subTest(n=n):
                self.assertEqual(len(fibonacci_list(n)), n)

    def test_matches_fibonacci(self):
        '''TC-SEQ-17. fibonacci_list: элемент i равен fibonacci(i)'''
        for n in (1, 2, 10, 60):
            result = fibonacci_list(n)
            for i in range(n):
                with self.subTest(n=n, i=i):
                    self.assertEqual(result[i], fibonacci(i))

    def test_recurrence_inside_list(self):
        '''TC-SEQ-18. fibonacci_list: элемент равен сумме двух предыдущих'''
        result = fibonacci_list(200)
        for i in range(2, len(result)):
            with self.subTest(i=i):
                self.assertEqual(result[i], result[i - 1] + result[i - 2])
        self.assertEqual(result[:2], [0, 1])

    def test_value_error_negative(self):
        '''TC-SEQ-19. fibonacci_list: ValueError на отрицательное number'''
        for bad in (-1, -2, -100):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(ValueError, "не может быть отрицательным"):
                    fibonacci_list(bad)

    def test_returns_independent_lists(self):
        '''TC-SEQ-20. fibonacci_list: тип list и новый список на вызов'''
        first = fibonacci_list(5)
        self.assertIsInstance(first, list)
        for item in first:
            self.assertIsInstance(item, int)
        first.append(999)
        first[0] = 42
        self.assertEqual(fibonacci_list(5), [0, 1, 1, 2, 3])
        self.assertIsNot(fibonacci_list(0), fibonacci_list(0))

    def test_large_argument(self):
        '''TC-SEQ-21. fibonacci_list: аргумент 5000 без ошибок'''
        result = fibonacci_list(5000)
        self.assertEqual(len(result), 5000)
        self.assertEqual(result[-1], fibonacci(4999))
        self.assertEqual(result[-2], fibonacci(4998))
        self.assertEqual(result[2499] * (2 * result[2500] - result[2499]), result[4998])

    def test_type_error_not_integer(self):
        '''TC-SEQ-22. fibonacci_list: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    fibonacci_list(bad)

    def test_type_error_bool(self):
        '''TC-SEQ-23. fibonacci_list: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    fibonacci_list(flag)


class FactorialTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-SEQ-24. factorial: табличные значения n!'''
        cases = [
            (3, 6), (4, 24), (5, 120), (6, 720), (10, 3628800), (12, 479001600),
            (15, 1307674368000), (20, 2432902008176640000),
            (21, 51090942171709440000), (25, 15511210043330985984000000),
        ]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(factorial(n), expected)

    def test_base_cases(self):
        '''TC-SEQ-25. factorial: границы 0, 1 и 2'''
        cases = [(0, 1), (1, 1), (2, 2)]
        for n, expected in cases:
            with self.subTest(n=n):
                self.assertEqual(factorial(n), expected)

    def test_matches_math_factorial_oracle(self):
        '''TC-SEQ-26. factorial: оракул math.factorial, n от 0 до 200'''
        for n in range(201):
            with self.subTest(n=n):
                self.assertEqual(factorial(n), math.factorial(n))

    def test_recurrence(self):
        '''TC-SEQ-27. factorial: n! = n * (n-1)!, n от 1 до 150'''
        for n in range(1, 151):
            with self.subTest(n=n):
                self.assertEqual(factorial(n), n * factorial(n - 1))

    def test_value_error_negative(self):
        '''TC-SEQ-28. factorial: ValueError на отрицательное number'''
        for bad in (-1, -2, -100):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(ValueError, "факториал отрицательного числа"):
                    factorial(bad)

    def test_result_type(self):
        '''TC-SEQ-29. factorial: результат всегда int'''
        for n in (0, 1, 2, 10, 25, 500):
            with self.subTest(n=n):
                result = factorial(n)
                self.assertIsInstance(result, int)
                self.assertNotIsInstance(result, bool)

    def test_large_argument_no_recursion_error(self):
        '''TC-SEQ-30. factorial: аргумент 5000 против math.factorial'''
        self.assertEqual(factorial(5000), math.factorial(5000))
        self.assertEqual(factorial(5000), 5000 * factorial(4999))

    def test_trailing_zeros_legendre(self):
        '''TC-SEQ-31. factorial: нули на конце по формуле Лежандра'''
        for n in (5, 24, 25, 100, 125, 1000, 5000):
            expected = 0
            power = 5
            while power <= n:
                expected += n // power
                power *= 5
            value = factorial(n)
            zeros = 0
            while value % 10 == 0:
                value //= 10
                zeros += 1
            with self.subTest(n=n):
                self.assertEqual(zeros, expected)

    def test_type_error_not_integer(self):
        '''TC-SEQ-32. factorial: TypeError на нецелый number'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    factorial(bad)

    def test_type_error_bool(self):
        '''TC-SEQ-33. factorial: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    factorial(flag)

    def test_performance_large_argument(self):
        '''TC-SEQ-34. factorial: 20000 укладывается в лимит времени'''
        started = time.perf_counter()
        result = factorial(20000)
        elapsed = time.perf_counter() - started
        self.assertEqual(result, math.factorial(20000))
        self.assertLess(elapsed, TIME_LIMIT_SECONDS)


def load_tests(loader, standard_tests, pattern):
    '''Расставляет тесты по номеру кейса TC-SEQ-NN из docstring.'''
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        found = re.match(r"TC-SEQ-(\d+)\.", test.shortDescription() or "")
        if found is None:
            raise ValueError("у теста %s нет номера TC-SEQ-NN в docstring" % test.id())
        return int(found.group(1))

    return unittest.TestSuite(sorted(flatten(standard_tests), key=case_number))


if __name__ == "__main__":
    unittest.main()

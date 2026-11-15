import math
import re
import unittest
from fractions import Fraction
from unittest import mock

from numtheory.divisors import gcd, lcm, divisors, is_perfect, euler_phi

NOT_INTEGERS = (2.5, "7", None)
BOOLEANS = (True, False)

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 97, 7919)


class GcdTestCase(unittest.TestCase):
    def test_positive_numbers(self):
        '''TC-DIV-01. gcd: положительные числа'''
        cases = [(48, 18, 6), (18, 48, 6), (17, 5, 1), (12, 12, 12), (100, 10, 10), (35, 64, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = gcd(a, b)
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_negative_numbers_sign_ignored(self):
        '''TC-DIV-02. gcd: отрицательные аргументы, знак не влияет'''
        cases = [(-12, 18, 6), (12, -18, 6), (-12, -18, 6), (-7, 7, 7), (-17, 5, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = gcd(a, b)
                self.assertEqual(result, expected)
                self.assertGreaterEqual(result, 0)

    def test_zero_arguments(self):
        '''TC-DIV-03. gcd: ноль в любой позиции'''
        cases = [(7, 0, 7), (0, 7, 7), (-7, 0, 7), (0, -7, 7), (0, 0, 0)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_unit_and_small_boundaries(self):
        '''TC-DIV-04. gcd: границы 1, -1 и 2'''
        cases = [(1, 1, 1), (1, 99, 1), (-1, 99, 1), (99, -1, 1), (2, 2, 2), (2, 4, 2), (2, 3, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_large_numbers(self):
        '''TC-DIV-05. gcd: большие числа до 10**12'''
        cases = [
            (10**12, 10**6, 10**6),
            (2**40, 2**30 * 3, 2**30),
            (10**12, 10**12 + 1, 1),
            (-(10**12), 10**12, 10**12),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_matches_math_gcd_oracle(self):
        '''TC-DIV-06. gcd: оракул math.gcd на парах от -30 до 30'''
        values = range(-30, 31)
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    self.assertEqual(gcd(a, b), math.gcd(a, b))

    def test_result_divides_both_arguments(self):
        '''TC-DIV-07. gcd: делит оба аргумента, gcd(a, b) = gcd(b, a)'''
        pairs = [(48, 18), (-12, 18), (17, 5), (1000, 250), (91, 143), (10**12, 10**6)]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                result = gcd(a, b)
                self.assertGreater(result, 0)
                self.assertEqual(a % result, 0)
                self.assertEqual(b % result, 0)
                self.assertEqual(result, gcd(b, a))

    def test_type_error_first_argument(self):
        '''TC-DIV-08. gcd: TypeError на нецелый number1'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number1 должен быть целым числом"):
                    gcd(bad, 5)

    def test_type_error_second_argument(self):
        '''TC-DIV-09. gcd: TypeError на нецелый number2'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number2 должен быть целым числом"):
                    gcd(5, bad)

    def test_type_error_bool(self):
        '''TC-DIV-10. gcd: TypeError на bool в обеих позициях'''
        for flag in BOOLEANS:
            with self.subTest(position="first", value=flag):
                with self.assertRaises(TypeError):
                    gcd(flag, 5)
            with self.subTest(position="second", value=flag):
                with self.assertRaises(TypeError):
                    gcd(5, flag)


class LcmTestCase(unittest.TestCase):
    def test_positive_numbers(self):
        '''TC-DIV-11. lcm: положительные числа'''
        cases = [(4, 6, 12), (6, 4, 12), (3, 5, 15), (12, 12, 12), (3, 9, 9), (21, 6, 42)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = lcm(a, b)
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_negative_numbers_sign_ignored(self):
        '''TC-DIV-12. lcm: отрицательные аргументы, знак не влияет'''
        cases = [(-4, 6, 12), (4, -6, 12), (-4, -6, 12), (-3, 3, 3)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = lcm(a, b)
                self.assertEqual(result, expected)
                self.assertGreaterEqual(result, 0)

    def test_zero_arguments(self):
        '''TC-DIV-13. lcm: ноль дает 0'''
        cases = [(5, 0), (0, 5), (-5, 0), (0, -5), (0, 0)]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(lcm(a, b), 0)

    def test_unit_and_small_boundaries(self):
        '''TC-DIV-14. lcm: границы 1, -1 и 2'''
        cases = [(1, 1, 1), (1, 99, 99), (-1, 99, 99), (99, -1, 99), (2, 2, 2), (2, 3, 6), (2, 4, 4)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(lcm(a, b), expected)

    def test_large_numbers(self):
        '''TC-DIV-15. lcm: большие числа'''
        cases = [
            (10**6, 10**6 + 1, 10**6 * (10**6 + 1)),
            (2**40, 3**20, 2**40 * 3**20),
            (10**12, 10**6, 10**12),
            (-(10**12), 10**12, 10**12),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(lcm(a, b), expected)

    def test_matches_math_lcm_oracle(self):
        '''TC-DIV-16. lcm: оракул math.lcm на парах от -30 до 30'''
        values = range(-30, 31)
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    self.assertEqual(lcm(a, b), math.lcm(a, b))

    def test_gcd_lcm_product_identity_and_multiple(self):
        '''TC-DIV-17. lcm: gcd * lcm = |a * b|, кратно обоим'''
        pairs = [(4, 6), (-4, 6), (17, 5), (48, 18), (91, 143), (10**6, 10**6 + 1)]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                multiple = lcm(a, b)
                self.assertEqual(gcd(a, b) * multiple, abs(a * b))
                self.assertEqual(multiple % a, 0)
                self.assertEqual(multiple % b, 0)

    def test_type_error_first_argument(self):
        '''TC-DIV-18. lcm: TypeError на нецелый number1'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number1 должен быть целым числом"):
                    lcm(bad, 5)

    def test_type_error_second_argument(self):
        '''TC-DIV-19. lcm: TypeError на нецелый number2'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number2 должен быть целым числом"):
                    lcm(5, bad)

    def test_type_error_bool(self):
        '''TC-DIV-20. lcm: TypeError на bool в обеих позициях'''
        for flag in BOOLEANS:
            with self.subTest(position="first", value=flag):
                with self.assertRaises(TypeError):
                    lcm(flag, 5)
            with self.subTest(position="second", value=flag):
                with self.assertRaises(TypeError):
                    lcm(5, flag)


class DivisorsTestCase(unittest.TestCase):
    def test_positive_numbers(self):
        '''TC-DIV-21. divisors: положительные числа, полный квадрат'''
        cases = [
            (36, [1, 2, 3, 4, 6, 9, 12, 18, 36]),
            (12, [1, 2, 3, 4, 6, 12]),
            (28, [1, 2, 4, 7, 14, 28]),
            (49, [1, 7, 49]),
            (100, [1, 2, 4, 5, 10, 20, 25, 50, 100]),
        ]
        for number, expected in cases:
            with self.subTest(number=number):
                result = divisors(number)
                self.assertIsInstance(result, list)
                self.assertEqual(result, expected)

    def test_negative_numbers_same_as_modulus(self):
        '''TC-DIV-22. divisors: отрицательные числа, как для модуля'''
        for number in (-6, -36, -13, -100):
            with self.subTest(number=number):
                result = divisors(number)
                self.assertEqual(result, divisors(-number))
                self.assertTrue(all(d > 0 for d in result))
        self.assertEqual(divisors(-6), [1, 2, 3, 6])

    def test_boundaries_one_two_and_primes(self):
        '''TC-DIV-23. divisors: границы 1, -1, 2 и простые числа'''
        self.assertEqual(divisors(1), [1])
        self.assertEqual(divisors(-1), [1])
        self.assertEqual(divisors(2), [1, 2])
        for p in SMALL_PRIMES + (10**9 + 7,):
            with self.subTest(prime=p):
                self.assertEqual(divisors(p), [1, p])

    def test_prime_powers(self):
        '''TC-DIV-24. divisors: степени простых'''
        for p, k in [(2, 10), (3, 5), (7, 4), (2, 1)]:
            with self.subTest(p=p, k=k):
                self.assertEqual(divisors(p**k), [p**i for i in range(k + 1)])

    def test_zero_raises_value_error(self):
        '''TC-DIV-25. divisors: ValueError на ноль'''
        with self.assertRaisesRegex(ValueError, "бесконечно много"):
            divisors(0)

    def test_matches_brute_force_oracle(self):
        '''TC-DIV-26. divisors: оракул перебором для n от 1 до 200'''
        for n in range(1, 201):
            with self.subTest(n=n):
                result = divisors(n)
                expected = [d for d in range(1, n + 1) if n % d == 0]
                self.assertEqual(result, expected)
                self.assertEqual(result, sorted(result))
                self.assertTrue(all(n % d == 0 for d in result))

    def test_large_number(self):
        '''TC-DIV-27. divisors: большое число 10**12, 169 делителей'''
        number = 10**12
        result = divisors(number)
        self.assertEqual(len(result), 13 * 13)
        self.assertEqual(result, sorted(set(result)))
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], number)
        self.assertTrue(all(number % d == 0 for d in result))

    def test_type_error(self):
        '''TC-DIV-28. divisors: TypeError на нецелый number и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    divisors(bad)


class IsPerfectTestCase(unittest.TestCase):
    def test_known_perfect_numbers(self):
        '''TC-DIV-29. is_perfect: известные совершенные числа'''
        for number in (6, 28, 496, 8128, 33550336):
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), True)

    def test_neighbours_and_other_numbers_are_not_perfect(self):
        '''TC-DIV-30. is_perfect: несовершенные числа дают False'''
        not_perfect = [5, 7, 27, 29, 495, 497, 8127, 8129]
        not_perfect += [2, 3, 13, 97]
        not_perfect += [12, 18, 20, 24]
        not_perfect += [4, 8, 9, 100]
        for number in not_perfect:
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), False)

    def test_zero_one_and_negative_are_not_perfect(self):
        '''TC-DIV-31. is_perfect: 0, 1 и отрицательные дают False'''
        for number in (0, 1, -1, -6, -28, -496):
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), False)

    def test_only_known_perfect_numbers_below_10000(self):
        '''TC-DIV-32. is_perfect: оракул, совершенные числа до 10000'''
        found = [n for n in range(-10, 10001) if is_perfect(n)]
        self.assertEqual(found, [6, 28, 496, 8128])

    def test_matches_sum_of_proper_divisors_definition(self):
        '''TC-DIV-33. is_perfect: оракул по определению, n от 2 до 300'''
        for n in range(2, 301):
            with self.subTest(n=n):
                expected = sum(d for d in range(1, n) if n % d == 0) == n
                self.assertEqual(is_perfect(n), expected)

    def test_large_number(self):
        '''TC-DIV-34. is_perfect: большое число 10**12'''
        self.assertIs(is_perfect(10**12), False)

    def test_type_error(self):
        '''TC-DIV-35. is_perfect: TypeError на нецелый number и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    is_perfect(bad)


class EulerPhiTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-DIV-36. euler_phi: известные значения'''
        cases = [(1, 1), (2, 1), (3, 2), (4, 2), (6, 2), (9, 6), (10, 4), (12, 4), (13, 12), (36, 12), (100, 40)]
        for number, expected in cases:
            with self.subTest(number=number):
                result = euler_phi(number)
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_matches_coprime_count_oracle(self):
        '''TC-DIV-37. euler_phi: оракул по взаимно простым, n до 200'''
        for n in range(1, 201):
            with self.subTest(n=n):
                expected = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
                self.assertEqual(euler_phi(n), expected)

    def test_prime_gives_p_minus_one(self):
        '''TC-DIV-38. euler_phi: phi(p) = p - 1 для простых'''
        for p in SMALL_PRIMES + (10**9 + 7,):
            with self.subTest(prime=p):
                self.assertEqual(euler_phi(p), p - 1)

    def test_prime_power(self):
        '''TC-DIV-39. euler_phi: phi(p**k) = p**(k - 1) * (p - 1)'''
        for p in (2, 3, 5, 7):
            for k in range(1, 7):
                with self.subTest(p=p, k=k):
                    self.assertEqual(euler_phi(p**k), p ** (k - 1) * (p - 1))

    def test_multiplicative_for_coprime_arguments(self):
        '''TC-DIV-40. euler_phi: мультипликативность для взаимно простых'''
        for a in range(1, 41):
            for b in range(1, 41):
                if math.gcd(a, b) != 1:
                    continue
                with self.subTest(a=a, b=b):
                    self.assertEqual(euler_phi(a * b), euler_phi(a) * euler_phi(b))

    def test_large_numbers(self):
        '''TC-DIV-41. euler_phi: большие числа'''
        self.assertEqual(euler_phi(10**12), 4 * 10**11)
        self.assertEqual(euler_phi(10007 * 10009), 10006 * 10008)

    def test_zero_and_negative_raise_value_error(self):
        '''TC-DIV-42. euler_phi: ValueError на 0 и отрицательные'''
        for number in (0, -1, -36, -(10**12)):
            with self.subTest(number=number):
                with self.assertRaisesRegex(ValueError, "натуральных"):
                    euler_phi(number)

    def test_type_error(self):
        '''TC-DIV-43. euler_phi: TypeError на нецелый number и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    euler_phi(bad)

    def test_integration_with_factorize_formula(self):
        '''TC-DIV-44. euler_phi: интеграция с factorize'''
        from numtheory.primes import factorize
        for n in range(2, 201):
            with self.subTest(n=n):
                expected = Fraction(n)
                for p in set(factorize(n)):
                    expected *= Fraction(p - 1, p)
                self.assertEqual(euler_phi(n), expected)

    def test_isolated_with_stubbed_factorize(self):
        '''TC-DIV-45. euler_phi: изоляция, factorize заменен заглушкой'''
        with mock.patch("numtheory.divisors.factorize", return_value=[2, 2, 3, 3]) as fake:
            result = euler_phi(36)
        fake.assert_called_once_with(36)
        self.assertEqual(result, 12)


def load_tests(loader, standard_tests, pattern):
    '''Расставляет тесты по номеру кейса TC-DIV-NN из docstring.'''
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        found = re.match(r"TC-DIV-(\d+)\.", test.shortDescription() or "")
        if found is None:
            raise ValueError("у теста %s нет номера TC-DIV-NN в docstring" % test.id())
        return int(found.group(1))

    return unittest.TestSuite(sorted(flatten(standard_tests), key=case_number))


if __name__ == "__main__":
    unittest.main()

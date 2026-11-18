import re
import unittest

from numtheory.divisors import gcd, lcm, divisors, is_perfect, euler_phi


class GcdTestCase(unittest.TestCase):
    def test_positive(self):
        '''TC-DIV-01. gcd: положительные числа'''
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(100, 75), 25)
        self.assertEqual(gcd(17, 5), 1)

    def test_negative(self):
        '''TC-DIV-02. gcd: отрицательные аргументы'''
        self.assertEqual(gcd(-12, 18), 6)
        self.assertEqual(gcd(12, -18), 6)
        self.assertEqual(gcd(-12, -18), 6)

    def test_zero(self):
        '''TC-DIV-03. gcd: ноль в любой позиции'''
        self.assertEqual(gcd(7, 0), 7)
        self.assertEqual(gcd(0, 7), 7)
        self.assertEqual(gcd(-5, 0), 5)
        self.assertEqual(gcd(0, 0), 0)


class LcmTestCase(unittest.TestCase):
    def test_positive(self):
        '''TC-DIV-04. lcm: положительные числа'''
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(3, 5), 15)
        self.assertEqual(lcm(21, 6), 42)

    def test_negative(self):
        '''TC-DIV-05. lcm: отрицательные аргументы'''
        self.assertEqual(lcm(-4, 6), 12)
        self.assertEqual(lcm(4, -6), 12)
        self.assertEqual(lcm(-4, -6), 12)

    def test_zero(self):
        '''TC-DIV-06. lcm: ноль дает 0'''
        self.assertEqual(lcm(5, 0), 0)
        self.assertEqual(lcm(0, 5), 0)
        self.assertEqual(lcm(0, 0), 0)


class DivisorsTestCase(unittest.TestCase):
    def test_positive(self):
        '''TC-DIV-07. divisors: положительные числа'''
        self.assertEqual(divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(divisors(28), [1, 2, 4, 7, 14, 28])
        self.assertEqual(divisors(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])

    def test_negative(self):
        '''TC-DIV-08. divisors: отрицательное число как его модуль'''
        self.assertEqual(divisors(-6), [1, 2, 3, 6])
        self.assertEqual(divisors(-12), [1, 2, 3, 4, 6, 12])

    def test_one_and_prime(self):
        '''TC-DIV-09. divisors: 1 и простое число'''
        self.assertEqual(divisors(1), [1])
        self.assertEqual(divisors(13), [1, 13])

    def test_zero(self):
        '''TC-DIV-10. divisors: ValueError на ноль'''
        with self.assertRaises(ValueError):
            divisors(0)


class IsPerfectTestCase(unittest.TestCase):
    def test_perfect(self):
        '''TC-DIV-11. is_perfect: совершенные числа'''
        self.assertTrue(is_perfect(6))
        self.assertTrue(is_perfect(28))
        self.assertTrue(is_perfect(496))

    def test_not_perfect(self):
        '''TC-DIV-12. is_perfect: несовершенные числа дают False'''
        self.assertFalse(is_perfect(12))
        self.assertFalse(is_perfect(8))
        self.assertFalse(is_perfect(10))
        self.assertFalse(is_perfect(100))

    def test_zero_one_and_negative(self):
        '''TC-DIV-13. is_perfect: 0, 1 и отрицательные дают False'''
        self.assertFalse(is_perfect(0))
        self.assertFalse(is_perfect(1))
        self.assertFalse(is_perfect(-6))
        self.assertFalse(is_perfect(-28))


class EulerPhiTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-DIV-14. euler_phi: известные значения'''
        self.assertEqual(euler_phi(1), 1)
        self.assertEqual(euler_phi(9), 6)
        self.assertEqual(euler_phi(10), 4)
        self.assertEqual(euler_phi(36), 12)

    def test_prime(self):
        '''TC-DIV-15. euler_phi: простое p дает p - 1'''
        self.assertEqual(euler_phi(2), 1)
        self.assertEqual(euler_phi(7), 6)
        self.assertEqual(euler_phi(13), 12)
        self.assertEqual(euler_phi(97), 96)

    def test_not_natural(self):
        '''TC-DIV-16. euler_phi: ValueError на 0 и отрицательные'''
        self.assertRaises(ValueError, euler_phi, 0)
        self.assertRaises(ValueError, euler_phi, -1)
        self.assertRaises(ValueError, euler_phi, -10)


class TypeErrorTestCase(unittest.TestCase):
    def test_not_integer(self):
        '''TC-DIV-17. divisors: TypeError на нецелый аргумент и bool'''
        for value in (2.5, "7", None, True, False):
            with self.subTest(value=value):
                self.assertRaises(TypeError, gcd, value, 4)
                self.assertRaises(TypeError, gcd, 4, value)
                self.assertRaises(TypeError, lcm, value, 4)
                self.assertRaises(TypeError, lcm, 4, value)
                self.assertRaises(TypeError, divisors, value)
                self.assertRaises(TypeError, is_perfect, value)
                self.assertRaises(TypeError, euler_phi, value)


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

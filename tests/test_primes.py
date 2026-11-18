import re
import time
import unittest

from numtheory.primes import is_prime, primes_up_to, factorize


class IsPrimeTestCase(unittest.TestCase):
    def test_small_primes(self):
        '''TC-PRI-01. is_prime: малые простые числа'''
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(97))

    def test_composites(self):
        '''TC-PRI-02. is_prime: составные числа дают False'''
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(15))
        self.assertFalse(is_prime(100))

    def test_zero_one_and_negative(self):
        '''TC-PRI-03. is_prime: 0, 1 и отрицательные дают False'''
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(-1))
        self.assertFalse(is_prime(-7))

    def test_large_prime(self):
        '''TC-PRI-04. is_prime: большое простое 10**9 + 7'''
        self.assertTrue(is_prime(10**9 + 7))


class PrimesUpToTestCase(unittest.TestCase):
    def test_up_to_thirty(self):
        '''TC-PRI-05. primes_up_to: простые до 30'''
        self.assertEqual(primes_up_to(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_border_is_included(self):
        '''TC-PRI-06. primes_up_to: граница number включена'''
        self.assertEqual(primes_up_to(13), [2, 3, 5, 7, 11, 13])
        self.assertEqual(primes_up_to(2), [2])
        self.assertEqual(primes_up_to(12), [2, 3, 5, 7, 11])

    def test_less_than_two(self):
        '''TC-PRI-07. primes_up_to: number меньше 2 дает пустой список'''
        self.assertEqual(primes_up_to(1), [])
        self.assertEqual(primes_up_to(0), [])
        self.assertEqual(primes_up_to(-5), [])

    def test_sieve_is_fast(self):
        '''TC-PRI-08. primes_up_to: решето до 10**6 быстрее 3 с'''
        started = time.perf_counter()
        result = primes_up_to(10**6)
        elapsed = time.perf_counter() - started
        self.assertEqual(len(result), 78498)
        self.assertEqual(result[-1], 999983)
        self.assertLess(elapsed, 3.0)


class FactorizeTestCase(unittest.TestCase):
    def test_known_factorizations(self):
        '''TC-PRI-09. factorize: известные разложения'''
        self.assertEqual(factorize(12), [2, 2, 3])
        self.assertEqual(factorize(360), [2, 2, 2, 3, 3, 5])
        self.assertEqual(factorize(1001), [7, 11, 13])

    def test_prime_number(self):
        '''TC-PRI-10. factorize: простое число раскладывается в себя'''
        self.assertEqual(factorize(2), [2])
        self.assertEqual(factorize(13), [13])
        self.assertEqual(factorize(97), [97])

    def test_negative_and_one(self):
        '''TC-PRI-11. factorize: отрицательные числа, 1 и -1'''
        self.assertEqual(factorize(-12), [-1, 2, 2, 3])
        self.assertEqual(factorize(-7), [-1, 7])
        self.assertEqual(factorize(1), [])
        self.assertEqual(factorize(-1), [-1])

    def test_zero(self):
        '''TC-PRI-12. factorize: ValueError на ноль'''
        with self.assertRaises(ValueError):
            factorize(0)


class TypeErrorTestCase(unittest.TestCase):
    def test_not_integer(self):
        '''TC-PRI-13. primes: TypeError на нецелый аргумент и bool'''
        for value in (2.5, "7", None, True, False):
            with self.subTest(value=value):
                self.assertRaises(TypeError, is_prime, value)
                self.assertRaises(TypeError, primes_up_to, value)
                self.assertRaises(TypeError, factorize, value)


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

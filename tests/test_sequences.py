import re
import unittest

from numtheory.sequences import fibonacci, fibonacci_list, factorial


class FibonacciTestCase(unittest.TestCase):
    def test_table_values(self):
        '''TC-SEQ-01. fibonacci: табличные значения'''
        self.assertEqual(fibonacci(7), 13)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(20), 6765)
        self.assertEqual(fibonacci(30), 832040)

    def test_borders(self):
        '''TC-SEQ-02. fibonacci: границы 0, 1 и 2'''
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)

    def test_negative(self):
        '''TC-SEQ-03. fibonacci: отрицательные номера'''
        self.assertEqual(fibonacci(-1), 1)
        self.assertEqual(fibonacci(-2), -1)
        self.assertEqual(fibonacci(-6), -8)


class FibonacciListTestCase(unittest.TestCase):
    def test_borders(self):
        '''TC-SEQ-04. fibonacci_list: границы 0, 1 и 2'''
        self.assertEqual(fibonacci_list(0), [])
        self.assertEqual(fibonacci_list(1), [0])
        self.assertEqual(fibonacci_list(2), [0, 1])

    def test_first_ten(self):
        '''TC-SEQ-05. fibonacci_list: первые 10 чисел'''
        self.assertEqual(fibonacci_list(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_length(self):
        '''TC-SEQ-06. fibonacci_list: длина списка равна number'''
        self.assertEqual(len(fibonacci_list(5)), 5)
        self.assertEqual(len(fibonacci_list(20)), 20)

    def test_negative(self):
        '''TC-SEQ-07. fibonacci_list: ValueError на отрицательное number'''
        self.assertRaises(ValueError, fibonacci_list, -1)
        self.assertRaises(ValueError, fibonacci_list, -5)


class FactorialTestCase(unittest.TestCase):
    def test_table_values(self):
        '''TC-SEQ-08. factorial: табличные значения'''
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        self.assertEqual(factorial(20), 2432902008176640000)

    def test_borders(self):
        '''TC-SEQ-09. factorial: границы 0 и 1'''
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)

    def test_negative(self):
        '''TC-SEQ-10. factorial: ValueError на отрицательное number'''
        self.assertRaises(ValueError, factorial, -1)
        self.assertRaises(ValueError, factorial, -5)


class TypeErrorTestCase(unittest.TestCase):
    def test_not_integer(self):
        '''TC-SEQ-11. sequences: TypeError на нецелый аргумент и bool'''
        for value in (2.5, "7", None, True, False):
            with self.subTest(value=value):
                self.assertRaises(TypeError, fibonacci, value)
                self.assertRaises(TypeError, fibonacci_list, value)
                self.assertRaises(TypeError, factorial, value)


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

import re
import unittest

from numtheory.modular import extended_gcd, mod_inverse, solve_diophantine, crt


class ExtendedGcdTestCase(unittest.TestCase):
    def test_documentation_examples(self):
        '''TC-MOD-01. extended_gcd: примеры из документации'''
        self.assertEqual(extended_gcd(240, 46), (2, -9, 47))
        self.assertEqual(extended_gcd(-12, 18), (6, 1, 1))
        self.assertEqual(extended_gcd(5, 0), (5, 1, 0))
        self.assertEqual(extended_gcd(0, 0), (0, 0, 0))

    def test_result_fits_equation(self):
        '''TC-MOD-02. extended_gcd: результат удовлетворяет a*x + b*y = g'''
        g, x, y = extended_gcd(35, 15)
        self.assertEqual(g, 5)
        self.assertEqual(35 * x + 15 * y, 5)
        g, x, y = extended_gcd(17, 5)
        self.assertEqual(g, 1)
        self.assertEqual(17 * x + 5 * y, 1)
        g, x, y = extended_gcd(240, 46)
        self.assertEqual(g, 2)
        self.assertEqual(240 * x + 46 * y, 2)

    def test_negative_and_zero(self):
        '''TC-MOD-03. extended_gcd: отрицательные числа и ноль'''
        self.assertEqual(extended_gcd(12, -18), (6, -1, -1))
        self.assertEqual(extended_gcd(-12, -18), (6, 1, -1))
        self.assertEqual(extended_gcd(0, 5), (5, 0, 1))
        self.assertEqual(extended_gcd(-5, 0), (5, -1, 0))


class ModInverseTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-MOD-04. mod_inverse: известные значения'''
        self.assertEqual(mod_inverse(3, 7), 5)
        self.assertEqual(mod_inverse(-3, 7), 2)
        self.assertEqual(mod_inverse(10, 17), 12)
        self.assertEqual(mod_inverse(5, 1), 0)

    def test_gcd_not_one(self):
        '''TC-MOD-05. mod_inverse: ValueError, если НОД не равен 1'''
        self.assertRaises(ValueError, mod_inverse, 4, 8)
        self.assertRaises(ValueError, mod_inverse, 6, 9)
        self.assertRaises(ValueError, mod_inverse, 0, 5)

    def test_modulus_less_than_one(self):
        '''TC-MOD-06. mod_inverse: ValueError при модуле меньше 1'''
        self.assertRaises(ValueError, mod_inverse, 3, 0)
        self.assertRaises(ValueError, mod_inverse, 3, -7)


class SolveDiophantineTestCase(unittest.TestCase):
    def test_documentation_examples(self):
        '''TC-MOD-07. solve_diophantine: примеры из документации'''
        self.assertEqual(solve_diophantine(3, 5, 1), (2, -1, 5, -3))
        self.assertEqual(solve_diophantine(6, 9, 15), (1, 1, 3, -2))
        self.assertEqual(solve_diophantine(4, 0, 8), (2, 0, 0, 1))
        self.assertEqual(solve_diophantine(0, 4, 8), (0, 2, 1, 0))

    def test_solution_fits_equation(self):
        '''TC-MOD-08. solve_diophantine: решение подходит в уравнение'''
        x0, y0, dx, dy = solve_diophantine(3, 5, 1)
        self.assertEqual(3 * x0 + 5 * y0, 1)
        self.assertEqual(3 * (x0 + dx) + 5 * (y0 + dy), 1)
        x0, y0, dx, dy = solve_diophantine(7, 5, 3)
        self.assertEqual(7 * x0 + 5 * y0, 3)
        self.assertEqual(7 * (x0 + dx) + 5 * (y0 + dy), 3)
        x0, y0, dx, dy = solve_diophantine(12, 18, 30)
        self.assertEqual(12 * x0 + 18 * y0, 30)
        self.assertEqual(12 * (x0 + dx) + 18 * (y0 + dy), 30)

    def test_zero_right_side_and_zero_coefficient(self):
        '''TC-MOD-09. solve_diophantine: c = 0 и нулевой коэффициент'''
        self.assertEqual(solve_diophantine(3, 5, 0), (0, 0, 5, -3))
        self.assertEqual(solve_diophantine(0, 5, 10), (0, 2, 1, 0))
        self.assertEqual(solve_diophantine(6, 0, 18), (3, 0, 0, 1))
        self.assertEqual(solve_diophantine(0, 5, 0), (0, 0, 1, 0))

    def test_no_solutions(self):
        '''TC-MOD-10. solve_diophantine: ValueError, решений нет'''
        self.assertRaises(ValueError, solve_diophantine, 6, 9, 7)
        self.assertRaises(ValueError, solve_diophantine, 4, 2, 3)
        self.assertRaises(ValueError, solve_diophantine, 0, 4, 6)
        self.assertRaises(ValueError, solve_diophantine, 0, 0, 5)
        self.assertRaises(ValueError, solve_diophantine, 0, 0, 0)


class CrtTestCase(unittest.TestCase):
    def test_classic_example(self):
        '''TC-MOD-11. crt: классический пример'''
        self.assertEqual(crt([2, 3, 2], [3, 5, 7]), (23, 105))

    def test_moduli_not_coprime(self):
        '''TC-MOD-12. crt: модули не взаимно просты, система совместна'''
        self.assertEqual(crt([1, 3], [4, 6]), (9, 12))
        self.assertEqual(crt([2, 4], [6, 8]), (20, 24))
        self.assertEqual(crt([3, 5], [4, 10]), (15, 20))

    def test_inconsistent_system(self):
        '''TC-MOD-13. crt: ValueError на несовместную систему'''
        self.assertRaises(ValueError, crt, [1, 2], [4, 6])
        self.assertRaises(ValueError, crt, [1, 2], [2, 4])

    def test_wrong_lengths_and_empty(self):
        '''TC-MOD-14. crt: ValueError на разную длину и пустые списки'''
        self.assertRaises(ValueError, crt, [1, 2], [3])
        self.assertRaises(ValueError, crt, [1], [3, 5])
        self.assertRaises(ValueError, crt, [], [])

    def test_modulus_less_than_one(self):
        '''TC-MOD-15. crt: ValueError при модуле меньше 1'''
        self.assertRaises(ValueError, crt, [1], [0])
        self.assertRaises(ValueError, crt, [1], [-3])
        self.assertRaises(ValueError, crt, [1, 2], [3, 0])


class TypeErrorTestCase(unittest.TestCase):
    def test_not_integer(self):
        '''TC-MOD-16. modular: TypeError на нецелые аргументы и bool'''
        for value in (2.5, "7", None, True, False):
            with self.subTest(value=value):
                self.assertRaises(TypeError, extended_gcd, value, 1)
                self.assertRaises(TypeError, extended_gcd, 1, value)
                self.assertRaises(TypeError, mod_inverse, value, 7)
                self.assertRaises(TypeError, mod_inverse, 3, value)
                self.assertRaises(TypeError, solve_diophantine, value, 1, 1)
                self.assertRaises(TypeError, solve_diophantine, 1, value, 1)
                self.assertRaises(TypeError, solve_diophantine, 1, 1, value)
                self.assertRaises(TypeError, crt, [value], [3])
                self.assertRaises(TypeError, crt, [1], [value])
                self.assertRaises(TypeError, crt, value, [3])
                self.assertRaises(TypeError, crt, [1], value)


def load_tests(loader, standard_tests, pattern):
    '''Расставляет тесты по номеру кейса TC-MOD-NN из docstring.'''
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        found = re.match(r"TC-MOD-(\d+)\.", test.shortDescription() or "")
        if found is None:
            raise ValueError("у теста %s нет номера TC-MOD-NN в docstring" % test.id())
        return int(found.group(1))

    return unittest.TestSuite(sorted(flatten(standard_tests), key=case_number))


if __name__ == "__main__":
    unittest.main()

import math
import re
import unittest
from unittest import mock

from numtheory.modular import extended_gcd, mod_inverse, solve_diophantine, crt

NOT_INTEGERS = (2.5, "7", None)
BOOLEANS = (True, False)
NOT_SEQUENCES = (5, "12", None, 2.5, True)

DIOPHANTINE_PAIRS = [
    (3, 5), (-3, 5), (3, -5), (-3, -5), (6, 9), (-6, 9), (6, -9), (12, 18),
    (1, 1), (1, -1), (-1, 1), (7, 13), (10, 4), (5, 3), (2, 3), (9, 6),
]


class ExtendedGcdTestCase(unittest.TestCase):
    def test_positive_numbers(self):
        '''TC-MOD-01. extended_gcd: положительные числа, тождество Безу'''
        cases = [(240, 46, 2), (46, 240, 2), (17, 5, 1), (12, 12, 12), (100, 10, 10), (35, 64, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = extended_gcd(a, b)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 3)
                for item in result:
                    self.assertIsInstance(item, int)
                    self.assertNotIsInstance(item, bool)
                g, x, y = result
                self.assertEqual(g, expected)
                self.assertEqual(a * x + b * y, g)

    def test_documented_examples(self):
        '''TC-MOD-02. extended_gcd: примеры из документации'''
        self.assertEqual(extended_gcd(240, 46), (2, -9, 47))
        self.assertEqual(extended_gcd(-12, 18), (6, 1, 1))
        self.assertEqual(extended_gcd(5, 0), (5, 1, 0))
        self.assertEqual(extended_gcd(0, 0), (0, 0, 0))

    def test_negative_numbers_sign_ignored(self):
        '''TC-MOD-03. extended_gcd: отрицательные числа, g неотрицателен'''
        cases = [(-12, 18, 6), (12, -18, 6), (-12, -18, 6), (-7, 7, 7), (-17, 5, 1), (-240, -46, 2)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                g, x, y = extended_gcd(a, b)
                self.assertEqual(g, expected)
                self.assertGreaterEqual(g, 0)
                self.assertEqual(a * x + b * y, g)

    def test_zero_arguments(self):
        '''TC-MOD-04. extended_gcd: ноль, коэффициент при нуле равен 0'''
        for a in (5, -5, 1, -1, 99):
            with self.subTest(a=a, b=0):
                g, x, y = extended_gcd(a, 0)
                self.assertEqual(g, abs(a))
                self.assertEqual(abs(x), 1)
                self.assertEqual(y, 0)
                self.assertEqual(a * x, g)
        for b in (7, -7, 1, -1, 99):
            with self.subTest(a=0, b=b):
                g, x, y = extended_gcd(0, b)
                self.assertEqual(g, abs(b))
                self.assertEqual(x, 0)
                self.assertEqual(abs(y), 1)
                self.assertEqual(b * y, g)
        self.assertEqual(extended_gcd(0, 0), (0, 0, 0))

    def test_unit_and_equal_boundaries(self):
        '''TC-MOD-05. extended_gcd: границы 1, -1, равные и кратные числа'''
        cases = [(1, 1, 1), (1, 99, 1), (-1, 99, 1), (99, -1, 1), (2, 2, 2), (2, 4, 2), (4, 2, 2), (9, 10, 1), (-5, -5, 5)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                g, x, y = extended_gcd(a, b)
                self.assertEqual(g, expected)
                self.assertEqual(a * x + b * y, g)

    def test_large_numbers(self):
        '''TC-MOD-06. extended_gcd: большие числа'''
        cases = [
            (10**12, 10**6, 10**6),
            (2**40, 2**30 * 3, 2**30),
            (10**12, 10**12 + 1, 1),
            (-(10**12), 10**12, 10**12),
            (2**61 - 1, 2**31 - 1, 1),
            (10**18 + 9, 10**9 + 7, 1),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                g, x, y = extended_gcd(a, b)
                self.assertEqual(g, expected)
                self.assertEqual(a * x + b * y, g)

    def test_matches_math_gcd_and_bezout_oracle(self):
        '''TC-MOD-07. extended_gcd: оракул math.gcd на парах от -30 до 30'''
        values = range(-30, 31)
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    g, x, y = extended_gcd(a, b)
                    self.assertEqual(g, math.gcd(a, b))
                    self.assertEqual(a * x + b * y, g)

    def test_type_error(self):
        '''TC-MOD-08. extended_gcd: TypeError на нецелый a, b и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(position="a", value=bad):
                with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
                    extended_gcd(bad, 5)
            with self.subTest(position="b", value=bad):
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    extended_gcd(5, bad)


class ModInverseTestCase(unittest.TestCase):
    def test_known_values(self):
        '''TC-MOD-09. mod_inverse: известные значения, тип int'''
        cases = [(3, 7, 5), (-3, 7, 2), (10, 17, 12), (1, 2, 1), (2, 5, 3), (7, 26, 15), (17, 3120, 2753)]
        for a, m, expected in cases:
            with self.subTest(a=a, m=m):
                result = mod_inverse(a, m)
                self.assertIsInstance(result, int)
                self.assertNotIsInstance(result, bool)
                self.assertEqual(result, expected)

    def test_argument_taken_as_residue_class(self):
        '''TC-MOD-10. mod_inverse: a и a + k*m дают один результат'''
        for a, m, expected in [(3, 7, 5), (-3, 7, 2), (5, 12, 5)]:
            for k in range(-3, 4):
                with self.subTest(a=a, m=m, k=k):
                    self.assertEqual(mod_inverse(a + k * m, m), expected)

    def test_modulus_one_gives_zero(self):
        '''TC-MOD-11. mod_inverse: модуль 1 дает 0 при любом a'''
        for a in (0, 1, -1, 5, -5, 10**12):
            with self.subTest(a=a):
                self.assertEqual(mod_inverse(a, 1), 0)

    def test_no_inverse_raises_value_error(self):
        '''TC-MOD-12. mod_inverse: ValueError при НОД не равном 1'''
        cases = [(4, 8), (6, 9), (0, 5), (5, 5), (10, 5), (-4, 8), (2, 4), (0, 2)]
        for a, m in cases:
            with self.subTest(a=a, m=m):
                with self.assertRaisesRegex(ValueError, "нет обратного"):
                    mod_inverse(a, m)

    def test_modulus_below_one_raises_value_error(self):
        '''TC-MOD-13. mod_inverse: ValueError при модуле меньше 1'''
        cases = [(3, 0), (3, -7), (1, -1), (0, 0), (4, 0), (-3, -7)]
        for a, m in cases:
            with self.subTest(a=a, m=m):
                with self.assertRaisesRegex(ValueError, "модуль должен быть натуральным"):
                    mod_inverse(a, m)

    def test_boundaries_one_and_minus_one(self):
        '''TC-MOD-14. mod_inverse: границы a = 1, -1, m - 1, m = 2'''
        for m in range(2, 21):
            with self.subTest(m=m):
                self.assertEqual(mod_inverse(1, m), 1)
                self.assertEqual(mod_inverse(-1, m), m - 1)
                self.assertEqual(mod_inverse(m - 1, m), m - 1)
        self.assertEqual(mod_inverse(1, 2), 1)
        self.assertEqual(mod_inverse(3, 2), 1)

    def test_matches_builtin_pow_oracle(self):
        '''TC-MOD-15. mod_inverse: оракул pow(a, -1, m), a от -35 до 35'''
        for m in range(1, 31):
            for a in range(-35, 36):
                with self.subTest(a=a, m=m):
                    if math.gcd(a, m) == 1:
                        result = mod_inverse(a, m)
                        self.assertEqual(result, pow(a, -1, m))
                        self.assertTrue(0 <= result < m)
                        self.assertEqual(a * result % m, 1 % m)
                    else:
                        with self.assertRaises(ValueError):
                            mod_inverse(a, m)

    def test_large_numbers(self):
        '''TC-MOD-16. mod_inverse: большие модули'''
        cases = [(123456789, 10**9 + 7), (2, 2**61 - 1), (10**12 + 39, 998244353), (-(10**15), 10**9 + 9)]
        for a, m in cases:
            with self.subTest(a=a, m=m):
                result = mod_inverse(a, m)
                self.assertEqual(result, pow(a, -1, m))
                self.assertEqual(a * result % m, 1)

    def test_type_error(self):
        '''TC-MOD-17. mod_inverse: TypeError на нецелый a, m и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(position="a", value=bad):
                with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
                    mod_inverse(bad, 7)
            with self.subTest(position="m", value=bad):
                with self.assertRaisesRegex(TypeError, "m должен быть целым числом"):
                    mod_inverse(3, bad)

    def test_isolated_with_stubbed_extended_gcd(self):
        '''TC-MOD-18. mod_inverse: изоляция, extended_gcd заменен заглушкой'''
        with mock.patch("numtheory.modular.extended_gcd", return_value=(1, 3, 0)) as fake:
            result = mod_inverse(10, 7)
        fake.assert_called_once_with(10, 7)
        self.assertEqual(result, 3)
        with mock.patch("numtheory.modular.extended_gcd", return_value=(2, 1, 0)):
            with self.assertRaisesRegex(ValueError, "нет обратного"):
                mod_inverse(10, 7)


class SolveDiophantineTestCase(unittest.TestCase):
    def test_documented_examples(self):
        '''TC-MOD-19. solve_diophantine: примеры из документации'''
        cases = [((3, 5, 1), (2, -1, 5, -3)), ((6, 9, 15), (1, 1, 3, -2)), ((4, 0, 8), (2, 0, 0, 1)), ((0, 4, 8), (0, 2, 1, 0))]
        for args, expected in cases:
            with self.subTest(args=args):
                result = solve_diophantine(*args)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 4)
                for item in result:
                    self.assertIsInstance(item, int)
                    self.assertNotIsInstance(item, bool)
                self.assertEqual(result, expected)

    def test_normalization_smallest_nonnegative_x0(self):
        '''TC-MOD-20. solve_diophantine: dx > 0 и 0 <= x0 < dx'''
        for a, b in DIOPHANTINE_PAIRS:
            g = math.gcd(a, b)
            for c in range(-20, 21):
                if c % g != 0:
                    continue
                with self.subTest(a=a, b=b, c=c):
                    x0, y0, dx, dy = solve_diophantine(a, b, c)
                    self.assertGreater(dx, 0)
                    self.assertTrue(0 <= x0 < dx)
                    self.assertEqual(a * x0 + b * y0, c)

    def test_step_formulas(self):
        '''TC-MOD-21. solve_diophantine: формулы шагов dx и dy'''
        for a, b in DIOPHANTINE_PAIRS:
            g = math.gcd(a, b)
            sign = 1 if b > 0 else -1
            with self.subTest(a=a, b=b):
                _, _, dx, dy = solve_diophantine(a, b, g)
                self.assertEqual(dx, abs(b) // g)
                self.assertEqual(dy, -sign * (a // g))

    def test_substitution_for_several_parameters(self):
        '''TC-MOD-22. solve_diophantine: подстановка при t от -5 до 5'''
        cases = [(3, 5, 1), (6, 9, 15), (-4, 6, 2), (7, -3, 5), (-8, -12, 20), (10, 4, -6), (1, 1, 0), (35, 15, 5)]
        for a, b, c in cases:
            x0, y0, dx, dy = solve_diophantine(a, b, c)
            for t in range(-5, 6):
                with self.subTest(a=a, b=b, c=c, t=t):
                    self.assertEqual(a * (x0 + dx * t) + b * (y0 + dy * t), c)

    def test_parametrization_covers_all_solutions(self):
        '''TC-MOD-23. solve_diophantine: все решения из окна в серии'''
        cases = [(3, 5, 1), (6, 9, 15), (-4, 6, 2), (7, -3, 5), (4, 6, 10), (-5, -10, 15)]
        window = range(-30, 31)
        for a, b, c in cases:
            x0, y0, dx, dy = solve_diophantine(a, b, c)
            found = [(x, y) for x in window for y in window if a * x + b * y == c]
            with self.subTest(a=a, b=b, c=c):
                self.assertTrue(found)
            for x, y in found:
                with self.subTest(a=a, b=b, c=c, x=x, y=y):
                    self.assertEqual((x - x0) % dx, 0)
                    t = (x - x0) // dx
                    self.assertEqual(y, y0 + dy * t)

    def test_zero_right_hand_side(self):
        '''TC-MOD-24. solve_diophantine: c = 0, решение (0, 0) и шаги'''
        cases = [((6, 9, 0), (0, 0, 3, -2)), ((3, 5, 0), (0, 0, 5, -3)), ((-6, 9, 0), (0, 0, 3, 2))]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(solve_diophantine(*args), expected)

    def test_zero_b_fixes_x(self):
        '''TC-MOD-25. solve_diophantine: b = 0, форма (c / a, 0, 0, 1)'''
        cases = [((4, 0, 8), (2, 0, 0, 1)), ((-4, 0, 8), (-2, 0, 0, 1)), ((4, 0, 0), (0, 0, 0, 1)),
                 ((1, 0, -5), (-5, 0, 0, 1)), ((3, 0, -9), (-3, 0, 0, 1)), ((-1, 0, -7), (7, 0, 0, 1))]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(solve_diophantine(*args), expected)

    def test_zero_a_fixes_y(self):
        '''TC-MOD-26. solve_diophantine: a = 0, форма (0, c / b, 1, 0)'''
        cases = [((0, 4, 8), (0, 2, 1, 0)), ((0, -4, 8), (0, -2, 1, 0)), ((0, 4, 0), (0, 0, 1, 0)),
                 ((0, 1, -5), (0, -5, 1, 0)), ((0, 3, -9), (0, -3, 1, 0)), ((0, -1, -7), (0, 7, 1, 0))]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(solve_diophantine(*args), expected)

    def test_no_solutions_raises_value_error(self):
        '''TC-MOD-27. solve_diophantine: ValueError, c не делится на НОД'''
        cases = [(6, 9, 7), (4, 6, 3), (2, 4, 1), (-6, 9, 1), (4, 0, 3), (0, 4, 3), (0, -4, 3), (-4, 0, 5), (10, 15, 1)]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaisesRegex(ValueError, "не имеет целых решений"):
                    solve_diophantine(*args)

    def test_both_coefficients_zero_nonzero_c(self):
        '''TC-MOD-28. solve_diophantine: a = b = 0 и c != 0, нет решений'''
        for c in (1, -1, 5, 10**12):
            with self.subTest(c=c):
                with self.assertRaisesRegex(ValueError, "не имеет решений"):
                    solve_diophantine(0, 0, c)

    def test_both_coefficients_zero_zero_c(self):
        '''TC-MOD-29. solve_diophantine: a = b = c = 0, нет параметризации'''
        with self.assertRaisesRegex(ValueError, "любая пара"):
            solve_diophantine(0, 0, 0)

    def test_solvability_criterion_oracle(self):
        '''TC-MOD-30. solve_diophantine: решение есть, если g делит c'''
        values = range(-6, 7)
        for a in values:
            for b in values:
                if a == 0 and b == 0:
                    continue
                g = math.gcd(a, b)
                for c in range(-12, 13):
                    with self.subTest(a=a, b=b, c=c):
                        if c % g == 0:
                            x0, y0, dx, dy = solve_diophantine(a, b, c)
                            self.assertEqual(a * x0 + b * y0, c)
                            self.assertEqual(a * (x0 + dx) + b * (y0 + dy), c)
                        else:
                            with self.assertRaises(ValueError):
                                solve_diophantine(a, b, c)

    def test_large_numbers(self):
        '''TC-MOD-31. solve_diophantine: большие коэффициенты'''
        cases = [
            (10**9 + 7, 998244353, 10**12),
            (2**40, 2**30 * 3, 2**30 * 5),
            (-(10**9 + 7), 10**9 + 9, -(10**15)),
            (2**61 - 1, 2**31 - 1, 1),
        ]
        for a, b, c in cases:
            with self.subTest(a=a, b=b, c=c):
                x0, y0, dx, dy = solve_diophantine(a, b, c)
                self.assertEqual(a * x0 + b * y0, c)
                self.assertEqual(a * (x0 + 3 * dx) + b * (y0 + 3 * dy), c)
                self.assertGreater(dx, 0)
                self.assertTrue(0 <= x0 < dx)

    def test_type_error(self):
        '''TC-MOD-32. solve_diophantine: TypeError на нецелый и bool'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(position="a", value=bad):
                with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
                    solve_diophantine(bad, 5, 1)
            with self.subTest(position="b", value=bad):
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    solve_diophantine(3, bad, 1)
            with self.subTest(position="c", value=bad):
                with self.assertRaisesRegex(TypeError, "c должен быть целым числом"):
                    solve_diophantine(3, 5, bad)


class CrtTestCase(unittest.TestCase):
    def test_classic_and_documented_examples(self):
        '''TC-MOD-33. crt: классический пример и примеры документации'''
        cases = [
            (([2, 3, 2], [3, 5, 7]), (23, 105)),
            (([1, 3], [4, 6]), (9, 12)),
            (([-1], [7]), (6, 7)),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = crt(*args)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                for item in result:
                    self.assertIsInstance(item, int)
                    self.assertNotIsInstance(item, bool)
                self.assertEqual(result, expected)

    def test_single_congruence_and_modulus_one(self):
        '''TC-MOD-34. crt: один остаток и модуль 1'''
        cases = [
            (([3], [7]), (3, 7)),
            (([0], [7]), (0, 7)),
            (([10], [7]), (3, 7)),
            (([5], [1]), (0, 1)),
            (([3, 2], [1, 5]), (2, 5)),
            (([0, 0], [1, 1]), (0, 1)),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(crt(*args), expected)

    def test_negative_and_large_remainders_reduced(self):
        '''TC-MOD-35. crt: остатки вне диапазона приводятся по модулю'''
        cases = [
            (([-10, -3], [7, 5]), (32, 35)),
            (([100, 200], [7, 5]), (30, 35)),
            (([-1, -1, -1], [3, 5, 7]), (104, 105)),
            (([-7], [7]), (0, 7)),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                result = crt(*args)
                self.assertEqual(result, expected)
                self.assertTrue(0 <= result[0] < result[1])

    def test_moduli_not_coprime_consistent(self):
        '''TC-MOD-36. crt: модули не взаимно просты, система совместна'''
        cases = [
            (([0, 0], [4, 6]), (0, 12)),
            (([2, 2], [6, 4]), (2, 12)),
            (([3, 3], [7, 7]), (3, 7)),
            (([5, 1], [12, 8]), (17, 24)),
            (([2, 5], [6, 9]), (14, 18)),
            (([1, 1, 1], [4, 6, 10]), (1, 60)),
        ]
        for args, expected in cases:
            with self.subTest(args=args):
                self.assertEqual(crt(*args), expected)

    def test_inconsistent_system_raises_value_error(self):
        '''TC-MOD-37. crt: ValueError на несовместную систему'''
        cases = [
            ([1, 2], [4, 6]),
            ([0, 1], [2, 4]),
            ([1, 0], [2, 4]),
            ([1, 2], [6, 9]),
            ([1, 2], [5, 5]),
            ([3, 3, 4], [6, 10, 15]),
        ]
        for remainders, moduli in cases:
            with self.subTest(remainders=remainders, moduli=moduli):
                with self.assertRaisesRegex(ValueError, "несовместна"):
                    crt(remainders, moduli)

    def test_matches_brute_force_oracle_two_congruences(self):
        '''TC-MOD-38. crt: оракул перебором, пары модулей от 1 до 8'''
        for m1 in range(1, 9):
            for m2 in range(1, 9):
                size = math.lcm(m1, m2)
                for r1 in range(m1):
                    for r2 in range(m2):
                        with self.subTest(r1=r1, m1=m1, r2=r2, m2=m2):
                            solutions = [x for x in range(size) if x % m1 == r1 and x % m2 == r2]
                            if solutions:
                                self.assertEqual(len(solutions), 1)
                                self.assertEqual(crt([r1, r2], [m1, m2]), (solutions[0], size))
                            else:
                                with self.assertRaises(ValueError):
                                    crt([r1, r2], [m1, m2])

    def test_matches_brute_force_oracle_three_congruences(self):
        '''TC-MOD-39. crt: оракул перебором, тройки модулей'''
        for moduli in [(3, 5, 7), (4, 6, 10), (6, 10, 15), (4, 6, 9), (8, 12, 18)]:
            size = math.lcm(*moduli)
            m1, m2, m3 = moduli
            for r1 in range(m1):
                for r2 in range(m2):
                    for r3 in range(m3):
                        with self.subTest(moduli=moduli, r=(r1, r2, r3)):
                            solutions = [x for x in range(size) if (x % m1, x % m2, x % m3) == (r1, r2, r3)]
                            if solutions:
                                self.assertEqual(crt([r1, r2, r3], list(moduli)), (solutions[0], size))
                            else:
                                with self.assertRaises(ValueError):
                                    crt([r1, r2, r3], list(moduli))

    def test_result_satisfies_every_congruence(self):
        '''TC-MOD-40. crt: x подходит всем сравнениям, M = НОК'''
        systems = [(3, 5, 7), (4, 6, 10), (12, 18), (1, 1, 5), (8, 12, 18), (9,)]
        for moduli in systems:
            size = math.lcm(*moduli)
            for truth in range(-50, 200, 7):
                remainders = [truth for _ in moduli]
                with self.subTest(moduli=moduli, truth=truth):
                    x, step = crt(remainders, list(moduli))
                    self.assertEqual(step, size)
                    self.assertTrue(0 <= x < step)
                    self.assertEqual(x, truth % size)
                    for m in moduli:
                        self.assertEqual(x % m, truth % m)
                    self.assertEqual(crt(remainders[::-1], list(moduli)[::-1]), (x, step))

    def test_tuples_accepted(self):
        '''TC-MOD-41. crt: кортежи принимаются вместо списков'''
        self.assertEqual(crt((2, 3, 2), (3, 5, 7)), (23, 105))
        self.assertEqual(crt([2, 3, 2], (3, 5, 7)), (23, 105))
        self.assertEqual(crt((2, 3, 2), [3, 5, 7]), (23, 105))
        self.assertEqual(crt((-1,), (7,)), (6, 7))

    def test_large_moduli(self):
        '''TC-MOD-42. crt: большие модули'''
        truth = 123456789012345678
        for moduli in [(10**9 + 7, 998244353, 10**9 + 9), (2**40, 2**30 * 3, 5**20), (2**61 - 1, 2**31 - 1)]:
            size = math.lcm(*moduli)
            remainders = [truth % m for m in moduli]
            with self.subTest(moduli=moduli):
                self.assertEqual(crt(remainders, list(moduli)), (truth % size, size))

    def test_different_lengths_raise_value_error(self):
        '''TC-MOD-43. crt: ValueError при разной длине списков'''
        cases = [([1, 2], [3]), ([1], [3, 5]), ([1, 2, 3], [3, 5]), ([], [3])]
        for remainders, moduli in cases:
            with self.subTest(remainders=remainders, moduli=moduli):
                with self.assertRaisesRegex(ValueError, "поровну"):
                    crt(remainders, moduli)

    def test_empty_lists_raise_value_error(self):
        '''TC-MOD-44. crt: ValueError на пустые списки и кортежи'''
        for remainders, moduli in [([], []), ((), ())]:
            with self.subTest(remainders=remainders, moduli=moduli):
                with self.assertRaisesRegex(ValueError, "система пуста"):
                    crt(remainders, moduli)

    def test_modulus_below_one_raises_value_error(self):
        '''TC-MOD-45. crt: ValueError при модуле меньше 1'''
        cases = [([1], [0]), ([1], [-3]), ([1, 2], [3, 0]), ([1, 2], [3, -5]), ([1, 2], [0, 5])]
        for remainders, moduli in cases:
            with self.subTest(remainders=remainders, moduli=moduli):
                with self.assertRaisesRegex(ValueError, "модуль должен быть натуральным"):
                    crt(remainders, moduli)

    def test_type_error_not_a_list(self):
        '''TC-MOD-46. crt: TypeError, если аргумент не список и не кортеж'''
        for bad in NOT_SEQUENCES:
            with self.subTest(position="remainders", value=bad):
                with self.assertRaisesRegex(TypeError, "remainders должен быть списком или кортежем"):
                    crt(bad, [3])
            with self.subTest(position="moduli", value=bad):
                with self.assertRaisesRegex(TypeError, "moduli должен быть списком или кортежем"):
                    crt([1], bad)

    def test_type_error_element_not_integer(self):
        '''TC-MOD-47. crt: TypeError на нецелый элемент и bool в списке'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(position="remainders", value=bad):
                with self.assertRaisesRegex(TypeError, r"remainders\[1\] должен быть целым числом"):
                    crt([1, bad], [3, 5])
            with self.subTest(position="moduli", value=bad):
                with self.assertRaisesRegex(TypeError, r"moduli\[1\] должен быть целым числом"):
                    crt([1, 2], [3, bad])
            with self.subTest(position="tuple", value=bad):
                with self.assertRaisesRegex(TypeError, r"remainders\[0\] должен быть целым числом"):
                    crt((bad, 2), (3, 5))

    def test_integration_with_extended_gcd_and_mod_inverse(self):
        '''TC-MOD-48. crt: интеграция с extended_gcd и mod_inverse'''
        moduli = [3, 5, 7, 11]
        remainders = [2, 3, 2, 9]
        product = math.prod(moduli)
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                self.assertEqual(extended_gcd(moduli[i], moduli[j])[0], 1)
        expected = sum(r * (product // m) * mod_inverse(product // m, m) for r, m in zip(remainders, moduli)) % product
        self.assertEqual(crt(remainders, moduli), (expected, product))

    def test_isolated_with_stubbed_mod_inverse(self):
        '''TC-MOD-49. crt: изоляция, mod_inverse заменен заглушкой'''
        with mock.patch("numtheory.modular.mod_inverse", return_value=1):
            result = crt([2, 3], [3, 5])
        self.assertEqual(result, (5, 15))


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

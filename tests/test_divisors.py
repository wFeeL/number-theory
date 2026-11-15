'''
Модульные тесты numtheory/divisors.py: gcd, lcm, divisors, is_perfect, euler_phi.

Каждый тест имеет номер ручного тест-кейса TC-DIV-NN и описание в docstring.
Нумерация сквозная по файлу, один номер соответствует одной строке таблицы в отчете.
Используется только стандартная библиотека (unittest, math, fractions, unittest.mock).

Запуск из корня репозитория:
    python3 -m unittest -v
    python3 -m unittest discover -s tests -v
'''
import math
import unittest
from fractions import Fraction
from unittest import mock

from numtheory.divisors import gcd, lcm, divisors, is_perfect, euler_phi

# Значения, которые не являются целыми числами и должны давать TypeError.
NOT_INTEGERS = (2.5, "7", None)
# bool наследуется от int, но библиотека его отклоняет.
BOOLEANS = (True, False)

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 97, 7919)


class GcdTestCase(unittest.TestCase):
    '''Тесты gcd: наибольший общий делитель двух целых чисел.'''

    def test_positive_numbers(self):
        '''TC-DIV-01. Класс эквивалентности "положительные числа": gcd на типичных парах, включая взаимно простые и кратные.'''
        # подготовка
        cases = [(48, 18, 6), (18, 48, 6), (17, 5, 1), (12, 12, 12), (100, 10, 10), (35, 64, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                # действие
                result = gcd(a, b)
                # проверка
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_negative_numbers_sign_ignored(self):
        '''TC-DIV-02. Класс эквивалентности "отрицательные числа": знаки аргументов не влияют, результат неотрицателен.'''
        cases = [(-12, 18, 6), (12, -18, 6), (-12, -18, 6), (-7, 7, 7), (-17, 5, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = gcd(a, b)
                self.assertEqual(result, expected)
                self.assertGreaterEqual(result, 0)

    def test_zero_arguments(self):
        '''TC-DIV-03. Граница "ноль": gcd(a, 0) равен модулю a в обеих позициях, gcd(0, 0) равен 0.'''
        cases = [(7, 0, 7), (0, 7, 7), (-7, 0, 7), (0, -7, 7), (0, 0, 0)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_unit_and_small_boundaries(self):
        '''TC-DIV-04. Граничные значения 1, -1 и 2: gcd с единицей равен 1, gcd(2, 2) равен 2, gcd(2, 4) равен 2.'''
        cases = [(1, 1, 1), (1, 99, 1), (-1, 99, 1), (99, -1, 1), (2, 2, 2), (2, 4, 2), (2, 3, 1)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(gcd(a, b), expected)

    def test_large_numbers(self):
        '''TC-DIV-05. Большие числа до 10**12: степени двойки и десятки, соседние числа взаимно просты.'''
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
        '''TC-DIV-06. Оракул: gcd совпадает с math.gcd на всех парах от -30 до 30, включая нули и отрицательные.'''
        values = range(-30, 31)
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    self.assertEqual(gcd(a, b), math.gcd(a, b))

    def test_result_divides_both_arguments(self):
        '''TC-DIV-07. Свойство: результат gcd делит оба аргумента, а gcd(a, b) равен gcd(b, a).'''
        pairs = [(48, 18), (-12, 18), (17, 5), (1000, 250), (91, 143), (10**12, 10**6)]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                result = gcd(a, b)
                self.assertGreater(result, 0)
                self.assertEqual(a % result, 0)
                self.assertEqual(b % result, 0)
                self.assertEqual(result, gcd(b, a))

    def test_type_error_first_argument(self):
        '''TC-DIV-08. Типы: нецелое первое число (float, str, None) дает TypeError с именем number1.'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number1 должен быть целым числом"):
                    gcd(bad, 5)

    def test_type_error_second_argument(self):
        '''TC-DIV-09. Типы: нецелое второе число (float, str, None) дает TypeError с именем number2.'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number2 должен быть целым числом"):
                    gcd(5, bad)

    def test_type_error_bool(self):
        '''TC-DIV-10. Типы: True и False отклоняются с TypeError в любой из двух позиций.'''
        for flag in BOOLEANS:
            with self.subTest(position="first", value=flag):
                with self.assertRaises(TypeError):
                    gcd(flag, 5)
            with self.subTest(position="second", value=flag):
                with self.assertRaises(TypeError):
                    gcd(5, flag)


class LcmTestCase(unittest.TestCase):
    '''Тесты lcm: наименьшее общее кратное двух целых чисел.'''

    def test_positive_numbers(self):
        '''TC-DIV-11. Класс эквивалентности "положительные числа": lcm на типичных парах, включая взаимно простые и кратные.'''
        cases = [(4, 6, 12), (6, 4, 12), (3, 5, 15), (12, 12, 12), (3, 9, 9), (21, 6, 42)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = lcm(a, b)
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_negative_numbers_sign_ignored(self):
        '''TC-DIV-12. Класс эквивалентности "отрицательные числа": знаки не влияют, результат неотрицателен.'''
        cases = [(-4, 6, 12), (4, -6, 12), (-4, -6, 12), (-3, 3, 3)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                result = lcm(a, b)
                self.assertEqual(result, expected)
                self.assertGreaterEqual(result, 0)

    def test_zero_arguments(self):
        '''TC-DIV-13. Граница "ноль": если хотя бы один аргумент равен 0, lcm равен 0, включая lcm(0, 0).'''
        cases = [(5, 0), (0, 5), (-5, 0), (0, -5), (0, 0)]
        for a, b in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(lcm(a, b), 0)

    def test_unit_and_small_boundaries(self):
        '''TC-DIV-14. Граничные значения 1, -1 и 2: lcm с единицей равен модулю другого числа.'''
        cases = [(1, 1, 1), (1, 99, 99), (-1, 99, 99), (99, -1, 99), (2, 2, 2), (2, 3, 6), (2, 4, 4)]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(lcm(a, b), expected)

    def test_large_numbers(self):
        '''TC-DIV-15. Большие числа: lcm соседних чисел равен произведению, lcm степеней разных простых тоже.'''
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
        '''TC-DIV-16. Оракул: lcm совпадает с math.lcm на всех парах от -30 до 30 (math.lcm есть с Python 3.9).'''
        values = range(-30, 31)
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    self.assertEqual(lcm(a, b), math.lcm(a, b))

    def test_gcd_lcm_product_identity_and_multiple(self):
        '''TC-DIV-17. Свойства: gcd(a, b) * lcm(a, b) равно |a * b|, а lcm кратно обоим аргументам.'''
        pairs = [(4, 6), (-4, 6), (17, 5), (48, 18), (91, 143), (10**6, 10**6 + 1)]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                multiple = lcm(a, b)
                self.assertEqual(gcd(a, b) * multiple, abs(a * b))
                self.assertEqual(multiple % a, 0)
                self.assertEqual(multiple % b, 0)

    def test_type_error_first_argument(self):
        '''TC-DIV-18. Типы: нецелое первое число (float, str, None) дает TypeError с именем number1.'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number1 должен быть целым числом"):
                    lcm(bad, 5)

    def test_type_error_second_argument(self):
        '''TC-DIV-19. Типы: нецелое второе число (float, str, None) дает TypeError с именем number2.'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number2 должен быть целым числом"):
                    lcm(5, bad)

    def test_type_error_bool(self):
        '''TC-DIV-20. Типы: True и False отклоняются с TypeError в любой из двух позиций.'''
        for flag in BOOLEANS:
            with self.subTest(position="first", value=flag):
                with self.assertRaises(TypeError):
                    lcm(flag, 5)
            with self.subTest(position="second", value=flag):
                with self.assertRaises(TypeError):
                    lcm(5, flag)


class DivisorsTestCase(unittest.TestCase):
    '''Тесты divisors: список натуральных делителей по возрастанию.'''

    def test_positive_numbers(self):
        '''TC-DIV-21. Класс эквивалентности "положительные числа": полный список делителей, в том числе полного квадрата.'''
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
        '''TC-DIV-22. Класс эквивалентности "отрицательные числа": делители -n совпадают с делителями n, все натуральные.'''
        for number in (-6, -36, -13, -100):
            with self.subTest(number=number):
                result = divisors(number)
                self.assertEqual(result, divisors(-number))
                self.assertTrue(all(d > 0 for d in result))
        self.assertEqual(divisors(-6), [1, 2, 3, 6])

    def test_boundaries_one_two_and_primes(self):
        '''TC-DIV-23. Граничные значения 1, -1, 2 и простые числа: у простого p ровно два делителя, 1 и p.'''
        self.assertEqual(divisors(1), [1])
        self.assertEqual(divisors(-1), [1])
        self.assertEqual(divisors(2), [1, 2])
        for p in SMALL_PRIMES + (10**9 + 7,):
            with self.subTest(prime=p):
                self.assertEqual(divisors(p), [1, p])

    def test_prime_powers(self):
        '''TC-DIV-24. Степени простых: делители p**k это 1, p, ..., p**k, их ровно k + 1.'''
        for p, k in [(2, 10), (3, 5), (7, 4), (2, 1)]:
            with self.subTest(p=p, k=k):
                self.assertEqual(divisors(p**k), [p**i for i in range(k + 1)])

    def test_zero_raises_value_error(self):
        '''TC-DIV-25. Негативный: divisors(0) выбрасывает ValueError с пояснением, что у нуля бесконечно много делителей.'''
        with self.assertRaisesRegex(ValueError, "бесконечно много"):
            divisors(0)

    def test_matches_brute_force_oracle(self):
        '''TC-DIV-26. Оракул: для n от 1 до 200 список совпадает с перебором, отсортирован, каждый элемент делит n.'''
        for n in range(1, 201):
            with self.subTest(n=n):
                result = divisors(n)
                expected = [d for d in range(1, n + 1) if n % d == 0]
                self.assertEqual(result, expected)
                self.assertEqual(result, sorted(result))
                self.assertTrue(all(n % d == 0 for d in result))

    def test_large_number(self):
        '''TC-DIV-27. Большое число 10**12 = 2**12 * 5**12: ровно 169 делителей, они отсортированы, без повторов, первый 1, последний 10**12.'''
        number = 10**12
        result = divisors(number)
        self.assertEqual(len(result), 13 * 13)
        self.assertEqual(result, sorted(set(result)))
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], number)
        self.assertTrue(all(number % d == 0 for d in result))

    def test_type_error(self):
        '''TC-DIV-28. Типы: float, str, None, True и False дают TypeError с именем number.'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    divisors(bad)


class IsPerfectTestCase(unittest.TestCase):
    '''Тесты is_perfect: проверка числа на совершенность.'''

    def test_known_perfect_numbers(self):
        '''TC-DIV-29. Известные совершенные числа 6, 28, 496, 8128 и 33550336 дают True.'''
        for number in (6, 28, 496, 8128, 33550336):
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), True)

    def test_neighbours_and_other_numbers_are_not_perfect(self):
        '''TC-DIV-30. Соседи совершенных чисел и простые, избыточные, недостаточные числа дают False.'''
        not_perfect = [5, 7, 27, 29, 495, 497, 8127, 8129]  # соседи
        not_perfect += [2, 3, 13, 97]                        # простые
        not_perfect += [12, 18, 20, 24]                      # избыточные: сумма делителей больше числа
        not_perfect += [4, 8, 9, 100]                        # недостаточные составные
        for number in not_perfect:
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), False)

    def test_zero_one_and_negative_are_not_perfect(self):
        '''TC-DIV-31. Граница и класс "не больше 1": 0, 1 и отрицательные числа, включая -6 и -28, дают False.'''
        for number in (0, 1, -1, -6, -28, -496):
            with self.subTest(number=number):
                self.assertIs(is_perfect(number), False)

    def test_only_known_perfect_numbers_below_10000(self):
        '''TC-DIV-32. Оракул: среди чисел от -10 до 10000 совершенными оказываются только 6, 28, 496 и 8128.'''
        found = [n for n in range(-10, 10001) if is_perfect(n)]
        self.assertEqual(found, [6, 28, 496, 8128])

    def test_matches_sum_of_proper_divisors_definition(self):
        '''TC-DIV-33. Оракул по определению: для n от 2 до 300 результат равен проверке "сумма делителей меньше n равна n" перебором.'''
        for n in range(2, 301):
            with self.subTest(n=n):
                expected = sum(d for d in range(1, n) if n % d == 0) == n
                self.assertEqual(is_perfect(n), expected)

    def test_large_number(self):
        '''TC-DIV-34. Большое число 10**12 не совершенное, функция возвращает False за разумное время.'''
        self.assertIs(is_perfect(10**12), False)

    def test_type_error(self):
        '''TC-DIV-35. Типы: float, str, None, True и False дают TypeError с именем number.'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    is_perfect(bad)


class EulerPhiTestCase(unittest.TestCase):
    '''Тесты euler_phi: функция Эйлера.'''

    def test_known_values(self):
        '''TC-DIV-36. Известные значения функции Эйлера, в том числе phi(1) = 1 и значения из документации.'''
        cases = [(1, 1), (2, 1), (3, 2), (4, 2), (6, 2), (9, 6), (10, 4), (12, 4), (13, 12), (36, 12), (100, 40)]
        for number, expected in cases:
            with self.subTest(number=number):
                result = euler_phi(number)
                self.assertIsInstance(result, int)
                self.assertEqual(result, expected)

    def test_matches_coprime_count_oracle(self):
        '''TC-DIV-37. Оракул: для n от 1 до 200 phi(n) равно числу k от 1 до n, взаимно простых с n по math.gcd.'''
        for n in range(1, 201):
            with self.subTest(n=n):
                expected = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
                self.assertEqual(euler_phi(n), expected)

    def test_prime_gives_p_minus_one(self):
        '''TC-DIV-38. Свойство: для простого p значение phi(p) равно p - 1, включая большое простое 10**9 + 7.'''
        for p in SMALL_PRIMES + (10**9 + 7,):
            with self.subTest(prime=p):
                self.assertEqual(euler_phi(p), p - 1)

    def test_prime_power(self):
        '''TC-DIV-39. Свойство: phi(p**k) равно p**(k - 1) * (p - 1) для малых простых и k от 1 до 6.'''
        for p in (2, 3, 5, 7):
            for k in range(1, 7):
                with self.subTest(p=p, k=k):
                    self.assertEqual(euler_phi(p**k), p ** (k - 1) * (p - 1))

    def test_multiplicative_for_coprime_arguments(self):
        '''TC-DIV-40. Свойство: phi(a * b) равно phi(a) * phi(b) для всех взаимно простых a и b от 1 до 40.'''
        for a in range(1, 41):
            for b in range(1, 41):
                if math.gcd(a, b) != 1:
                    continue
                with self.subTest(a=a, b=b):
                    self.assertEqual(euler_phi(a * b), euler_phi(a) * euler_phi(b))

    def test_large_numbers(self):
        '''TC-DIV-41. Большие числа: phi(10**12) = 4 * 10**11, phi(p * q) = (p - 1) * (q - 1) для простых 10007 и 10009.'''
        self.assertEqual(euler_phi(10**12), 4 * 10**11)
        self.assertEqual(euler_phi(10007 * 10009), 10006 * 10008)

    def test_zero_and_negative_raise_value_error(self):
        '''TC-DIV-42. Негативный: 0 и отрицательные числа дают ValueError с пояснением про натуральные числа.'''
        for number in (0, -1, -36, -(10**12)):
            with self.subTest(number=number):
                with self.assertRaisesRegex(ValueError, "натуральных"):
                    euler_phi(number)

    def test_type_error(self):
        '''TC-DIV-43. Типы: float, str, None, True и False дают TypeError с именем number.'''
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
                    euler_phi(bad)

    def test_integration_with_factorize_formula(self):
        '''TC-DIV-44. Интеграционный (euler_phi + primes.factorize): phi(n) совпадает с формулой n * произведение (1 - 1/p) по различным простым из настоящего factorize, n от 2 до 200.'''
        from numtheory.primes import factorize
        for n in range(2, 201):
            with self.subTest(n=n):
                expected = Fraction(n)
                for p in set(factorize(n)):
                    expected *= Fraction(p - 1, p)
                self.assertEqual(euler_phi(n), expected)

    def test_isolated_with_stubbed_factorize(self):
        '''TC-DIV-45. Модульный в изоляции: factorize подменен заглушкой с ответом [2, 2, 3, 3], проверяется, что euler_phi вызывает его один раз с аргументом 36 и учитывает каждое простое один раз.'''
        with mock.patch("numtheory.divisors.factorize", return_value=[2, 2, 3, 3]) as fake:
            result = euler_phi(36)
        fake.assert_called_once_with(36)
        self.assertEqual(result, 12)


if __name__ == "__main__":
    unittest.main()

import re
import unittest

from numtheory._validation import check_int, check_int_list, ints_only


class CheckIntTestCase(unittest.TestCase):
    def test_integers_pass(self):
        '''TC-VAL-01. check_int: целые числа проходят'''
        self.assertIsNone(check_int(0, "x"))
        self.assertIsNone(check_int(5, "x"))
        self.assertIsNone(check_int(-3, "x"))
        self.assertIsNone(check_int(10**20, "x"))

    def test_not_integers(self):
        '''TC-VAL-02. check_int: TypeError на float, str и None'''
        with self.assertRaisesRegex(TypeError, "x должен быть целым числом"):
            check_int(2.5, "x")
        with self.assertRaisesRegex(TypeError, "x должен быть целым числом"):
            check_int("7", "x")
        with self.assertRaisesRegex(TypeError, "x должен быть целым числом"):
            check_int(None, "x")

    def test_booleans(self):
        '''TC-VAL-03. check_int: TypeError на True и False'''
        with self.assertRaisesRegex(TypeError, "x должен быть целым числом"):
            check_int(True, "x")
        with self.assertRaisesRegex(TypeError, "x должен быть целым числом"):
            check_int(False, "x")


class CheckIntListTestCase(unittest.TestCase):
    def test_list_and_tuple_pass(self):
        '''TC-VAL-04. check_int_list: список и кортеж целых проходят'''
        self.assertIsNone(check_int_list([1, 2, 3], "x"))
        self.assertIsNone(check_int_list((4, -5), "x"))
        self.assertIsNone(check_int_list([], "x"))

    def test_not_a_list(self):
        '''TC-VAL-05. check_int_list: TypeError, если аргумент не список'''
        for value in (5, "12", None, 2.5):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, "x должен быть списком или кортежем"):
                    check_int_list(value, "x")

    def test_bad_item_index(self):
        '''TC-VAL-06. check_int_list: плохой элемент, индекс в ошибке'''
        with self.assertRaisesRegex(TypeError, r"x\[1\] должен быть целым числом"):
            check_int_list([1, "2", 3], "x")
        with self.assertRaisesRegex(TypeError, r"x\[0\] должен быть целым числом"):
            check_int_list([2.5, 1], "x")
        with self.assertRaisesRegex(TypeError, r"x\[2\] должен быть целым числом"):
            check_int_list((1, 2, True), "x")


class IntsOnlyTestCase(unittest.TestCase):
    def test_checks_arguments(self):
        '''TC-VAL-07. ints_only: проверяет аргументы int и list[int]'''
        @ints_only
        def total(number: int, items: list[int]) -> int:
            return number + sum(items)

        self.assertEqual(total(1, [2, 3]), 6)
        self.assertEqual(total(10, []), 10)
        with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
            total(2.5, [1])
        with self.assertRaisesRegex(TypeError, "number должен быть целым числом"):
            total(True, [1])
        with self.assertRaisesRegex(TypeError, r"items\[1\] должен быть целым числом"):
            total(1, [1, "2"])
        with self.assertRaisesRegex(TypeError, "items должен быть списком"):
            total(1, 5)

    def test_keeps_name_and_docstring(self):
        '''TC-VAL-08. ints_only: сохраняет имя и docstring функции'''
        @ints_only
        def double(number: int) -> int:
            '''Удваивает число.'''
            return number * 2

        self.assertEqual(double.__name__, "double")
        self.assertEqual(double.__doc__, "Удваивает число.")
        self.assertEqual(double(4), 8)


def load_tests(loader, standard_tests, pattern):
    '''Расставляет тесты по номеру кейса TC-VAL-NN из docstring.'''
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item

    def case_number(test):
        found = re.match(r"TC-VAL-(\d+)\.", test.shortDescription() or "")
        if found is None:
            raise ValueError("у теста %s нет номера TC-VAL-NN в docstring" % test.id())
        return int(found.group(1))

    return unittest.TestSuite(sorted(flatten(standard_tests), key=case_number))


if __name__ == "__main__":
    unittest.main()

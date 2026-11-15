import inspect
import re
import unittest

from numtheory._validation import check_int, check_int_list, ints_only
from numtheory.divisors import gcd
from numtheory.modular import crt

NOT_INTEGERS = (2.5, 3.0, "7", None, 1 + 2j, [1], (1,), {1}, b"1")
BOOLEANS = (True, False)


class MyInt(int):
    pass


class CheckIntTestCase(unittest.TestCase):
    def test_integers_pass(self):
        '''TC-VAL-01. check_int: нуль, положительные, отрицательные, большие'''
        for value in (0, 1, -1, 42, -42, 2**64, -(2**64), 10**30, -(10**30)):
            with self.subTest(value=value):
                self.assertIsNone(check_int(value, "x"))

    def test_int_subclass_passes(self):
        '''TC-VAL-02. check_int: подкласс int, не bool, считается целым'''
        self.assertIsNone(check_int(MyInt(5), "x"))

    def test_bool_rejected(self):
        '''TC-VAL-03. check_int: TypeError на True и False'''
        for flag in BOOLEANS:
            with self.subTest(value=flag):
                with self.assertRaisesRegex(TypeError, "x должен быть целым числом, получено bool"):
                    check_int(flag, "x")

    def test_non_integers_rejected(self):
        '''TC-VAL-04. check_int: TypeError на float, str, None, complex, список'''
        for bad in NOT_INTEGERS:
            with self.subTest(value=bad):
                with self.assertRaises(TypeError):
                    check_int(bad, "x")

    def test_error_message_has_name_and_type(self):
        '''TC-VAL-05. check_int: текст ошибки с именем и типом'''
        cases = [
            (True, "flag", "bool"),
            (2.5, "ratio", "float"),
            ("7", "text", "str"),
            (None, "nothing", "NoneType"),
            (1 + 2j, "z", "complex"),
            ([1], "items", "list"),
        ]
        for bad, name, type_name in cases:
            with self.subTest(name=name):
                with self.assertRaises(TypeError) as context:
                    check_int(bad, name)
                expected = "%s должен быть целым числом, получено %s" % (name, type_name)
                self.assertEqual(str(context.exception), expected)


class CheckIntListTestCase(unittest.TestCase):
    def test_lists_and_tuples_of_integers_pass(self):
        '''TC-VAL-06. check_int_list: список, кортеж и пустые контейнеры'''
        cases = [[1, 2, 3], (1, 2, 3), [0], [-5, 0, 5, 10**20], (7,), [], ()]
        for value in cases:
            with self.subTest(value=value):
                self.assertIsNone(check_int_list(value, "xs"))

    def test_non_sequence_rejected(self):
        '''TC-VAL-07. check_int_list: TypeError на int, str, set, None'''
        for bad, type_name in [(5, "int"), ("123", "str"), ({1, 2}, "set"), (None, "NoneType"), (2.5, "float")]:
            with self.subTest(value=bad):
                with self.assertRaises(TypeError) as context:
                    check_int_list(bad, "xs")
                expected = "xs должен быть списком или кортежем целых чисел, получено %s" % type_name
                self.assertEqual(str(context.exception), expected)

    def test_bad_element_reported_with_index(self):
        '''TC-VAL-08. check_int_list: плохой элемент, индекс в имени'''
        cases = [
            ([1, 2.5], "remainders", "remainders[1] должен быть целым числом, получено float"),
            ([True, 1], "xs", "xs[0] должен быть целым числом, получено bool"),
            ([1, 2, False], "xs", "xs[2] должен быть целым числом, получено bool"),
            ((1, None), "moduli", "moduli[1] должен быть целым числом, получено NoneType"),
            (["7"], "xs", "xs[0] должен быть целым числом, получено str"),
            ([[1]], "xs", "xs[0] должен быть целым числом, получено list"),
        ]
        for value, name, expected in cases:
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as context:
                    check_int_list(value, name)
                self.assertEqual(str(context.exception), expected)

    def test_first_bad_element_reported(self):
        '''TC-VAL-09. check_int_list: при нескольких ошибках первый индекс'''
        with self.assertRaisesRegex(TypeError, re.escape("xs[1]")):
            check_int_list([1, 2.5, "x", None], "xs")


class IntsOnlyTestCase(unittest.TestCase):
    def test_int_argument_checked_positionally(self):
        '''TC-VAL-10. ints_only: аргумент int проверяется позиционно'''
        @ints_only
        def add(a: int, b: int):
            return a + b

        self.assertEqual(add(2, 3), 5)
        for bad in NOT_INTEGERS + BOOLEANS:
            with self.subTest(position="first", value=bad):
                with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
                    add(bad, 3)
            with self.subTest(position="second", value=bad):
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    add(2, bad)

    def test_int_argument_checked_by_keyword(self):
        '''TC-VAL-11. ints_only: аргумент int проверяется по ключу'''
        @ints_only
        def add(a: int, b: int, *, scale: int = 1):
            return (a + b) * scale

        self.assertEqual(add(a=2, b=3), 5)
        self.assertEqual(add(2, b=3, scale=2), 10)
        for bad in (2.5, "7", None, True):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    add(2, b=bad)
                with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
                    add(a=bad, b=3)
                with self.assertRaisesRegex(TypeError, "scale должен быть целым числом"):
                    add(2, 3, scale=bad)

    def test_list_of_int_checked_elementwise(self):
        '''TC-VAL-12. ints_only: list[int] проверяется поэлементно'''
        @ints_only
        def total(xs: list[int]):
            return sum(xs)

        for good in ([1, 2, 3], (1, 2, 3), []):
            with self.subTest(value=good):
                self.assertEqual(total(good), 6 if good else 0)
        with self.assertRaisesRegex(TypeError, re.escape("xs[1] должен быть целым числом, получено float")):
            total([1, 2.5, 3])
        with self.assertRaisesRegex(TypeError, re.escape("xs[0] должен быть целым числом, получено bool")):
            total([True, 2])
        for bad in (5, "123", {1, 2}, None):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "xs должен быть списком или кортежем"):
                    total(bad)

    def test_other_annotations_not_checked(self):
        '''TC-VAL-13. ints_only: другие аннотации не проверяются'''
        @ints_only
        def echo(a: str, b: float, c: list[str], d: tuple[int, ...], e: object):
            return (a, b, c, d, e)

        result = echo(5, "x", [1, 2], ("a",), None)
        self.assertEqual(result, (5, "x", [1, 2], ("a",), None))

    def test_unannotated_arguments_not_checked(self):
        '''TC-VAL-14. ints_only: аргументы без аннотации не проверяются'''
        @ints_only
        def echo(a, b):
            return (a, b)

        self.assertEqual(echo("x", None), ("x", None))
        self.assertEqual(echo(a=2.5, b=True), (2.5, True))

    def test_default_values_not_checked(self):
        '''TC-VAL-15. ints_only: значения по умолчанию не проверяются'''
        @ints_only
        def pick(a: int, b: int = None, xs: list[int] = "default"):
            return (a, b, xs)

        self.assertEqual(pick(1), (1, None, "default"))
        self.assertEqual(pick(1, 2), (1, 2, "default"))

    def test_explicit_value_for_defaulted_argument_checked(self):
        '''TC-VAL-16. ints_only: явное значение вместо умолчания проверяется'''
        @ints_only
        def pick(a: int, b: int = 0):
            return (a, b)

        for bad in (2.5, "7", None, True):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    pick(1, bad)
                with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
                    pick(1, b=bad)

    def test_signature_mismatch_gives_native_type_error(self):
        '''TC-VAL-17. ints_only: несовпадение с сигнатурой, родной TypeError'''
        calls = []

        @ints_only
        def add(a: int, b: int):
            calls.append((a, b))
            return a + b

        cases = [
            ((1,), {}),
            (("x",), {}),
            ((), {}),
            ((1, 2, 3), {}),
            ((1, 2), {"c": 3}),
            ((1,), {"b": 2, "c": 3}),
            ((1, 2), {"a": 3}),
            (("x", 2), {"a": 3}),
        ]
        for args, kwargs in cases:
            with self.subTest(args=args, kwargs=kwargs):
                with self.assertRaises(TypeError) as context:
                    add(*args, **kwargs)
                self.assertNotIn("должен быть целым числом", str(context.exception))
        self.assertEqual(calls, [])

    def test_var_positional_and_var_keyword_skipped(self):
        '''TC-VAL-18. ints_only: *args и **kwargs пропускаются'''
        @ints_only
        def gather(a: int, *args: int, **kwargs: int):
            return (a, args, kwargs)

        self.assertEqual(gather(1, "x", 2.5, key="y"), (1, ("x", 2.5), {"key": "y"}))
        self.assertEqual(gather(1), (1, (), {}))
        with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
            gather("x", 2, key=3)

    def test_preserves_name_and_docstring(self):
        '''TC-VAL-19. ints_only: сохраняет __name__ и __doc__'''
        def original(a: int):
            '''Описание исходной функции.'''
            return a

        wrapped = ints_only(original)
        self.assertEqual(wrapped.__name__, "original")
        self.assertEqual(wrapped.__doc__, "Описание исходной функции.")

    def test_preserves_signature(self):
        '''TC-VAL-20. ints_only: сохраняет сигнатуру для inspect'''
        def original(a: int, xs: list[int], b: int = 3, *args, key: int = 0, **kwargs) -> int:
            return a

        wrapped = ints_only(original)
        self.assertEqual(inspect.signature(wrapped), inspect.signature(original))
        self.assertEqual(list(inspect.signature(wrapped).parameters), ["a", "xs", "b", "args", "key", "kwargs"])

    def test_returns_result_and_passes_arguments_unchanged(self):
        '''TC-VAL-21. ints_only: результат и аргументы передаются как есть'''
        sentinel = object()
        produced = [1, 2]
        received = []

        @ints_only
        def func(a: int, xs: list[int], *, k: int = 0):
            received.append((a, xs, k))
            return sentinel

        @ints_only
        def make_list(a: int):
            return produced

        @ints_only
        def nothing(a: int):
            return None

        data = [4, 5]
        self.assertIs(func(1, data, k=2), sentinel)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0][0], 1)
        self.assertIs(received[0][1], data)
        self.assertEqual(received[0][2], 2)
        self.assertIs(make_list(1), produced)
        self.assertIsNone(nothing(1))

    def test_checks_follow_parameter_order(self):
        '''TC-VAL-22. ints_only: первым сообщается первый неверный параметр'''
        @ints_only
        def func(a: int, b: int, c: int):
            return a + b + c

        with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
            func("x", 2.5, None)
        with self.assertRaisesRegex(TypeError, "b должен быть целым числом"):
            func(1, 2.5, None)
        with self.assertRaisesRegex(TypeError, "c должен быть целым числом"):
            func(1, 2, None)
        with self.assertRaisesRegex(TypeError, "a должен быть целым числом"):
            func(c=None, b=2.5, a="x")

    def test_function_not_called_on_bad_argument(self):
        '''TC-VAL-23. ints_only: функция не вызывается при неверном аргументе'''
        calls = []

        @ints_only
        def func(a: int, xs: list[int]):
            calls.append((a, xs))
            return a

        bad_calls = [
            ("x", [1]),
            (True, [1]),
            (1, [1, 2.5]),
            (1, "123"),
            (1, None),
        ]
        for args in bad_calls:
            with self.subTest(args=args):
                with self.assertRaises(TypeError):
                    func(*args)
        self.assertEqual(calls, [])
        func(1, [1])
        self.assertEqual(len(calls), 1)

    def test_integration_gcd_is_protected(self):
        '''TC-VAL-24. ints_only: интеграция, gcd защищена декоратором'''
        for bad in (2.5, "7", None, True):
            with self.subTest(value=bad):
                with self.assertRaisesRegex(TypeError, "number1 должен быть целым числом"):
                    gcd(bad, 5)
                with self.assertRaisesRegex(TypeError, "number2 должен быть целым числом"):
                    gcd(5, bad)
        self.assertEqual(gcd(48, 18), 6)

    def test_integration_crt_list_is_protected(self):
        '''TC-VAL-25. ints_only: интеграция, crt защищена, list[int]'''
        with self.assertRaisesRegex(TypeError, re.escape("remainders[1] должен быть целым числом")):
            crt([2, 3.5], [3, 5])
        with self.assertRaisesRegex(TypeError, re.escape("moduli[0] должен быть целым числом")):
            crt([2, 3], [True, 5])
        with self.assertRaisesRegex(TypeError, "remainders должен быть списком или кортежем"):
            crt("23", [3, 5])
        self.assertEqual(crt([2, 3], [3, 5]), (8, 15))


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

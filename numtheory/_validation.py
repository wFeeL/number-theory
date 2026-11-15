import functools
import inspect
from typing import get_args, get_origin


def check_int(value: object, name: str) -> None:
    '''
    Проверяет, что аргумент функции является целым числом, и выбрасывает TypeError, если это не так.
    Значения True и False отклоняются: в Python bool наследуется от int, но числом по смыслу не является.
    Это помощник для ints_only, из функций библиотеки его напрямую не вызывают.

        Параметры:
            value (object): проверяемое значение
            name (str): имя аргумента для текста ошибки

        Возвращаемое значение:
            None (NoneType): функция ничего не возвращает
    '''
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} должен быть целым числом, получено {type(value).__name__}")


def check_int_list(value: object, name: str) -> None:
    '''
    Проверяет, что аргумент функции является списком или кортежем целых чисел, и выбрасывает
    TypeError, если это не так. Элементы проверяются по одному через check_int, в тексте ошибки
    для элемента имя дополняется его номером, например remainders[1]. Пустой список допустим.
    Это помощник для ints_only, из функций библиотеки его напрямую не вызывают.

        Параметры:
            value (object): проверяемое значение
            name (str): имя аргумента для текста ошибки

        Возвращаемое значение:
            None (NoneType): функция ничего не возвращает
    '''
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} должен быть списком или кортежем целых чисел, получено {type(value).__name__}")
    for index, item in enumerate(value):
        check_int(item, f"{name}[{index}]")


def ints_only(func):
    '''
    Декоратор: проверяет аргументы функции по её аннотациям, чтобы тип не приходилось записывать дважды.
    Аргумент с аннотацией int проверяется через check_int, аргумент с аннотацией list[int] через
    check_int_list. Аргументы с другими аннотациями и без аннотации не проверяются. Проверка идёт
    в порядке параметров функции и выбрасывает TypeError с тем же текстом, что и ручной вызов
    check_int. Если вызов не подходит под сигнатуру (не хватает аргументов, лишний аргумент),
    ошибку выбрасывает сам Python. Имя, docstring и сигнатура функции сохраняются.
    Аннотации должны быть настоящими объектами, а не строками, поэтому в модулях с декоратором
    нельзя писать from __future__ import annotations. Для работы на Python 3.9 список
    распознаётся через typing.get_origin и typing.get_args.

        Параметры:
            func (Callable): декорируемая функция

        Возвращаемое значение:
            wrapper (Callable): функция с тем же именем и docstring, проверяющая аргументы перед вызовом
    '''
    signature = inspect.signature(func)
    checks = {}
    for name, parameter in signature.parameters.items():
        if parameter.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if parameter.annotation is int:
            checks[name] = check_int
        elif get_origin(parameter.annotation) is list and get_args(parameter.annotation) == (int,):
            checks[name] = check_int_list

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            bound = signature.bind(*args, **kwargs)
        except TypeError:
            return func(*args, **kwargs)
        for name, check in checks.items():
            if name in bound.arguments:
                check(bound.arguments[name], name)
        return func(*args, **kwargs)

    return wrapper

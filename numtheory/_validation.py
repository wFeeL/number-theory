def check_int(value: object, name: str) -> None:
    '''
    Проверяет, что аргумент функции является целым числом, и выбрасывает TypeError, если это не так.
    Значения True и False отклоняются: в Python bool наследуется от int, но числом по смыслу не является.

        Параметры:
            value (object): проверяемое значение
            name (str): имя аргумента для текста ошибки

        Возвращаемое значение:
            None (NoneType): функция ничего не возвращает
    '''
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} должен быть целым числом, получено {type(value).__name__}")

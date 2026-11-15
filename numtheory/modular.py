from numtheory._validation import ints_only


@ints_only
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    '''
    Расширенный алгоритм Евклида: находит НОД и коэффициенты Безу.
    Возвращает такие числа g, x, y, что a * x + b * y = g, где g равен наибольшему общему
    делителю a и b и всегда неотрицателен. Знаки аргументов не влияют на g. Если один аргумент
    равен 0, коэффициент при этом нулевом аргументе равен 0, а при другом равен ±1:
    extended_gcd(a, 0) возвращает (|a|, ±1, 0), а extended_gcd(0, b) возвращает (|b|, 0, ±1).
    Для пары (0, 0) возвращается (0, 0, 0): равенство 0 * 0 + 0 * 0 = 0 выполняется.
    Для нецелого аргумента выбрасывает TypeError.

        Параметры:
            a (int): первое целое число
            b (int): второе целое число

        Возвращаемое значение:
            result (tuple[int, int, int]): тройка (g, x, y), где g = НОД(a, b) и a * x + b * y = g
    '''
    if a == 0 and b == 0:
        return 0, 0, 0

    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    if old_r < 0:
        return -old_r, -old_x, -old_y
    return old_r, old_x, old_y

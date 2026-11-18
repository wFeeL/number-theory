# number-theory

Небольшая библиотека на Python для теории чисел. Функции разделены на четыре модуля: `primes` (простые числа и разложение на множители), `divisors` (НОД, НОК, делители и функция Эйлера), `modular` (расширенный алгоритм Евклида, обратные числа по модулю, линейные диофантовы уравнения и китайская теорема об остатках) и `sequences` (числа Фибоначчи и факториал).

Проект используется в лабораторных работах по курсу «Инструментальные средства разработки ПО».

## Установка

Устанавливать ничего не нужно, достаточно Python 3.9 или новее. Склонируйте репозиторий и перейдите в него:

```bash
git clone https://github.com/wFeeL/number-theory.git
cd number-theory
```

## Пример использования

Сохраните код в файл `example.py` в корне репозитория:

```python
from numtheory.primes import factorize
from numtheory.divisors import gcd, euler_phi
from numtheory.modular import mod_inverse, crt
from numtheory.sequences import fibonacci_list

print(factorize(360))       # [2, 2, 2, 3, 3, 5]
print(gcd(84, 36))          # 12
print(euler_phi(36))        # 12
print(mod_inverse(3, 7))    # 5
print(crt([2, 3], [3, 5]))  # (8, 15)
print(fibonacci_list(8))    # [0, 1, 1, 2, 3, 5, 8, 13]
```

и запустите его:

```bash
python3 example.py
```

Если запустить файл из другой папки, Python не найдёт пакет `numtheory` и выдаст `ModuleNotFoundError`.

## Тесты

Тесты лежат в папке `tests/` и написаны на стандартном `unittest`, сторонние пакеты не нужны. Запускайте их из корня репозитория:

```bash
python3 -m unittest -v
```

На Windows команда такая: `python -m unittest -v`. У каждого теста в docstring есть номер кейса вида `TC-DIV-01`, он виден в выводе с флагом `-v`.

Тесты разложены по файлам, по одному на модуль, плюс отдельный файл на проверку аргументов:

| Файл | Префикс кейсов |
|---|---|
| `tests/test_divisors.py` | `TC-DIV` |
| `tests/test_primes.py` | `TC-PRI` |
| `tests/test_sequences.py` | `TC-SEQ` |
| `tests/test_modular.py` | `TC-MOD` |
| `tests/test_validation.py` | `TC-VAL` |

Команда запуска общая для всех файлов. Нужен Python 3.9 или новее, как и для самой библиотеки.

## Документация

- [Общее описание решения](docs/overview.md)
- [Описание функций с примерами](docs/functions.md)
- [История изменений](docs/changelog.md)

## Автор

[wFeeL](https://github.com/wFeeL)

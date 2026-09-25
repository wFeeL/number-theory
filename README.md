# number-theory

Небольшая библиотека на Python для теории чисел. Функции разделены на три модуля: `primes` (простые числа и разложение на множители), `divisors` (НОД, НОК и делители) и `sequences` (числа Фибоначчи и факториал).

Проект сделан для лабораторной работы №2 «Документирование» по курсу «Инструментальные средства разработки ПО».

## Установка

Устанавливать ничего не нужно, достаточно Python 3.9 или новее. Склонируйте репозиторий и запускайте Python из его корня:

```bash
git clone https://github.com/wFeeL/number-theory.git
cd number-theory
```

## Пример использования

```python
from numtheory.primes import factorize
from numtheory.divisors import gcd
from numtheory.sequences import fibonacci_list

print(factorize(360))      # [2, 2, 2, 3, 3, 5]
print(gcd(84, 36))         # 12
print(fibonacci_list(8))   # [0, 1, 1, 2, 3, 5, 8, 13]
```

## Документация

- [Общее описание решения](docs/overview.md)
- [Описание функций с примерами](docs/functions.md)
- [История изменений](docs/changelog.md)

## Автор

[wFeeL](https://github.com/wFeeL)

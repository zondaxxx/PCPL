"""Ленивый генератор случайных целых с включёнными границами."""

import random


def gen_random(num_count, begin, end):
    if num_count < 0:
        raise ValueError("Количество не может быть отрицательным")
    if begin > end:
        raise ValueError("Минимум не может превышать максимум")
    for _ in range(num_count):
        yield random.randint(begin, end)


if __name__ == "__main__":
    random.seed(35)
    print(list(gen_random(5, 1, 3)))

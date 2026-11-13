"""Общий ввод, вывод и преобразование t = x² обратно к x."""

from decimal import Decimal, localcontext
import math
import sys


PRECISION = 50


def coefficient(value):
    """Проверить конечное вещественное число и сохранить его десятичную запись."""
    try:
        number = float(value)
        if not math.isfinite(number):
            raise ValueError
        return Decimal(str(number))
    except (ValueError, TypeError, OverflowError):
        raise ValueError("нужно конечное вещественное число") from None


def read_coefficients(argv=None, input_fn=None, output_fn=None):
    """Ошибочный или отсутствующий аргумент заменяется интерактивным вводом."""
    args = list(sys.argv[1:] if argv is None else argv)
    input_fn = input if input_fn is None else input_fn
    output_fn = print if output_fn is None else output_fn
    if len(args) > 3:
        raise ValueError("ожидается не более трёх коэффициентов A B C")
    result = []
    for index, name in enumerate(("A", "B", "C")):
        value = args[index] if index < len(args) else None
        while True:
            if value is None:
                value = input_fn(f"Введите {name}: ")
            try:
                result.append(coefficient(value))
                break
            except ValueError as error:
                output_fn(f"Ошибка в {name}: {error}. Повторите ввод.")
                value = None
    return tuple(result)


def roots_from_squares(values):
    """Отрицательные t отбрасываются; повторные корни и -0 удаляются."""
    roots = set()
    for value in values:
        if value > 0:
            root = value.sqrt()
            roots.update((-root, root))
        elif value == 0:
            roots.add(Decimal(0))
    return tuple(sorted(roots))


def format_number(value):
    return "0" if value == 0 else format(value.normalize(), ".12g")


def run(solver, argv=None):
    try:
        a, b, c = read_coefficients(argv)
        with localcontext() as context:
            context.prec = PRECISION
            discriminant = b * b - 4 * a * c
            roots = solver(a, b, c)
            print(f"Дискриминант: {format_number(discriminant)}")
            if roots is None:
                print("Любое действительное число является корнем.")
            elif roots:
                print("Действительные корни: " + ", ".join(map(format_number, roots)))
            else:
                print("Действительных корней нет.")
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Ошибка: {error}.", file=sys.stderr)
        return 2

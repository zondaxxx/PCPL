"""Биквадратное уравнение: процедурный подход."""

from decimal import localcontext
from common import PRECISION, coefficient, roots_from_squares, run


def solve(a, b, c):
    a, b, c = map(coefficient, (a, b, c))
    with localcontext() as context:
        context.prec = PRECISION
        if a == 0:
            if b == 0:
                return None if c == 0 else ()
            return roots_from_squares((-c / b,))

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return ()
        if discriminant == 0:
            return roots_from_squares((-b / (2 * a),))

        # Устойчивая форма квадратной формулы уменьшает потерю точности.
        sqrt_d = discriminant.sqrt()
        q = -(b + (sqrt_d if b >= 0 else -sqrt_d)) / 2
        return roots_from_squares((q / a, c / q))


if __name__ == "__main__":
    raise SystemExit(run(solve))

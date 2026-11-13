"""Биквадратное уравнение: чистая функция с сопоставлением с образцом."""

from decimal import localcontext
from common import PRECISION, coefficient, roots_from_squares, run


def solve(a, b, c):
    a, b, c = map(coefficient, (a, b, c))
    with localcontext() as context:
        context.prec = PRECISION
        match (a, b, c):
            case (0, 0, 0):
                return None
            case (0, 0, _):
                return ()
            case (0, _, _):
                return roots_from_squares((-c / b,))
            case _:
                discriminant = b * b - 4 * a * c
                match discriminant:
                    case d if d < 0:
                        return ()
                    case 0:
                        return roots_from_squares((-b / (2 * a),))
                    case d:
                        sqrt_d = d.sqrt()
                        q = -(b + (sqrt_d if b >= 0 else -sqrt_d)) / 2
                        return roots_from_squares((q / a, c / q))


if __name__ == "__main__":
    raise SystemExit(run(solve))

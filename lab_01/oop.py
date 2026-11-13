"""Биквадратное уравнение: объектно-ориентированный подход."""

from decimal import localcontext
from common import PRECISION, coefficient, roots_from_squares, run


class BiquadraticEquation:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = map(coefficient, (a, b, c))

    @property
    def discriminant(self):
        with localcontext() as context:
            context.prec = PRECISION
            return self.b * self.b - 4 * self.a * self.c

    def solve(self):
        with localcontext() as context:
            context.prec = PRECISION
            if self.a == 0:
                if self.b == 0:
                    return None if self.c == 0 else ()
                return roots_from_squares((-self.c / self.b,))

            discriminant = self.discriminant
            if discriminant < 0:
                return ()
            if discriminant == 0:
                return roots_from_squares((-self.b / (2 * self.a),))

            sqrt_d = discriminant.sqrt()
            q = -(self.b + (sqrt_d if self.b >= 0 else -sqrt_d)) / 2
            return roots_from_squares((q / self.a, self.c / q))


def solve(a, b, c):
    return BiquadraticEquation(a, b, c).solve()


if __name__ == "__main__":
    raise SystemExit(run(solve))

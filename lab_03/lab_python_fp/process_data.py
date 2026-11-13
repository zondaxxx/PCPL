"""Обработка списка вакансий цепочкой функциональных преобразований."""

import argparse
import json
from pathlib import Path
import random

if __package__:
    from .cm_timer import cm_timer_1
    from .field import field
    from .gen_random import gen_random
    from .print_result import print_result
    from .unique import Unique
else:
    from cm_timer import cm_timer_1
    from field import field
    from gen_random import gen_random
    from print_result import print_result
    from unique import Unique


@print_result
def f1(arg):
    return sorted(Unique(field(arg, "job-name"), ignore_case=True), key=str.casefold)


@print_result
def f2(arg):
    return list(filter(lambda title: title.casefold().startswith("программист"), arg))


@print_result
def f3(arg):
    return list(map(lambda title: f"{title} с опытом Python", arg))


@print_result
def f4(arg):
    return [f"{title}, зарплата {salary} руб." for title, salary in zip(arg, gen_random(len(arg), 100000, 200000))]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "data_light.json")
    parser.add_argument("--seed", type=int, help="Начальное значение для воспроизводимых примеров")
    args = parser.parse_args(argv)
    if args.seed is not None:
        random.seed(args.seed)
    try:
        with args.path.open(encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        parser.error(str(error))
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        parser.error("Ожидается JSON-массив словарей")
    if any(row.get("job-name") is not None and not isinstance(row["job-name"], str) for row in data):
        parser.error("Поле job-name должно быть строкой или null")
    with cm_timer_1():
        f4(f3(f2(f1(data))))


if __name__ == "__main__":
    main()

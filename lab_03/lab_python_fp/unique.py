"""Итератор уникальных хешируемых элементов с сохранением порядка."""


class Unique:
    def __init__(self, items, **kwargs):
        unknown = kwargs.keys() - {"ignore_case"}
        if unknown:
            raise TypeError(f"Неизвестные параметры: {', '.join(sorted(unknown))}")
        self.ignore_case = kwargs.get("ignore_case", False)
        if not isinstance(self.ignore_case, bool):
            raise TypeError("ignore_case должен иметь тип bool")
        self._items = iter(items)
        self._seen = set()

    def __iter__(self):
        return self

    def __next__(self):
        for item in self._items:
            key = item.casefold() if self.ignore_case and isinstance(item, str) else item
            if key not in self._seen:
                self._seen.add(key)
                return item
        raise StopIteration


if __name__ == "__main__":
    print(list(Unique([1, 1, 1, 2, 2, 2])))
    letters = ["a", "A", "b", "B", "a", "A", "b", "B"]
    print(list(Unique(letters)))
    print(list(Unique(letters, ignore_case=True)))
    print(list(Unique(value % 3 for value in range(8))))

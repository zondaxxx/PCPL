"""Выбор непустых значений полей из последовательности словарей."""


def field(items, *args):
    if not args:
        raise ValueError("Укажите хотя бы одно имя поля")
    for item in items:
        if len(args) == 1:
            value = item.get(args[0])
            if value is not None:
                yield value
        else:
            selected = {key: item[key] for key in args if item.get(key) is not None}
            if selected:
                yield selected


if __name__ == "__main__":
    goods = [
        {"title": "Ковер", "price": 2000, "color": "green"},
        {"title": "Диван для отдыха", "color": "black"},
        {"title": None, "price": None},
    ]
    print(list(field(goods, "title")))
    print(list(field(goods, "title", "price")))

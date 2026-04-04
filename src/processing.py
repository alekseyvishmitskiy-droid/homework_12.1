import ast
from typing import Any

"""
В модуле processing напишите функцию filter_by_state,
которая принимает список словарей и опционально значение для ключа
state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей,
содержащий только те словари, у которых ключ
state соответствует указанному значению.
"""

"""
В том же модуле напишите функцию sort_by_date,
которая принимает список словарей и необязательный параметр,
задающий порядок сортировки (по умолчанию — убывание).
Функция должна возвращать новый список, отсортированный по дате (date).
"""


def filter_by_state(data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    return sorted(data, key=lambda x: str(x.get("date", "")), reverse=reverse)


def main() -> None:
    user_input = input("Введите список транзакций:")

    try:
        data = ast.literal_eval(user_input)

        if not isinstance(data, list):
            print("Ошибка: Введенные данные должны быть списком.")
            return

        print("\n# Выход функции со статусом 'EXECUTED':")
        print(filter_by_state(data))

        print("\n# Выход функции со статусом 'CANCELED':")
        print(filter_by_state(data, state="CANCELED"))

        print("\n# Весь список, отсортированный по дате (от новых к старым):")
        print(sort_by_date(data))

    except SyntaxError:
        print("Ошибка: Некорректный формат данных.")


if __name__ == "__main__":
    main()

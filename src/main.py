import os
import re
from collections import Counter
from typing import Any, Dict, List

from src.processing import filter_by_state, sort_by_date
from src.utils import filter_transactions_by_currency, get_transactions_data
from src.widget_csv import process_bank_transactions
from src.widget_excel import process_bank_transactions_excel

Transaction = Dict[Any, Any]


def process_bank_search(data: List[Transaction], search: str) -> List[Transaction]:
    """
    Задание 1: Поиск по описанию с использованием регулярных выражений.
    Использует библиотеку re.
    """
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [op for op in data if pattern.search(str(op.get("description", "")))]


def count_operations_by_category(operations: List[Transaction]) -> Dict[str, int]:
    """
    Задание 2: Подсчет количества операций по категориям в поле description.
    """
    processed_descriptions = []
    for op in operations:
        desc = op.get("description")
        if desc is None or str(desc).strip() == "":
            processed_descriptions.append("Не указано")
        else:
            processed_descriptions.append(str(desc))

    return dict(Counter(processed_descriptions))


def main() -> None:
    """
    Задание 3: Основная логика программы.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice: str = input("Пользователь: ").strip()
    data: List[Transaction] = []

    if choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        data = get_transactions_data(os.path.join("data", "operations.json"))
    elif choice == "2":
        print("\nПрограмма: Для обработки выбран CSV-файл.")
        data = process_bank_transactions(os.path.join("data", "transactions.csv"))
    elif choice == "3":
        print("\nПрограмма: Для обработки выбран XLSX-файл.")
        data = process_bank_transactions_excel(os.path.join("data", "transactions_excel.xlsx"))
    else:
        print("Ошибка: Неверный выбор.")
        return

    if not data:
        print("Программа: Данные не загружены или список пуст.")
        return

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input: str = input("Пользователь: ").strip()
        status_upper: str = status_input.upper()

        if status_upper in ["EXECUTED", "CANCELED", "PENDING"]:
            data = filter_by_state(data, status_upper)
            print(f'Программа: Операции отфильтрованы по статусу "{status_upper}"')
            break
        print(f'Программа: Статус операции "{status_input}" недоступен.')

    if input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ").lower() == "да":
        order: str = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").lower()
        data = sort_by_date(data, reverse=(False if "возраст" in order else True))

    if input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").lower() == "да":
        data = filter_transactions_by_currency(data, "RUB")

    if (
        input("\nПрограмма: Отфильтровать список по определенному слову в описании? Да/Нет\nПользователь: ").lower()
        == "да"
    ):
        query: str = input("Введите строку для поиска: ").strip()
        data = process_bank_search(data, query)

    print("\nПрограмма: Распечатываю итоговый список транзакций...")

    if not data:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}")

    for op in data:
        date: str = str(op.get("date", "00.00.0000"))
        desc: str = str(op.get("description", "Без описания"))

        from_acc = op.get("from", "")
        to_acc = op.get("to", "—")

        if from_acc and from_acc != "—":
            path = f"{from_acc} -> {to_acc}"
        else:
            path = to_acc

        amt_info = op.get("operationAmount")
        if isinstance(amt_info, dict):
            amount = amt_info.get("amount")
            currency = amt_info.get("currency", {}).get("name")
        else:
            amount = op.get("amount")
            currency = op.get("currency_name", "руб.")

        print(f"\n{date} {desc}")
        print(path)
        print(f"Сумма: {amount} {currency}")

    print("\n--- Статистика по категориям в финальной выборке ---")
    stats = count_operations_by_category(data)
    for cat, count in stats.items():
        print(f"{cat}: {count}")


if __name__ == "__main__":
    main()

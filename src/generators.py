from typing import Any, Generator, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """
    Функция принимает на вход список словарей, представляющих транзакции.
    Функция возвращать итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


transactions: list[dict[str, Any]] = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]

target_currency = input("Введите валюту: ").upper()
usd_transactions = filter_by_currency(transactions, target_currency)

try:
    print(next(usd_transactions))
except StopIteration:
    print("Ничего не найдено")


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Generator[str, None, None]:
    """
    Генератор принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Перевод организации"},
    {"description": "Оплата услуг"},
]

descriptions = transaction_descriptions(transactions)

count_input = input("Сколько описаний вывести? (например, 5): ")

try:
    count = int(count_input)
    print("\n--- Результат ---")

    for _ in range(count):
        print(next(descriptions))

except ValueError:
    print("Ошибка: введите целое число.")
except StopIteration:
    print("\n[Транзакции в списке закончились]")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор выдает номера банковских карт в формате XXXX XXXX XXXX XXXX,
    где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне
    от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    Генератор должен принимать начальное и конечное значения для генерации диапазона номеров.
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"


try:
    start_val = int(input("Введите начало диапазона: "))
    stop_val = int(input("Введите конец диапазона: "))

    if start_val > stop_val:
        print("\nОшибка: начало диапазона не может быть больше конца.")
    else:
        print("\n>>>")
        for card_number in card_number_generator(start_val, stop_val):
            print(f"    {card_number}")

except ValueError:
    print("Ошибка: введите целое число.")

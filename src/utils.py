import logging
import os
import json
from typing import List, Dict, Any, cast

TransactionList = List[Dict[str, Any]]

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transactions_data(path: str) -> TransactionList:
    """Читает JSON-файл и возвращает список транзакций."""
    logger.info(f"ПОЛЬЗОВАТЕЛЬ ЗАПРОСИЛ ФАЙЛ: {path}")

    if not path:
        logger.error("Введен пустой путь к файлу")
        return []

    if not os.path.exists(path):
        logger.warning(f"ФАЙЛ НЕ НАЙДЕН: {path}")
        print(f"Ошибка: Файл '{path}' не существует.")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"УСПЕХ: Загружено {len(data)} транзакций из {path}")
                return cast(TransactionList, data)
            else:
                logger.error(f"ФОРМАТ ОШИБКА: Файл {path} содержит {type(data)}, а не список")
                return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON ОШИБКА в файле {path}: {e}")
        print("Ошибка: Неверный формат JSON в файле.")
        return []
    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА при чтении {path}: {e}")
        return []


def filter_transactions_by_currency(transactions: TransactionList, currency_code: str) -> TransactionList:
    """Фильтрует транзакции по заданному коду валюты (например, 'USD')."""
    logger.info(f"Фильтрация транзакций по валюте: {currency_code}")

    filtered_transactions = []
    for transaction in transactions:
        amount_info = transaction.get("operationAmount")
        if isinstance(amount_info, dict):
            code = amount_info.get("currency", {}).get("code")
        else:
            code = transaction.get("currency")

        if code == currency_code:
            filtered_transactions.append(transaction)

    logger.info(f"Найдено транзакций: {len(filtered_transactions)}")
    return filtered_transactions


if __name__ == "__main__":
    print("--- 📂 Работа с данными транзакций ---")

    file_path = input("Введите путь к JSON-файлу (например, data/operations.json): ").strip()

    transactions = get_transactions_data(file_path)

    if transactions:
        print(f"✅ Успешно прочитано транзакций: {len(transactions)}")
        print("Первая запись:", transactions[0])
    else:
        print("❌ Не удалось получить данные. Подробности в logs/utils.log")

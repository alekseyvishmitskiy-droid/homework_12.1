import json
import os
from typing import Any, Callable, Dict, List, Optional, cast

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY: Optional[str] = os.getenv("EXCHANGE_RATE_API_KEY")

TransactionList = List[Dict[str, Any]]


def stat_decorator(func: Callable[..., TransactionList]) -> Callable[..., TransactionList]:
    """Декоратор для вывода статистики по отфильтрованным транзакциям."""

    def wrapper(*args: Any, **kwargs: Any) -> TransactionList:
        result = func(*args, **kwargs)
        filtered_transactions = cast(TransactionList, result)

        total_amount = sum([float(t.get("amount", 0)) for t in filtered_transactions])
        print(f"Отфильтровано {len(filtered_transactions)} транзакций на сумму {total_amount}")
        return filtered_transactions

    return wrapper


def get_transactions_data(path: str) -> TransactionList:
    """Читает JSON-файл и возвращает список транзакций."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return cast(TransactionList, data) if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


@stat_decorator
def filter_transactions_by_currency(input_file: str, output_file: str, currency_code: str) -> TransactionList:
    """Фильтрует транзакции из файла по валюте и сохраняет результат."""
    transactions = get_transactions_data(input_file)

    filtered = [
        t
        for t in transactions
        if t.get("currency") == currency_code
        or (
            isinstance(t.get("operationAmount"), dict)
            and cast(dict, t.get("operationAmount")).get("currency", {}).get("code") == currency_code
        )
    ]

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(filtered, f, indent=4, ensure_ascii=False)

    return filtered


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Запрашивает актуальный курс через API и конвертирует сумму в рубли.
    """
    operation_amount: Dict[str, Any] = transaction.get("operationAmount", {})
    amount: float = float(operation_amount.get("amount", 0))
    currency_code: str = operation_amount.get("currency", {}).get("code", "RUB")

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        current_api_key = API_KEY or os.getenv("EXCHANGE_RATE_API_KEY")

        if not current_api_key:
            print("Критическая ошибка: API_KEY не найден в .env")
            return 0.0

        url = f"https://apilayer.com{currency_code}&amount={amount}"
        headers = {"apikey": current_api_key}

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            result: float = float(response.json().get("result", 0))
            return result
        except Exception:
            return 0.0

    return 0.0

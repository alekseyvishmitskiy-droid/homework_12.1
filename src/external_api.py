import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Принимает транзакцию и возвращает сумму в рублях (float).
    Если валюта USD или EUR, конвертирует сумму через Exchange Rates Data API.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency_code = operation_amount.get("currency", {}).get("code", "RUB")

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        if not API_KEY:
            print("Ошибка: EXCHANGE_RATE_API_KEY не найден в .env")
            return 0.0

        url = f"https://apilayer.com{currency_code}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            return float(data.get("result", 0.0))

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Ошибка при запросе к API для {currency_code}: {e}")
            return 0.0

    return 0.0

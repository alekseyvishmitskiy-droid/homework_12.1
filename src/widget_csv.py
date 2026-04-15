import os
import pandas as pd
from typing import List, Dict, Any
from src.widget import get_date, mask_card_and_account


def process_bank_transactions(file_path: str) -> List[Dict[Any, Any]]:
    """Читает CSV, маскирует данные и возвращает список словарей."""

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return []

    try:
        df = pd.read_csv(file_path, sep=";")

        if "date" in df.columns:
            df["date"] = (
                df["date"].fillna("").apply(lambda x: get_date(str(x)) if str(x).strip() != "" else "00.00.0000")
            )

        if "from" in df.columns:
            df["from"] = (
                df["from"].fillna("").apply(lambda x: mask_card_and_account(str(x)) if str(x).strip() != "" else "—")
            )

        if "to" in df.columns:
            df["to"] = (
                df["to"].fillna("").apply(lambda x: mask_card_and_account(str(x)) if str(x).strip() != "" else "—")
            )

        return df.to_dict(orient="records")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == "__main__":
    file_name = "transactions.csv"
    transactions_list = process_bank_transactions(file_name)

    if transactions_list:
        print(f"Успешно обработано транзакций: {len(transactions_list)}")
        print("Пример данных:", transactions_list[0])

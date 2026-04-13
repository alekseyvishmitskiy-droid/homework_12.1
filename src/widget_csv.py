import os

import pandas as pd

from src.widget import get_date, mask_card_and_account


def process_bank_transactions(file_path):
    """Читает CSV и применяет маскирование к колонкам."""

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return None

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

        return df

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


if __name__ == "__main__":
    file_name = "transactions.csv"

    df_result = process_bank_transactions(file_name)

    if df_result is not None:
        print("РЕЗУЛЬТАТ ОБРАБОТКИ (Первые строки):")

        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 1000)

        cols = ["date", "from", "to", "description", "amount", "state"]
        print(df_result[cols].to_string(index=False))

        df_result.to_csv("transactions_masked.csv", index=False, sep=";")
        print("Результат сохранен в файл: processed_transactions.csv")

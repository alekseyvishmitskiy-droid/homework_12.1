import os
from typing import Optional

import pandas as pd

from src.widget import get_date, mask_card_and_account


def process_bank_transactions_excel(file_path: str) -> Optional[pd.DataFrame]:
    """Читает Excel файл и применяет маскирование к колонкам."""

    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return None

    try:
        # Читаем Excel. Указываем тип возвращаемого значения для mypy
        df: pd.DataFrame = pd.read_excel(file_path, engine="openpyxl")

        # 1. Обрабатываем дату
        if "date" in df.columns:
            df["date"] = (
                df["date"].fillna("").apply(lambda x: get_date(str(x)) if str(x).strip() != "" else "00.00.0000")
            )

        # 2. Маскируем отправителя и получателя
        for col in ["from", "to"]:
            if col in df.columns:
                df[col] = (
                    df[col].fillna("").apply(lambda x: mask_card_and_account(str(x)) if str(x).strip() != "" else "—")
                )

        return df

    except Exception as e:
        print(f"Произошла ошибка при чтении Excel: {e}")
        return None

import os
from typing import Optional

import pandas as pd

from src.widget import get_date, mask_card_and_account


def process_bank_transactions(file_path: str) -> Optional[pd.DataFrame]:
    """Читает CSV и применяет маскирование к колонкам."""

    if not os.path.exists(file_path):
        print(f"❌ Файл {file_path} не найден!")
        return None

    try:
        df: pd.DataFrame = pd.read_csv(file_path, sep=";")

        if "date" in df.columns:
            df["date"] = (
                df["date"].fillna("").apply(lambda x: get_date(str(x)) if str(x).strip() != "" else "00.00.0000")
            )

        for col in ["from", "to"]:
            if col in df.columns:
                df[col] = (
                    df[col].fillna("").apply(lambda x: mask_card_and_account(str(x)) if str(x).strip() != "" else "—")
                )

        return df

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        return None

from typing import Any

import pandas as pd
import pytest

from src.widget_excel import process_bank_transactions_excel


@pytest.fixture
def temp_excel_file(tmp_path: Any) -> str:
    """Создает временный Excel-файл для тестов."""
    data = {
        "id": [650703, 3598919],
        "state": ["EXECUTED", "EXECUTED"],
        "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
        "amount": [16210, 29740],
        "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
        "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
        "description": ["Перевод организации", "Перевод с карты на карту"],
    }
    df = pd.DataFrame(data)

    file_path = tmp_path / "test_transactions.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    return str(file_path)


def test_process_excel_valid_data(temp_excel_file: str) -> None:
    """Тест успешной обработки корректного Excel-файла."""
    result_df = process_bank_transactions_excel(temp_excel_file)

    assert isinstance(result_df, pd.DataFrame)

    assert result_df.loc[0, "from"] == "Счет **3391"

    assert "3172 60** **** 0065" in str(result_df.loc[1, "from"])

    assert result_df.loc[0, "date"] == "05.09.2023"


def test_process_excel_missing_file() -> None:
    """Тест реакции на отсутствие файла."""
    result = process_bank_transactions_excel("non_existent_file.xlsx")
    assert result is None


def test_process_excel_empty_columns(tmp_path: Any) -> None:
    """Тест обработки файла с пустыми значениями (NaN)."""
    data = {"date": ["2023-09-05T11:30:32Z"], "from": [None], "to": ["Счет 12345678901234567890"]}
    df = pd.DataFrame(data)
    file_path = tmp_path / "empty_test.xlsx"
    df.to_excel(file_path, index=False)

    result_df = process_bank_transactions_excel(str(file_path))
    assert result_df is not None
    assert result_df.loc[0, "from"] == "—"

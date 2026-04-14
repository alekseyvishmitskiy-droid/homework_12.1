from unittest.mock import patch

import pandas as pd

from src.widget_csv import process_bank_transactions


def test_process_csv_valid_data() -> None:
    """Тестирование успешного чтения и маскирования CSV."""
    data = {
        "date": ["2023-12-31T12:00:00"],
        "from": ["Visa Platinum 7000792289606611"],
        "to": ["Счет 73654108430135874305"],
        "description": ["Перевод"],
    }
    df = pd.DataFrame(data)

    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read:
        mock_exists.return_value = True
        mock_read.return_value = df

        result = process_bank_transactions("fake_path.csv")

        assert isinstance(result, list)
        assert len(result) == 1
        assert "Visa Platinum 7000 79** **** 6611" in result[0]["from"]
        assert "**4305" in result[0]["to"]


def test_process_csv_missing_file() -> None:
    """Тестирование поведения при отсутствии файла."""
    result = process_bank_transactions("non_existent.csv")
    assert result == []


def test_process_csv_error_during_reading() -> None:
    """Тестирование обработки исключений (например, битый файл)."""
    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read:
        mock_exists.return_value = True
        mock_read.side_effect = Exception("Read error")

        result = process_bank_transactions("corrupt.csv")
        assert result == []


def test_process_csv_empty_file() -> None:
    """Тестирование обработки пустого файла."""
    with patch("os.path.exists") as mock_exists, patch("pandas.read_csv") as mock_read:
        mock_exists.return_value = True
        mock_read.return_value = pd.DataFrame()

        result = process_bank_transactions("empty.csv")
        assert result == []

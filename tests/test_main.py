from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from src.main import count_operations_by_category, main, process_bank_search


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными."""
    return [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Перевод с карты на карту", "amount": 200},
        {"description": "Оплата связи", "amount": 50},
        {"description": None, "amount": 10},
    ]


def test_process_bank_search(sample_data: List[Dict[str, Any]]) -> None:
    """Тест функции поиска по регулярным выражениям."""
    assert len(process_bank_search(sample_data, "перевод")) == 2
    assert len(process_bank_search(sample_data, "ПЕРЕВОД")) == 2
    assert len(process_bank_search(sample_data, ".*")) == 0


def test_count_operations_by_category(sample_data: List[Dict[str, Any]]) -> None:
    """Тест функции подсчета категорий."""
    result = count_operations_by_category(sample_data)
    assert result["Перевод организации"] == 1
    assert result["Оплата связи"] == 1
    assert result.get("None") == 1 or result.get("Не указано") == 1


@patch("src.main.get_transactions_data")
@patch("builtins.input")
def test_main_logic_json(mock_input: MagicMock, mock_get_data: MagicMock) -> None:
    mock_get_data.return_value = [
        {
            "state": "EXECUTED",
            "date": "2023-01-01",
            "description": "Тест",
            "operationAmount": {"amount": "100", "currency": {"name": "RUB"}},
        }
    ]

    mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]

    with patch("builtins.print") as mock_print:
        main()
        mock_print.assert_any_call("\nПрограмма: Распечатываю итоговый список транзакций...")

import json
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

import pytest

from src.utils import filter_transactions_by_currency, get_transactions_data


def test_get_transactions_data_success() -> None:
    """Тест успешного чтения корректного JSON-списка."""
    mock_data = [{"id": 1, "amount": "100"}]
    mock_json = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            result = get_transactions_data("fake_path.json")
            assert result == mock_data
            assert len(result) == 1


def test_get_transactions_data_not_found() -> None:
    """Тест поведения, если файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = get_transactions_data("non_existent.json")
        assert result == []


def test_get_transactions_data_invalid_json() -> None:
    """Тест обработки битого JSON-файла."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            result = get_transactions_data("bad.json")
            assert result == []


def test_get_transactions_data_not_a_list() -> None:
    """Тест случая, когда в JSON не список, а словарь."""
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        with patch("os.path.exists", return_value=True):
            result = get_transactions_data("dict.json")
            assert result == []


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 3, "currency": "USD"},
        {"id": 4, "operationAmount": {"currency": {"code": "EUR"}}},
    ]


def test_filter_transactions_by_usd(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по USD."""
    result = filter_transactions_by_currency(sample_transactions, "USD")
    assert len(result) == 2


def test_filter_transactions_no_match(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации валюты, которой нет в списке."""
    result = filter_transactions_by_currency(sample_transactions, "GBP")
    assert result == []


def test_filter_transactions_empty_list() -> None:
    """Проверка работы с пустым списком."""
    assert filter_transactions_by_currency([], "RUB") == []

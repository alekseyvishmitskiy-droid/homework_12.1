from typing import Any
from unittest.mock import patch, MagicMock
from src.external_api import get_transaction_amount_in_rub


def test_get_amount_rub() -> None:
    """Проверка возврата суммы, если валюта уже RUB."""
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    assert get_transaction_amount_in_rub(transaction) == 100.50


def test_get_amount_no_data() -> None:
    """Проверка поведения при пустой транзакции."""
    assert get_transaction_amount_in_rub({}) == 0.0


@patch("requests.get")
@patch("src.external_api.API_KEY", "fake_key")
def test_get_amount_usd_success(mock_get: Any) -> None:
    """Успешный запрос конвертации USD -> RUB."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 7500.0}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

    result = get_transaction_amount_in_rub(transaction)

    assert result == 7500.0
    mock_get.assert_called_once()


@patch("requests.get")
@patch("src.external_api.API_KEY", "fake_key")
def test_get_amount_api_error(mock_get: Any) -> None:
    """Проверка обработки ошибки сервера."""
    import requests

    mock_get.side_effect = requests.RequestException("Connection error")

    transaction = {"operationAmount": {"amount": "50", "currency": {"code": "EUR"}}}

    assert get_transaction_amount_in_rub(transaction) == 0.0


def test_get_amount_no_api_key() -> None:
    """Проверка случая, когда API_KEY отсутствует."""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

    with patch("src.external_api.API_KEY", None):
        assert get_transaction_amount_in_rub(transaction) == 0.0

import unittest
from typing import Any
from unittest.mock import MagicMock, patch

import requests

from src.utils import get_transaction_amount_in_rub


class TestExternalApi(unittest.TestCase):

    def test_amount_rub(self) -> None:
        """1. Тест транзакции в рублях (без вызова API)"""
        transaction: dict[str, Any] = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
        self.assertEqual(get_transaction_amount_in_rub(transaction), 100.50)

    @patch("os.getenv")
    @patch("requests.get")
    def test_amount_conversion_usd(self, mock_get: MagicMock, mock_getenv: MagicMock) -> None:
        """2. Тест успешной конвертации из USD через мок API"""
        mock_getenv.return_value = "fake_api_key_for_test"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 7500.0}
        mock_get.return_value = mock_response

        transaction: dict[str, Any] = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        result = get_transaction_amount_in_rub(transaction)

        self.assertEqual(result, 7500.0)
        mock_get.assert_called_once()

    @patch("os.getenv")
    def test_missing_api_key(self, mock_getenv: MagicMock) -> None:
        """3. Тест сценария, когда API_KEY отсутствует в .env"""
        mock_getenv.return_value = None

        transaction: dict[str, Any] = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}

        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 0.0)

    @patch("os.getenv")
    @patch("requests.get")
    def test_api_error(self, mock_get: MagicMock, mock_getenv: MagicMock) -> None:
        """4. Тест поведения при сетевой ошибке API (должен вернуть 0.0)"""
        mock_getenv.return_value = "fake_api_key_for_test"

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        transaction: dict[str, Any] = {"operationAmount": {"amount": "100", "currency": {"code": "EUR"}}}

        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()

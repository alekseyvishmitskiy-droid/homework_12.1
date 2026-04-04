from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_card_and_account


@pytest.fixture
def data() -> List[Dict[str, Any]]:
    return [
        {"id": 441945873, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 594223403, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-16T07:33:05.103048"},
    ]


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Maestro 1596837814705307", "Maestro 1596 83** **** 5307"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("", "Ошибка: Пустая строка"),
    ],
)
def test_mask_card_and_account_valid(input_string: str, expected: str) -> None:
    assert mask_card_and_account(input_string) == expected


@pytest.mark.parametrize(
    "date_input, expected_date",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2018-12-31T23:59:59", "31.12.2018"),
    ],
)
def test_get_date_valid(date_input: str, expected_date: str) -> None:
    assert get_date(date_input) == expected_date


def test_filter_by_state_executed(data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации EXECUTED (по умолчанию)"""
    result = filter_by_state(data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_canceled(data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации CANCELED"""
    result = filter_by_state(data, state="CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 594223403


def test_filter_by_state_empty_list() -> None:
    """Проверка фильтрации пустого списка"""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_no_match(data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации несуществующего статуса"""
    assert filter_by_state(data, state="PENDING") == []


def test_sort_by_date_descending(data: List[Dict[str, Any]]) -> None:
    """Сортировка от новых к старым (reverse=True по умолчанию)"""
    result = sort_by_date(data)
    assert result[0]["id"] == 441945873  # 2019 год
    assert result[-1]["id"] == 939719570  # 2018 июнь


def test_sort_by_date_ascending(data: List[Dict[str, Any]]) -> None:
    """Сортировка от старых к новым (reverse=False)"""
    result = sort_by_date(data, reverse=False)
    assert result[0]["id"] == 939719570  # 2018 июнь
    assert result[-1]["id"] == 441945873  # 2019 год


def test_sort_by_date_empty_list() -> None:
    """Проверка сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_by_date_missing_key() -> None:
    """Проверка устойчивости, если у одного из словарей нет ключа date"""
    data_missing: List[Dict[str, Any]] = [{"id": 1, "date": "2023-01-01"}, {"id": 2}]

    result = sort_by_date(data_missing)
    assert len(result) == 2
    assert result[0]["id"] == 1


def test_main_success(capsys: Any) -> None:
    """Тест успешного выполнения main с корректным вводом"""
    user_input = '[{"id": 1, "state": "EXECUTED", "date": "2023-01-01"}]'

    with patch("builtins.input", return_value=user_input):
        from src.processing import main

        main()

    captured = capsys.readouterr()
    assert "# Выход функции со статусом 'EXECUTED':" in captured.out
    assert "EXECUTED" in captured.out


def test_main_invalid_format(capsys: Any) -> None:
    """Тест main с некорректным синтаксисом (SyntaxError)"""
    with patch("builtins.input", return_value="not a list"):
        from src.processing import main

        main()

    captured = capsys.readouterr()
    assert "Ошибка: Некорректный формат данных." in captured.out


def test_main_not_a_list(capsys: Any) -> None:
    """Тест main, когда введен словарь вместо списка"""
    with patch("builtins.input", return_value='{"id": 1}'):
        from src.processing import main

        main()

    captured = capsys.readouterr()
    assert "Ошибка: Введенные данные должны быть списком." in captured.out

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_valid() -> None:
    """Проверка корректного номера карты"""
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_get_mask_card_number_invalid_length() -> None:
    """Проверка ошибки при неверной длине номера карты"""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        get_mask_card_number("12345")


def test_get_mask_account_valid() -> None:
    """Проверка корректного номера счета"""
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_short() -> None:
    """Проверка ошибки при слишком коротком номере счета"""
    with pytest.raises(ValueError, match="Номер счета слишком короткий"):
        get_mask_account("123")


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1111222233334444", "1111 22** **** 4444"),
        ("0000000000000000", "0000 00** **** 0000"),
    ],
)
def test_get_mask_card_number_various(card_number: str, expected: str) -> None:
    """Проверка различных номеров карт через параметры"""
    assert get_mask_card_number(card_number) == expected

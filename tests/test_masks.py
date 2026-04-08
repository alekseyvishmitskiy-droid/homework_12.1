import pytest
import logging
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_success(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    result = get_mask_card_number("7000 7922 8960 6361")

    assert result == "7000 79** **** 6361"
    assert "УСПЕХ: Карта замаскирована" in caplog.text


def test_get_mask_card_number_invalid_chars(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR)
    result = get_mask_card_number("7000 7922 8960 abcd")

    assert result == "некорректный номер (содержит буквы)"
    assert "ОШИБКА: Номер карты содержит недопустимые символы" in caplog.text


def test_get_mask_card_number_wrong_length(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR)
    result = get_mask_card_number("12345")

    assert result == "некорректный номер (не 16 цифр)"
    assert "Неверная длина номера карты" in caplog.text


def test_get_mask_account_success(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    result = get_mask_account("73654108430135874305")

    assert result == "**4305"
    assert "УСПЕХ: Счет замаскирован" in caplog.text


def test_get_mask_account_too_short(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR)
    result = get_mask_account("123")

    assert result == "некорректный номер (слишком короткий)"
    assert "Номер счета слишком короткий" in caplog.text


def test_get_mask_account_non_digit(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR)
    result = get_mask_account("12345A")

    assert result == "некорректный номер"
    assert "содержит недопустимые символы" in caplog.text

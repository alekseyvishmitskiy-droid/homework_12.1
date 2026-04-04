from typing import Any, Generator, Iterator

import pytest


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:  # Теперь Mypy будет знать, что здесь работает next()
    return (tx for tx in transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == currency)


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Generator[str, None, None]:
    for tx in transactions:
        yield tx.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    for number in range(start, end + 1):
        s = f"{number:016d}"
        yield f"{s[:4]} {s[4:8]} {s[8:12]} {s[12:]}"


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    return [
        {"operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод 1"},
        {"operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод 2"},
        {"operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод 3"},
    ]


def test_filter_by_currency(sample_transactions: list[dict[str, Any]]) -> None:
    usd_iter = filter_by_currency(sample_transactions, "USD")
    assert next(usd_iter)["description"] == "Перевод 1"
    assert next(usd_iter)["description"] == "Перевод 3"
    with pytest.raises(StopIteration):
        next(usd_iter)


def test_transaction_descriptions(sample_transactions: list[dict[str, Any]]) -> None:
    descriptions = transaction_descriptions(sample_transactions)
    assert next(descriptions) == "Перевод 1"
    assert next(descriptions) == "Перевод 2"
    assert next(descriptions) == "Перевод 3"


def test_card_number_generator() -> None:
    gen = card_number_generator(1, 2)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_range() -> None:
    gen = card_number_generator(9999999999999998, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9998"
    assert next(gen) == "9999 9999 9999 9999"

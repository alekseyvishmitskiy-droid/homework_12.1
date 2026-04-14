from src.widget_excel import process_bank_transactions_excel


def test_process_excel_valid_data() -> None:
    result = process_bank_transactions_excel("tests/test_data.xlsx")

    assert isinstance(result, list)
    if len(result) > 0:
        assert "date" in result[0]
        assert "from" in result[0]


def test_process_excel_missing_file() -> None:
    result = process_bank_transactions_excel("non_existent.xlsx")
    assert result == []


def test_process_excel_empty_columns() -> None:
    result = process_bank_transactions_excel("tests/empty.xlsx")
    assert isinstance(result, list)

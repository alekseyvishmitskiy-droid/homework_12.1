from typing import Any

import pytest

from src.decorators import log


def test_log_console_success(capsys: Any) -> None:
    """Тест логирования успешного выполнения в консоль."""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    add(1, 2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_log_file_success(tmp_path: Any) -> None:
    """Тест логирования успешного выполнения в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    multiply(3, 4)

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read().strip()

    assert log_content == "multiply ok"


def test_log_file_error(tmp_path: Any) -> None:
    """Тест логирования ошибки в файл."""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read().strip()

    assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in log_content


def test_log_preserves_metadata() -> None:
    """Тест сохранения метаданных функции (имя, docstring)."""

    @log()
    def sample_func() -> bool:
        """Test docstring"""
        return True

    assert sample_func.__name__ == "sample_func"
    assert sample_func.__doc__ == "Test docstring"

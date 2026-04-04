import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования результатов работы функции.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}"
                _write_log(log_message, filename)
                raise e

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Записывает сообщение в файл (если задан) или в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    else:
        print(message)


@log()
def divide(x: int, y: int) -> float:
    return x / y


if __name__ == "__main__":
    try:
        divide(1, 0)
    except ZeroDivisionError:
        pass

from src.masks import get_mask_account, get_mask_card_number


def mask_card_and_account(data: str) -> str:
    """Маскирует номер карты или счета, даже если введены только цифры."""
    if not data or not data.strip():
        return "Ошибка: Введена пустая строка"

    parts = data.split()

    if len(parts) == 1:
        number = parts[0]
        if number.isdigit():
            return get_mask_card_number(number)
        else:
            return "Ошибка: Введите номер цифрами или укажите название (напр. Счет 1234...)"

    number = parts[-1]
    name = " ".join(parts[:-1])

    if "Счет" in name:
        masked_result = get_mask_account(number)
    else:
        masked_result = get_mask_card_number(number)

    return f"{name} {masked_result}"


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ."""
    try:
        date_part = date_string.split("T")[0]
        parts = date_part.split("-")

        if len(parts) != 3:
            return "неверный формат"

        year, month, day = parts
        return f"{day}.{month}.{year}"
    except Exception:
        return "неверный формат"


def main() -> None:
    """Основной цикл программы."""
    print("--- 🛠 Программа обработки банковских данных ---")
    print("Теперь можно вводить просто цифры карты без названия.")
    print("Введите 'выход' для завершения.\n")

    while True:
        print("-" * 30)
        user_input = input("Введите данные: ").strip()

        if user_input.lower() in ["выход", "exit", "quit"]:
            break

        if not user_input:
            continue

        if "T" in user_input and "-" in user_input:
            print(f"Результат (Дата): {get_date(user_input)}")
        else:
            print(f"Результат (Маска): {mask_card_and_account(user_input)}")


if __name__ == "__main__":
    main()

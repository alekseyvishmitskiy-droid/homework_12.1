def get_mask_card_number(number: str) -> str:
    """Изменяем номер карты"""
    if len(number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{number[:4]} {number[4:6]}** **** {number[-4:]}"


def get_mask_account(number: str) -> str:
    """Изменяем номер счета"""
    if len(number) < 4:
        raise ValueError("Номер счета слишком короткий")

    return f"**{number[-4:]}"

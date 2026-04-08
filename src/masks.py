import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(number: str) -> str:
    """Маскирует номер карты и логирует детали процесса."""
    logger.info(f"Пользователь запросил маскирование КАРТЫ. Ввод: '{number}'")

    clean_number = number.replace(" ", "")

    if not clean_number.isdigit():
        logger.error(f"ОШИБКА: Номер карты содержит недопустимые символы (не цифры): '{clean_number}'")
        return "некорректный номер (содержит буквы)"

    if len(clean_number) != 16:
        logger.error(
            f"ОШИБКА: Неверная длина номера карты. Ожидалось 16, получено {len(clean_number)}: '{clean_number}'"
        )
        return "некорректный номер (не 16 цифр)"

    result = f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
    logger.info(f"УСПЕХ: Карта замаскирована: {result}")
    return result


def get_mask_account(number: str) -> str:
    """Маскирует номер счета и логирует детали процесса."""
    logger.info(f"Пользователь запросил маскирование СЧЕТА. Ввод: '{number}'")

    clean_number = number.replace(" ", "")

    if not clean_number.isdigit():
        logger.error(f"ОШИБКА: Номер счета содержит недопустимые символы: '{clean_number}'")
        return "некорректный номер"

    if len(clean_number) < 4:
        logger.error(f"ОШИБКА: Номер счета слишком короткий ({len(clean_number)} цифр), минимум 4")
        return "некорректный номер (слишком короткий)"

    result = f"**{clean_number[-4:]}"
    logger.info(f"УСПЕХ: Счет замаскирован: {result}")
    return result

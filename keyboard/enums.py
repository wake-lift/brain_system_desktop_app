from core.enums import StrLabelEnum


class PressedKeyEnum(StrLabelEnum):
    """All available pressed keyboard keys."""

    RED = '1', 'Нажата красная кнопка игрока'
    GREEN = '2', 'Нажата зеленая кнопка игрока'
    YELLOW = '3', 'Нажата желтая кнопка игрока'
    BLUE = '4', 'Нажата синяя кнопка игрока'
    WHITE = '5', 'Нажата белая кнопка игрока'
    BLACK = '6', 'Нажата черная кнопка игрока'

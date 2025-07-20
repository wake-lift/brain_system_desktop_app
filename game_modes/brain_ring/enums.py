from core.enums import StrLabelEnum


class BrainRingGameStatusEnum(StrLabelEnum):
    """Возможные статусы раунда (брейн-ринг)."""

    READY_TO_START_COUNTDOWN = 'Ready to start/resume timer', 'Готов к старту таймера'
    COUNTDOWN_STARTED = 'Timer started', 'Начат обратный отсчет'
    PLAYER_BUTTON_PRESSED = 'Player button pressed', 'Нажата кнопка'
    FALSE_START = 'False start', 'Фальстарт'
    TIME_IS_UP = 'Time is up', 'Время вышло'

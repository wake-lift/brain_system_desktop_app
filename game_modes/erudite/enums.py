from core.enums import StrLabelEnum


class EruditeGameStatusEnum(StrLabelEnum):
    """Возможные статусы раунда (эрудитка)."""

    READY_TO_START_COUNTDOWN = 'Ready to start/resume timer', 'Готов к старту таймера'
    COUNTDOWN_STARTED = 'Timer started', 'Начат обратный отсчет'
    PLAYER_BUTTON_PRESSED = 'Player button pressed', 'Нажата кнопка'
    TIME_IS_UP = 'Time is up', 'Время вышло'

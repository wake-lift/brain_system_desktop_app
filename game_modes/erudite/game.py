from PyQt6.QtCore import QTime

from game_modes.erudite.enums import EruditeGameStatusEnum


class EruditeGame:
    """Класс с параметрами игры в эрудитку."""

    def __init__(self, status: EruditeGameStatusEnum = EruditeGameStatusEnum.READY_TO_START_COUNTDOWN) -> None:
        self.status: EruditeGameStatusEnum = status
        self.first_button_pressed_time: QTime | None = None

from PyQt6.QtCore import QTime

from game_modes.brain_ring.enums import BrainRingGameStatusEnum


class BrainRingGame:
    def __init__(
        self,
        status: BrainRingGameStatusEnum = BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN,
        is_false_start_active: bool = False,
    ) -> None:
        self.status: BrainRingGameStatusEnum = status
        self.is_false_start_active: bool = is_false_start_active
        self.first_button_pressed_time: QTime | None = None

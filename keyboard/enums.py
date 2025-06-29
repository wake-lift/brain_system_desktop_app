from enum import StrEnum

from config.config import AppConfig
from core.enums import StrLabelEnum


app_config = AppConfig()


class PlayerPressedKeyEnum(StrLabelEnum):
    """All available keyboard keys, which can be pressed by players."""

    RED = '1', 'red'
    GREEN = '2', 'green'
    YELLOW = '3', 'yellow'
    BLUE = '4', 'blue'
    WHITE = '5', 'white'
    BLACK = '6', 'black'


class ModeratorPressedKeyEnum(StrEnum):
    """All available keyboard keys, which can be pressed by moderator."""

    START_RESUME = app_config.brain_ring_start_resume_key
    RESET_PAUSE = app_config.brain_ring_reset_pause_key
    RESET_ROUND = app_config.brain_ring_reset_round_key

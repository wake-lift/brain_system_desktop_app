from core.enums import StrLabelEnum


class PlayerPressedKeyEnum(StrLabelEnum):
    """All available keyboard keys, which can be pressed by players."""

    RED = '1', 'red'
    GREEN = '2', 'green'
    YELLOW = '3', 'yellow'
    BLUE = '4', 'blue'
    WHITE = '5', 'white'
    BLACK = '6', 'black'

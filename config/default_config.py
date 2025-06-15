from typing import Dict

from config.enums import GameTypeEnum


DEFAULT_CONFIG: Dict[str, Dict[str, str | int | bool]] = {
    'GENERAL': {
        'game_type': GameTypeEnum.BRAIN_RING.value,
    },
    'BRAIN_RING': {
        'brain_ring_round_time': 30,
    },
    'WHAT_WHERE_WHEN': {},
    'ERUDITE': {},
    'BUTTONS': {
        'red_button_enabled': True,
        'red_button_player_name': 'Red Team',
        'green_button_enabled': True,
        'green_button_player_name': 'Green Team',
        'blue_button_enabled': False,
        'blue_button_player_name': 'Blue Team',
        'yellow_button_enabled': False,
        'yellow_button_player_name': 'Yellow Team',
        'white_button_enabled': False,
        'white_button_player_name': 'White Team',
        'black_button_enabled': False,
        'black_button_player_name': 'Black Team',
    },
}

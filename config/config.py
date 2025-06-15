from configparser import ConfigParser
from pathlib import Path
from typing import List
from config.config_parser import CONFIG_FILE_PATH, brain_ring_config, buttons_config, config, general_config
from config.default_config import DEFAULT_CONFIG


class AppConfig:
    def __init__(self) -> None:
        self.game_type: str = general_config.get(
            option='game_type', fallback=DEFAULT_CONFIG['GENERAL']['game_type']
        )
        self.brain_ring_round_time: int = brain_ring_config.getint(
            option='brain_ring_round_time', fallback=DEFAULT_CONFIG['BRAIN_RING']['brain_ring_round_time'],
        )
        self.red_button_enabled: bool = buttons_config.getboolean(
            option='red_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['red_button_enabled'],
        )
        self.red_button_player_name: int = buttons_config.get(
            option='red_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['red_button_player_name'],
        )
        self.green_button_enabled: bool = buttons_config.getboolean(
            option='green_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['green_button_enabled'],
        )
        self.green_button_player_name: int = buttons_config.get(
            option='green_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['green_button_player_name'],
        )
        self.blue_button_enabled: bool = buttons_config.getboolean(
            option='blue_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['blue_button_enabled'],
        )
        self.blue_button_player_name: int = buttons_config.get(
            option='blue_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['blue_button_player_name'],
        )
        self.yellow_button_enabled: bool = buttons_config.getboolean(
            option='yellow_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['yellow_button_enabled'],
        )
        self.yellow_button_player_name: int = buttons_config.get(
            option='yellow_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['yellow_button_player_name'],
        )
        self.white_button_enabled: bool = buttons_config.getboolean(
            option='white_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['white_button_enabled'],
        )
        self.white_button_player_name: int = buttons_config.get(
            option='white_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['white_button_player_name'],
        )
        self.black_button_enabled: bool = buttons_config.getboolean(
            option='black_button_enabled', fallback=DEFAULT_CONFIG['BUTTONS']['black_button_enabled'],
        )
        self.black_button_player_name: int = buttons_config.get(
            option='black_button_player_name', fallback=DEFAULT_CONFIG['BUTTONS']['black_button_player_name'],
        )

    def update_config_file(self) -> None:
        config_attrs: List[str] = [attr for attr in self.__dict__ if not attr.startswith('__')]
        for section in DEFAULT_CONFIG.keys():
            for config_attr in config_attrs:
                if config_attr in DEFAULT_CONFIG[section].keys():
                    config.set(section=section, option=config_attr, value=str(getattr(self, config_attr)))

        self._write_config_file(CONFIG_FILE_PATH, config)

    def restore_default_config_file(self):
        for section in DEFAULT_CONFIG.keys():
            for option, option_value in DEFAULT_CONFIG[section].items():
                config.set(section=section, option=option, value=str(option_value))

        self._write_config_file(CONFIG_FILE_PATH, config)

    @staticmethod
    def _write_config_file(config_file_path: Path, config: ConfigParser):
        with open(config_file_path, 'w') as config_file:
            config.write(config_file, space_around_delimiters=True)

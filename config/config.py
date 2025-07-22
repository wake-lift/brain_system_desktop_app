from __future__ import annotations

from typing import TYPE_CHECKING, List

from config.config_parser import (
    CONFIG_FILE_PATH,
    brain_ring_config,
    config,
    erudite_config,
    general_config,
    moderator_buttons_config,
    player_buttons_config,
    www_config,
)
from config.default_config import DEFAULT_CONFIG


if TYPE_CHECKING:
    from configparser import ConfigParser
    from pathlib import Path


class AppConfig:  # noqa: WPS230
    """Класс, содержащий основные настройки приложения."""

    def __init__(self) -> None:
        www_defaults: dict[str, int] = DEFAULT_CONFIG['WHAT_WHERE_WHEN']
        player_buttons_defaults: dict[str, str | bool] = DEFAULT_CONFIG['PLAYER_BUTTONS']
        moderator_buttons_defaults: dict[str, str | bool] = DEFAULT_CONFIG['MODERATOR_BUTTONS']

        self.game_type: str = general_config.get(
            option='game_type', fallback=DEFAULT_CONFIG['GENERAL']['game_type']
        )
        self.brain_ring_round_time: int = brain_ring_config.getint(
            option='brain_ring_round_time', fallback=DEFAULT_CONFIG['BRAIN_RING']['brain_ring_round_time'],
        )
        self.www_regular_time: int = www_config.getint(
            option='www_regular_time', fallback=www_defaults['www_regular_time'],
        )
        self.www_blitz_time: int = www_config.getint(
            option='www_blitz_time', fallback=www_defaults['www_blitz_time'],
        )
        self.www_super_blitz_time: int = www_config.getint(
            option='www_super_blitz_time', fallback=www_defaults['www_super_blitz_time'],
        )
        self.www_time_to_provide_answers: int = www_config.getint(
            option='www_time_to_provide_answers',
            fallback=www_defaults['www_time_to_provide_answers'],
        )
        self.erudite_round_time: int = erudite_config.getint(
            option='erudite_round_time', fallback=DEFAULT_CONFIG['ERUDITE']['erudite_round_time'],
        )
        self.red_button_enabled: bool = player_buttons_config.getboolean(
            option='red_button_enabled', fallback=player_buttons_defaults['red_button_enabled'],
        )
        self.red_button_player_name: str = player_buttons_config.get(
            option='red_button_player_name', fallback=player_buttons_defaults['red_button_player_name'],
        )
        self.green_button_enabled: bool = player_buttons_config.getboolean(
            option='green_button_enabled', fallback=player_buttons_defaults['green_button_enabled'],
        )
        self.green_button_player_name: str = player_buttons_config.get(
            option='green_button_player_name', fallback=player_buttons_defaults['green_button_player_name'],
        )
        self.blue_button_enabled: bool = player_buttons_config.getboolean(
            option='blue_button_enabled', fallback=player_buttons_defaults['blue_button_enabled'],
        )
        self.blue_button_player_name: str = player_buttons_config.get(
            option='blue_button_player_name', fallback=player_buttons_defaults['blue_button_player_name'],
        )
        self.yellow_button_enabled: bool = player_buttons_config.getboolean(
            option='yellow_button_enabled', fallback=player_buttons_defaults['yellow_button_enabled'],
        )
        self.yellow_button_player_name: str = player_buttons_config.get(
            option='yellow_button_player_name', fallback=player_buttons_defaults['yellow_button_player_name'],
        )
        self.white_button_enabled: bool = player_buttons_config.getboolean(
            option='white_button_enabled', fallback=player_buttons_defaults['white_button_enabled'],
        )
        self.white_button_player_name: str = player_buttons_config.get(
            option='white_button_player_name', fallback=player_buttons_defaults['white_button_player_name'],
        )
        self.black_button_enabled: bool = player_buttons_config.getboolean(
            option='black_button_enabled', fallback=player_buttons_defaults['black_button_enabled'],
        )
        self.black_button_player_name: str = player_buttons_config.get(
            option='black_button_player_name', fallback=player_buttons_defaults['black_button_player_name'],
        )
        self.brain_ring_start_resume_key: str = moderator_buttons_config.get(
            option='brain_ring_start_resume_key',
            fallback=moderator_buttons_defaults['brain_ring_start_resume_key'],
        )
        self.brain_ring_reset_pause_key: str = moderator_buttons_config.get(
            option='brain_ring_reset_pause_key',
            fallback=moderator_buttons_defaults['brain_ring_reset_pause_key'],
        )
        self.brain_ring_reset_round_key: str = moderator_buttons_config.get(
            option='brain_ring_reset_round_key',
            fallback=moderator_buttons_defaults['brain_ring_reset_round_key'],
        )

    def update_config_file(self) -> None:
        """Обновляет файл `config.ini` данными, введенными пользователем."""
        config_attrs: List[str] = [attr for attr in self.__dict__ if not attr.startswith('__')]
        for section in DEFAULT_CONFIG.keys():
            for config_attr in config_attrs:
                if config_attr in DEFAULT_CONFIG[section].keys():
                    config.set(section=section, option=config_attr, value=str(getattr(self, config_attr)))

        self._write_config_file(CONFIG_FILE_PATH, config)

    def restore_default_config_file(self):
        """Восстанавливает файл `config.ini` данными, находящимися в словаре дефолтных настроек."""
        for section in DEFAULT_CONFIG.keys():
            for option, option_value in DEFAULT_CONFIG[section].items():
                config.set(section=section, option=option, value=str(option_value))

        self._write_config_file(CONFIG_FILE_PATH, config)

    @staticmethod
    def _write_config_file(config_file_path: Path, config: ConfigParser):
        with open(config_file_path, 'w') as config_file:
            config.write(config_file, space_around_delimiters=True)

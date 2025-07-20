from __future__ import annotations

from typing import TYPE_CHECKING

from config.enums import ColorSchemaEnum
from keyboard.enums import PlayerPressedKeyEnum


if TYPE_CHECKING:
    from ui.main_window import MainWindow


class Player():
    """Класс, описывающий игрока."""

    def __init__(self, obj: MainWindow, button_color: PlayerPressedKeyEnum) -> None:
        self.MAP_PLAYER_COLOR_QCOLOR = {
            PlayerPressedKeyEnum.RED.label: ColorSchemaEnum.RED,
            PlayerPressedKeyEnum.GREEN.label: ColorSchemaEnum.GREEN,
            PlayerPressedKeyEnum.BLUE.label: ColorSchemaEnum.BLUE,
            PlayerPressedKeyEnum.YELLOW.label: ColorSchemaEnum.YELLOW,
            PlayerPressedKeyEnum.WHITE.label: ColorSchemaEnum.WHITE,
            PlayerPressedKeyEnum.BLACK.label: ColorSchemaEnum.BLACK,
        }

        match button_color:
            case PlayerPressedKeyEnum.RED:
                self.name: str = obj.app_config.red_button_player_name
                self.is_enbled: bool = obj.app_config.red_button_enabled
                self.color: str = button_color.label
            case PlayerPressedKeyEnum.GREEN:
                self.name = obj.app_config.green_button_player_name
                self.is_enbled = obj.app_config.green_button_enabled
                self.color = button_color.label
            case PlayerPressedKeyEnum.YELLOW:
                self.name = obj.app_config.yellow_button_player_name
                self.is_enbled = obj.app_config.yellow_button_enabled
                self.color = button_color.label
            case PlayerPressedKeyEnum.BLUE:
                self.name = obj.app_config.blue_button_player_name
                self.is_enbled = obj.app_config.blue_button_enabled
                self.color = button_color.label
            case PlayerPressedKeyEnum.WHITE:
                self.name = obj.app_config.white_button_player_name
                self.is_enbled = obj.app_config.white_button_enabled
                self.color = button_color.label
            case PlayerPressedKeyEnum.BLACK:
                self.name = obj.app_config.black_button_player_name
                self.is_enbled = obj.app_config.black_button_enabled
                self.color = button_color.label
        self.is_blocked = False
        self.is_already_displayed_on_widget = False

    @property
    def icon_stroke_color(self) -> ColorSchemaEnum:
        """Указатель цвета, которым для данного игрока необходимо окрашивать обводку игровых значков."""
        if self.color == PlayerPressedKeyEnum.BLACK.label:
            return ColorSchemaEnum.WHITE
        return ColorSchemaEnum.BLACK

    @property
    def icon_background_color(self) -> ColorSchemaEnum:
        """Указатель цвета, которым для данного игрока необходимо окрашивать внутреннюю заливку игровых значков."""
        return self.MAP_PLAYER_COLOR_QCOLOR[self.color]

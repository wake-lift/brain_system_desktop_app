from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from keyboard.enums import PlayerPressedKeyEnum


if TYPE_CHECKING:
    from ui.main_window import MainWindow


class Player():
    """Класс, описывающий игрока."""

    def __init__(self, obj: MainWindow, button_color: PlayerPressedKeyEnum) -> None:
        self.MAP_PLAYER_COLOR_QCOLOR = {
            PlayerPressedKeyEnum.RED.label: Qt.GlobalColor.red,
            PlayerPressedKeyEnum.GREEN.label: Qt.GlobalColor.green,
            PlayerPressedKeyEnum.BLUE.label: Qt.GlobalColor.blue,
            PlayerPressedKeyEnum.YELLOW.label: Qt.GlobalColor.yellow,
            PlayerPressedKeyEnum.WHITE.label: Qt.GlobalColor.white,
            PlayerPressedKeyEnum.BLACK.label: Qt.GlobalColor.black,
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
    def icon_stroke_color(self) -> Qt.GlobalColor:
        """Указатель цвета, которым для данного игрока необходимо окрашивать обводку игровых значков."""
        if self.color == PlayerPressedKeyEnum.BLACK.label:
            return Qt.GlobalColor.white
        return Qt.GlobalColor.black

    @property
    def icon_background_color(self) -> Qt.GlobalColor:
        """Указатель цвета, которым для данного игрока необходимо окрашивать внутреннюю заливку игровых значков."""
        return self.MAP_PLAYER_COLOR_QCOLOR[self.color]

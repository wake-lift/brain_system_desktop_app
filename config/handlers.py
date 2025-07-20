from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMessageBox

from config.config import AppConfig
from config.enums import GameTypeEnum
from core.timer import CustomTimer
from ui.brain_ring_game_window import BrainRingGameWindow
from ui.www_game_window import WWWGameWindow


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def choose_brain_ring_radio_button_handler(obj: MainWindow):
    """Обработчик нажатия на радио-кнопку "брейн-ринг"."""
    if obj.choose_brain_ring_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.BRAIN_RING.value
    obj._setup_game()


def choose_www_radio_button_handler(obj: MainWindow):
    """Обработчик нажатия на радио-кнопку "чгк"."""
    if obj.choose_www_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.WWW.value
    obj._setup_game()


def choose_erudite_radio_button_handler(obj: MainWindow):
    """Обработчик нажатия на радио-кнопку "эрудитка"."""
    if obj.choose_erudite_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.ERUDITE.value
    obj._setup_game()


def brain_ring_round_duration_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени раунда (брейн-ринг)."""
    obj.app_config.brain_ring_round_time = obj.brain_ring_round_duration_spin_box.value()


def erudite_round_duration_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени раунда (эрудитка)."""
    obj.app_config.erudite_round_time = obj.erudite_round_duration_spin_box.value()


def www_regular_time_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени стандартного раунда (чгк)."""
    obj.app_config.www_regular_time = obj.www_regular_time_spin_box.value()


def www_blitz_time_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени блиц-раунда (чгк)."""
    obj.app_config.www_blitz_time = obj.www_blitz_time_spin_box.value()


def www_super_blitz_time_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени суперблиц-раунда (чгк)."""
    obj.app_config.www_super_blitz_time = obj.www_super_blitz_time_spin_box.value()


def www_time_to_provide_answers_spin_box_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик времени, отводящегося на сбор ответов команд (чгк)."""
    obj.app_config.www_time_to_provide_answers = obj.www_time_to_provide_answers_spin_box.value()


def red_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с красной кнопкой."""
    if checkbox_state == 0:
        obj.app_config.red_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.red_button_enabled = True


def green_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с зеленой кнопкой."""
    if checkbox_state == 0:
        obj.app_config.green_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.green_button_enabled = True


def blue_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с синей кнопкой."""
    if checkbox_state == 0:
        obj.app_config.blue_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.blue_button_enabled = True


def yellow_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с желтой кнопкой."""
    if checkbox_state == 0:
        obj.app_config.yellow_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.yellow_button_enabled = True


def white_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с белой кнопкой."""
    if checkbox_state == 0:
        obj.app_config.white_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.white_button_enabled = True


def black_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    """Обработчик чек-бокса активации игрока с черной кнопкой."""
    if checkbox_state == 0:
        obj.app_config.black_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.black_button_enabled = True


def red_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с красной кнопкой."""
    obj.app_config.red_button_player_name = obj.red_player_set_team_name_line_edit.text()


def green_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с зеленой кнопкой."""
    obj.app_config.green_button_player_name = obj.green_player_set_team_name_line_edit.text()


def blue_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с синей кнопкой."""
    obj.app_config.blue_button_player_name = obj.blue_player_set_team_name_line_edit.text()


def yellow_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с желтой кнопкой."""
    obj.app_config.yellow_button_player_name = obj.yellow_player_set_team_name_line_edit.text()


def white_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с белой кнопкой."""
    obj.app_config.white_button_player_name = obj.white_player_set_team_name_line_edit.text()


def black_player_set_team_name_line_edit_handler(obj: MainWindow):
    """Обработчик ввода значения в задатчик названия команды с черной кнопкой."""
    obj.app_config.black_button_player_name = obj.black_player_set_team_name_line_edit.text()


def save_settings_button_handler(obj: MainWindow):
    """Обработчик нажатия на кнопку сохранения настроек."""
    acknowledge_box = QMessageBox()
    acknowledge_box.setWindowTitle('Save settings')
    try:
        obj.app_config.update_config_file()
    except Exception:
        acknowledge_box.setText('Error occurred while trying to save settings!')
        acknowledge_box.setIcon(QMessageBox.Icon.Critical)
        acknowledge_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        acknowledge_box.exec()
    else:
        acknowledge_box.setText('Changes successfully saved')
        acknowledge_box.setIcon(QMessageBox.Icon.Information)
        acknowledge_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        acknowledge_box.exec()
        _reinitialize_app_data(obj)


def reset_settings_button_handler(obj: MainWindow):
    """Обработчик нажатия на кнопку сброса настроек."""
    acknowledge_box = QMessageBox()
    acknowledge_box.setWindowTitle('Reset settings')

    confirm_box_reply = QMessageBox.question(
        obj,
        'Reset settings',
        'This will reset all settings to defaults. Are you sure?',
        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        QMessageBox.StandardButton.Cancel,
    )
    if confirm_box_reply == QMessageBox.StandardButton.Cancel:
        return

    try:
        obj.app_config.restore_default_config_file()
    except Exception:
        acknowledge_box.setText('Error occurred while trying to reset settings!')
        acknowledge_box.setIcon(QMessageBox.Icon.Critical)
        acknowledge_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        acknowledge_box.exec()
    else:
        acknowledge_box.setText('Successfully reset settings to their defaults')
        acknowledge_box.setIcon(QMessageBox.Icon.Information)
        acknowledge_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        acknowledge_box.exec()
        _reinitialize_app_data(obj)


def _reinitialize_app_data(obj: MainWindow):
    """Заново инициализирует виджеты и игровые окна при обновлении/сбросе игровых настроек."""
    obj.app_config = AppConfig()
    obj._populate_settings_widgets()
    obj.brain_ring_timer = CustomTimer(initial_time=obj.app_config.brain_ring_round_time)
    obj.www_timer = CustomTimer(initial_time=obj.app_config.www_regular_time, precision=100)
    obj.erudite_timer = CustomTimer(initial_time=obj.app_config.erudite_round_time)
    obj.main_window_brain_info_timer_widget_vertical_layout.removeWidget(obj.main_window_brain_info_timer_label)
    obj.main_window_www_timer_widget_vertical_layout.removeWidget(obj.main_window_www_timer_label)
    obj.main_window_erudite_info_timer_widget_vertical_layout.removeWidget(obj.main_window_erudite_info_timer_label)
    obj._setup_game_widgets()
    obj.clear_brain_ring_info_labels()
    obj.clear_erudite_info_labels()
    obj.reset_all_enabled_players_widget_display()
    obj.clear_layout(obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout)
    obj.clear_layout(obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout)
    obj._setup_main_window_moderator_controls()
    obj._setup_game()
    obj.MAP_BUTTONS_TO_ENABLED_PLAYERS = obj._setup_players()
    obj.enabled_players = list(obj.MAP_BUTTONS_TO_ENABLED_PLAYERS.values())

    # закрываем и создаем заново игровые окна
    obj.brain_ring_game_window.close()
    obj.brain_ring_game_window.deleteLater()
    obj.brain_ring_game_window = None
    obj.open_brain_ring_window_button.clicked.disconnect()
    obj.brain_ring_game_window = BrainRingGameWindow(obj)

    obj.www_game_window.close()
    obj.www_game_window.deleteLater()
    obj.www_game_window = None
    obj.open_www_window_button.clicked.disconnect()
    obj.www_game_window = WWWGameWindow(obj)

    obj._setup_game_windows()

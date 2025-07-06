from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMessageBox

from config.config import AppConfig
from config.enums import GameTypeEnum
from core.timer import CustomTimer
from game_modes.what_where_when.game import WWWGame
from game_modes.what_where_when.handlers import set_www_game_info_label_text
from ui.widgets.brain_ring_moderator_game_widget import BrainRingModeratorGameWidget
from ui.widgets.erudite_moderator_game_widget import EruditeModeratorGameWidget
from ui.widgets.www_moderator_game_widget import WWWModeratorGameWidget


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def choose_brain_ring_radio_button_handler(obj: MainWindow):
    if obj.choose_brain_ring_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.BRAIN_RING.value
    obj._setup_game()


def choose_www_radio_button_handler(obj: MainWindow):
    if obj.choose_www_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.WWW.value
    obj._setup_game()


def choose_erudite_radio_button_handler(obj: MainWindow):
    if obj.choose_erudite_radio_button.isChecked():
        obj.app_config.game_type = GameTypeEnum.ERUDITE.value
    obj._setup_game()


def brain_ring_round_duration_spin_box_handler(obj: MainWindow):
    obj.app_config.brain_ring_round_time = obj.brain_ring_round_duration_spin_box.value()


def erudite_round_duration_spin_box_handler(obj: MainWindow):
    obj.app_config.erudite_round_time = obj.erudite_round_duration_spin_box.value()


def www_regular_time_spin_box_handler(obj: MainWindow):
    obj.app_config.www_regular_time = obj.www_regular_time_spin_box.value()


def www_blitz_time_spin_box_handler(obj: MainWindow):
    obj.app_config.www_blitz_time = obj.www_blitz_time_spin_box.value()


def www_super_blitz_time_spin_box_handler(obj: MainWindow):
    obj.app_config.www_super_blitz_time = obj.www_super_blitz_time_spin_box.value()


def www_time_to_provide_answers_spin_box_handler(obj: MainWindow):
    obj.app_config.www_time_to_provide_answers = obj.www_time_to_provide_answers_spin_box.value()


def red_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.red_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.red_button_enabled = True


def green_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.green_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.green_button_enabled = True


def blue_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.blue_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.blue_button_enabled = True


def yellow_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.yellow_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.yellow_button_enabled = True


def white_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.white_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.white_button_enabled = True


def black_player_check_box_handler(obj: MainWindow, checkbox_state: int):
    if checkbox_state == 0:
        obj.app_config.black_button_enabled = False
    elif checkbox_state == 2:
        obj.app_config.black_button_enabled = True


def red_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.red_button_player_name = obj.red_player_set_team_name_line_edit.text()


def green_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.green_button_player_name = obj.green_player_set_team_name_line_edit.text()


def blue_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.blue_button_player_name = obj.blue_player_set_team_name_line_edit.text()


def yellow_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.yellow_button_player_name = obj.yellow_player_set_team_name_line_edit.text()


def white_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.white_button_player_name = obj.white_player_set_team_name_line_edit.text()


def black_player_set_team_name_line_edit_handler(obj: MainWindow):
    obj.app_config.black_button_player_name = obj.black_player_set_team_name_line_edit.text()


def save_settings_button_handler(obj: MainWindow):
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
    obj.app_config = AppConfig()
    obj._populate_settings_widgets()
    obj.brain_ring_timer = CustomTimer(initial_time=obj.app_config.brain_ring_round_time)
    obj.www_timer = CustomTimer(initial_time=obj.app_config.www_regular_time, precision=100)
    obj.erudite_timer = CustomTimer(initial_time=obj.app_config.erudite_round_time)
    obj.main_window_brain_info_timer_widget_vertical_layout.removeWidget(obj.main_window_brain_info_timer_label)
    obj.main_window_brain_info_timer_label = BrainRingModeratorGameWidget(
        parent=obj.brain_ring_game_display_tab,
        timer=obj.brain_ring_timer,
        audio_player=obj.audio_player,
        audio_output=obj.audio_output,
    )
    obj.main_window_brain_info_timer_widget_vertical_layout.addWidget(obj.main_window_brain_info_timer_label)
    obj.main_window_www_timer_widget_vertical_layout.removeWidget(obj.main_window_www_timer_label)
    obj.main_window_www_timer_label = WWWModeratorGameWidget(
        parent=obj.brain_ring_game_display_tab,
        timer=obj.www_timer,
        audio_player=obj.audio_player,
        audio_output=obj.audio_output,
    )
    obj.main_window_www_timer_widget_vertical_layout.addWidget(obj.main_window_www_timer_label)
    obj.main_window_erudite_info_timer_widget_vertical_layout.removeWidget(obj.main_window_erudite_info_timer_label)
    obj.main_window_erudite_info_timer_label = EruditeModeratorGameWidget(
        parent=obj.erudite_game_display_tab,
        timer=obj.erudite_timer,
        audio_player=obj.audio_player,
        audio_output=obj.audio_output,
    )
    obj.main_window_erudite_info_timer_widget_vertical_layout.addWidget(obj.main_window_erudite_info_timer_label)
    obj.clear_brain_ring_info_labels()
    obj.clear_erudite_info_labels()
    obj.reset_all_enabled_players_widget_display()
    obj.clear_layout(obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout)
    obj.clear_layout(obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout)
    obj._setup_main_window_moderator_controls()
    if isinstance(obj.current_game, WWWGame):
        set_www_game_info_label_text(obj)
    else:
        obj.main_window_www_game_info_label.setText('')
    obj._setup_game()
    obj.MAP_BUTTONS_TO_ENABLED_PLAYERS = obj._setup_players()
    obj.enabled_players = list(obj.MAP_BUTTONS_TO_ENABLED_PLAYERS.values())

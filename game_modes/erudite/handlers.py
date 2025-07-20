from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTime
from PyQt6.QtGui import QColor

from config.enums import GameTypeEnum, SoundFileEnum
from game_modes.erudite.enums import EruditeGameStatusEnum
from game_modes.erudite.game import EruditeGame
from game_modes.player import Player
from ui.widgets.icon_widgets import CrossSvgWidget


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def erudite_moderator_start_resume_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СТАРТ/ПРОДОЛЖИТЬ" на панели управления (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    if obj.current_game.status == EruditeGameStatusEnum.READY_TO_START_COUNTDOWN:
        if obj.erudite_timer.is_paused:
            obj.erudite_timer.resume()
        else:
            obj.erudite_timer.start()
        obj.current_game.status = EruditeGameStatusEnum.COUNTDOWN_STARTED
        obj.moderator_erudite_game_status_label.setText(f'{EruditeGameStatusEnum.COUNTDOWN_STARTED.value}')


def erudite_moderator_reset_pause_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СБРОС ПАУЗЫ" на панели управления (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    if obj.current_game.status == EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED:
        obj.current_game.status = EruditeGameStatusEnum.READY_TO_START_COUNTDOWN
        obj.moderator_erudite_game_status_label.setText(f'{EruditeGameStatusEnum.READY_TO_START_COUNTDOWN.value}')
        obj.clear_erudite_info_labels()
        obj.reset_all_enabled_players_widget_display()


def erudite_moderator_reset_round_push_button_handler(obj: MainWindow):
    """Обработчик нажатия кнопки ведущего СБРОС РАУНДА" на панели управления (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    obj.erudite_timer.reset()
    obj.reset_all_enabled_players()
    obj.current_game.status = EruditeGameStatusEnum.READY_TO_START_COUNTDOWN
    obj.moderator_erudite_game_status_label.setText(f'{EruditeGameStatusEnum.READY_TO_START_COUNTDOWN.value}')
    obj.clear_erudite_info_labels()
    obj.clear_layout(obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout)


def erudite_player_key_press_handler(obj: MainWindow, player: Player):
    """Обработчик нажатия кнопки ведущего "СБРОС ПАУЗЫ" на панели управления (эрудитка)."""
    if any([player.is_blocked, not player.is_enbled, not isinstance(obj.current_game, EruditeGame)]):
        return
    if obj.current_game.status == EruditeGameStatusEnum.COUNTDOWN_STARTED:
        # Обработка логики для игрока, который первым нажал кнопку и имеет право дать ответ
        player.is_blocked = True
        remaining_time = obj.erudite_timer.pause()
        obj.current_game.first_button_pressed_time = QTime.currentTime()
        obj.play_sound_file(SoundFileEnum.BRAIN_PLAYER_BUTTON_PRESSED)
        obj.current_game.status = EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED
        obj.moderator_erudite_game_status_label.setText(
            f'{EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED.value}: {player.name}',
        )
        obj.set_erudite_info_label(player=player, game_status=obj.current_game.status, remaining_time=remaining_time)
        obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout.addWidget(
            CrossSvgWidget(
                background_color=QColor(player.icon_background_color), stroke_color=QColor(player.icon_stroke_color),
            ),
        )

    elif obj.current_game.status == EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED:
        # Обработка логики для игроков, которые нажали кнопку, но не были первыми
        if obj.current_game.first_button_pressed_time is not None:
            if not player.is_already_displayed_on_widget:
                current_time = QTime.currentTime()
                diff_time = round((obj.current_game.first_button_pressed_time.msecsTo(current_time) / 1000.0), 3)
                obj.set_erudite_info_label(player=player, game_status=obj.current_game.status, diff_time=diff_time)
                player.is_already_displayed_on_widget = True


def erudite_timer_run_out_event_handler(obj: MainWindow) -> None:
    """Обработчик события истечения времени таймера (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    obj.current_game.status = EruditeGameStatusEnum.TIME_IS_UP
    obj.block_all_enabled_players()
    obj.reset_all_enabled_players_widget_display()
    obj.moderator_erudite_game_status_label.setText(f'{EruditeGameStatusEnum.TIME_IS_UP.value}')

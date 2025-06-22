from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTime
from PyQt6.QtGui import QColor

from config.enums import GameTypeEnum, SoundFilesEnum
from core.blocked_player_indicator import BlockedPlayerIndicatorWidget
from game_modes.player import Player
from game_modes.brain_ring.enums import BrainRingGameStatusEnum


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def brain_ring_moderator_start_resume_push_button_handler(obj: MainWindow):
    if obj.game_type != GameTypeEnum.BRAIN_RING:
        return
    if obj.current_game.status == BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN:
        if obj.brain_ring_timer.is_paused:
            obj.brain_ring_timer.resume()
        else:
            obj.brain_ring_timer.start()
        obj.current_game.status = BrainRingGameStatusEnum.COUNTDOWN_STARTED
        obj.moderator_game_status_label.setText(f'{BrainRingGameStatusEnum.COUNTDOWN_STARTED.value}')


def brain_ring_moderator_reset_pause_push_button_handler(obj: MainWindow):
    if obj.game_type != GameTypeEnum.BRAIN_RING:
        return
    if obj.current_game.status in [BrainRingGameStatusEnum.FALSE_START, BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED]:
        obj.current_game.status = BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN
        obj.current_game.is_false_start_active = False
        obj.moderator_game_status_label.setText(
            f'{BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN.value}',
        )
        obj.clear_brain_ring_info_labels()


def brain_ring_moderator_reset_round_push_button_handler(obj: MainWindow):
    if obj.game_type != GameTypeEnum.BRAIN_RING:
        return
    obj.brain_ring_timer.reset()
    obj.reset_all_enabled_players()
    obj.current_game.is_false_start_active = False
    obj.current_game.status = BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN
    obj.moderator_game_status_label.setText(f'{BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN.value}')
    obj.clear_brain_ring_info_labels()
    obj.clear_layout(obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout)


def brain_ring_player_key_press_handler(obj: MainWindow, player: Player):
    if any([player.is_blocked, not player.is_enbled]):
        return
    if obj.current_game.status == BrainRingGameStatusEnum.COUNTDOWN_STARTED:
        # player was first who pushed the button to give an answer
        player.is_blocked = True
        remaining_time = obj.brain_ring_timer.pause()
        obj.current_game.first_button_pressed_time = QTime.currentTime()
        obj.play_sound_file(SoundFilesEnum.BRAIN_PLAYER_BUTTON_PRESSED)
        obj.current_game.status = BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED
        obj.moderator_game_status_label.setText(
            f'{BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED.value}: {player.name}',
        )
        obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status, remaining_time=remaining_time)
        obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout.addWidget(
            BlockedPlayerIndicatorWidget(background_color=QColor(player.MAP_PLAYER_COLOR_QCOLOR[player.color])),
        )

    elif obj.current_game.status == BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED:
        # player was not first who pushed the button to give an answer
        if obj.current_game.first_button_pressed_time is not None:
            current_time = QTime.currentTime()
            diff_time = round((obj.current_game.first_button_pressed_time.msecsTo(current_time) / 1000.0), 3)
            obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status, diff_time=diff_time)

    elif all([
            obj.current_game.status == BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN,
            not obj.current_game.is_false_start_active,
    ]):
        # player made a false start
        obj.current_game.is_false_start_active = True
        player.is_blocked = True
        obj.play_sound_file(SoundFilesEnum.BRAIN_PLAYER_FALSE_START)
        obj.current_game.status = BrainRingGameStatusEnum.FALSE_START
        obj.moderator_game_status_label.setText(f'{BrainRingGameStatusEnum.FALSE_START.value}: {player.name}')
        obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status)
        obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout.addWidget(
            BlockedPlayerIndicatorWidget(background_color=QColor(player.MAP_PLAYER_COLOR_QCOLOR[player.color])),
        )

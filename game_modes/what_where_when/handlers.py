from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QColor

from config.enums import GameTypeEnum, SoundFilesEnum
from core.timer import CustomTimer
from game_modes.what_where_when.enums import (
    WWWBlitzQuestionCounter,
    WWWGameStatusEnum,
    WWWRoundModeEnum,
    WWWSuperBlitzQuestionCounter,
)
from game_modes.what_where_when.game import WWWGame
from ui.widgets.www_moderator_game_widget import WWWModeratorGameWidget


if TYPE_CHECKING:
    from game_modes.player import Player
    from ui.main_window import MainWindow


def www_choose_regular_question_radio_button_handler(obj: MainWindow) -> None:
    initialize_www_timer(obj, initial_time=obj.app_config.www_regular_time)

    initialize_main_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.REGULAR
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = None
        obj.current_game.current_super_blitz_question = None
        set_www_game_info_label_text(obj)


def www_choose_blitz_radio_button_handler(obj: MainWindow) -> None:
    initialize_www_timer(obj, initial_time=obj.app_config.www_blitz_time)
    initialize_main_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.BLITZ
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = WWWBlitzQuestionCounter.FIRST
        obj.current_game.current_super_blitz_question = None
        set_www_game_info_label_text(obj)


def www_choose_super_blitz_radio_button_handler(obj: MainWindow) -> None:
    initialize_www_timer(obj, initial_time=obj.app_config.www_super_blitz_time)
    initialize_main_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.SUPER_BLITZ
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = None
        obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
        set_www_game_info_label_text(obj)


def www_time_to_provide_answers_check_box_handler(obj: MainWindow, checkbox_state: int) -> None:
    if not isinstance(obj.current_game, WWWGame):
        return
    if checkbox_state == 0:
        obj.current_game.enable_time_to_provide_answers = False
    elif checkbox_state == 2:
        obj.current_game.enable_time_to_provide_answers = True


def www_moderator_start_resume_push_button_handler(obj: MainWindow) -> None:
    if obj.game_type != GameTypeEnum.WWW or not isinstance(obj.current_game, WWWGame):
        return
    if obj.current_game.status == WWWGameStatusEnum.READY:
        obj.www_timer.start()
        obj.current_game.status = WWWGameStatusEnum.COUNTDOWN_STARTED


def www_moderator_reset_push_button_handler(obj: MainWindow) -> None:
    if obj.game_type != GameTypeEnum.WWW or not isinstance(obj.current_game, WWWGame):
        return
    obj.www_timer.reset()
    match obj.current_game.round_mode:
        case WWWRoundModeEnum.REGULAR:
            obj.current_game.current_blitz_question = None
            obj.current_game.current_super_blitz_question = None
            obj.main_window_www_game_info_label.setText(f'{obj.current_game.round_mode.label}')
            initialize_www_timer(obj, initial_time=obj.app_config.www_regular_time)
            initialize_main_window_www_timer_widget(obj)
        case WWWRoundModeEnum.BLITZ:
            obj.current_game.current_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
            obj.current_game.current_super_blitz_question = None
            obj.main_window_www_game_info_label.setText(
                f'{obj.current_game.round_mode.label}: {obj.current_game.current_blitz_question.value}'
            )
            initialize_www_timer(obj, initial_time=obj.app_config.www_blitz_time)
            initialize_main_window_www_timer_widget(obj)
        case WWWRoundModeEnum.SUPER_BLITZ:
            obj.current_game.current_blitz_question = None
            obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
            obj.main_window_www_game_info_label.setText(
                f'{obj.current_game.round_mode.label}: {obj.current_game.current_super_blitz_question.value}'
            )
            initialize_www_timer(obj, initial_time=obj.app_config.www_super_blitz_time)
            initialize_main_window_www_timer_widget(obj)
    obj.current_game.status = WWWGameStatusEnum.READY


def www_player_key_press_handler(obj: MainWindow, player: Player) -> None:
    pass


def set_www_game_info_label_text(obj: MainWindow) -> None:
    if not isinstance(obj.current_game, WWWGame):
        return
    if obj.current_game.round_mode == WWWRoundModeEnum.REGULAR:
        obj.main_window_www_game_info_label.setText(obj.current_game.round_mode.label)
    elif obj.current_game.round_mode == WWWRoundModeEnum.BLITZ:
        obj.main_window_www_game_info_label.setText(
            f'{obj.current_game.round_mode.label}: {obj.current_game.current_blitz_question.value}'
        )
    elif obj.current_game.round_mode == WWWRoundModeEnum.SUPER_BLITZ:
        obj.main_window_www_game_info_label.setText(
            f'{obj.current_game.round_mode.label}: {obj.current_game.current_super_blitz_question.value}'
        )


def www_timer_start_event_handler(obj: MainWindow):
    pass


def www_timer_run_out_event_handler(obj: MainWindow) -> None:
    if all([
        obj.current_game.enable_time_to_provide_answers,
        obj.current_game.status != WWWGameStatusEnum.PROVIDE_ANSWERS_COUNTDOWN_STARTED and
        any([
            (
                obj.current_game.current_blitz_question == WWWBlitzQuestionCounter.SECOND or
                obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.THIRD
            ),
            (
                obj.current_game.current_super_blitz_question is None and
                obj.current_game.current_blitz_question is None
            ),
        ]),
    ]):
        run_timer_to_provide_answers(obj)
        return
    match obj.current_game.round_mode:
        case WWWRoundModeEnum.REGULAR:
            play_sound_in_www_handlers(obj, sound=SoundFilesEnum.TIMER_START_STOP)
            www_moderator_reset_push_button_handler(obj)
        case WWWRoundModeEnum.BLITZ:
            if obj.current_game.current_blitz_question == WWWBlitzQuestionCounter.SECOND:
                play_sound_in_www_handlers(obj, sound=SoundFilesEnum.TIMER_START_STOP)
                www_moderator_reset_push_button_handler(obj)
            else:
                obj.current_game.current_blitz_question = WWWBlitzQuestionCounter.SECOND
                obj.main_window_www_game_info_label.setText(
                    f'{obj.current_game.round_mode.label}: {obj.current_game.current_blitz_question.value}'
                )
                obj.current_game.status = WWWGameStatusEnum.READY
        case WWWRoundModeEnum.SUPER_BLITZ:
            if obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.THIRD:
                play_sound_in_www_handlers(obj, sound=SoundFilesEnum.TIMER_START_STOP)
                www_moderator_reset_push_button_handler(obj)
            elif obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.SECOND:
                obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.THIRD
                obj.main_window_www_game_info_label.setText(
                    f'{obj.current_game.round_mode.label}: {obj.current_game.current_super_blitz_question.value}'
                )
                obj.current_game.status = WWWGameStatusEnum.READY
            elif obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.FIRST:
                obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.SECOND
                obj.main_window_www_game_info_label.setText(
                    f'{obj.current_game.round_mode.label}: {obj.current_game.current_super_blitz_question.value}'
                )
                obj.current_game.status = WWWGameStatusEnum.READY


def www_timer_timer_reset_event_handler(obj: MainWindow):
    pass


def www_timer_timer_ten_seconds_left_handler(obj: MainWindow) -> None:
    if obj.current_game.round_mode == WWWRoundModeEnum.REGULAR:
        play_sound_in_www_handlers(obj, sound=SoundFilesEnum.TIMER_10_SEC_LEFT)
        obj.main_window_www_timer_label.set_font_color(QColor(210, 126, 0))


def run_timer_to_provide_answers(obj: MainWindow) -> None:
    obj.www_timer = CustomTimer(obj.app_config.www_time_to_provide_answers, precision=100)
    obj.www_timer.timer_to_provide_answers_run_out.connect(slot=lambda: www_timer_run_out_event_handler(obj))
    obj.www_timer.timer_reset.connect(slot=lambda: www_timer_timer_reset_event_handler(obj))
    initialize_main_window_www_timer_widget(obj)
    obj.current_game.status = WWWGameStatusEnum.PROVIDE_ANSWERS_COUNTDOWN_STARTED
    obj.main_window_www_game_info_label.setText(f'{obj.current_game.status.label}')
    obj.www_timer.start()
    obj.main_window_www_timer_label.set_font_color(QColor(191, 29, 2))


def initialize_www_timer(obj: MainWindow, initial_time: int, precision: int = 100) -> None:
    obj.www_timer = CustomTimer(initial_time=initial_time, precision=precision)
    obj.www_timer.timer_start.connect(slot=lambda: www_timer_start_event_handler(obj))
    obj.www_timer.timer_run_out.connect(slot=lambda: www_timer_run_out_event_handler(obj))
    obj.www_timer.timer_reset.connect(slot=lambda: www_timer_timer_reset_event_handler(obj))
    obj.www_timer.timer_ten_seconds_left.connect(slot=lambda: www_timer_timer_ten_seconds_left_handler(obj))


def initialize_main_window_www_timer_widget(obj: MainWindow) -> None:
    obj.main_window_www_timer_widget_vertical_layout.removeWidget(obj.main_window_www_timer_label)
    obj.main_window_www_timer_label = WWWModeratorGameWidget(
        parent=obj.brain_ring_game_display_tab,
        timer=obj.www_timer,
        audio_player=obj.audio_player,
        audio_output=obj.audio_output,
    )
    obj.main_window_www_timer_widget_vertical_layout.addWidget(obj.main_window_www_timer_label)


def play_sound_in_www_handlers(obj: MainWindow, sound: SoundFilesEnum) -> None:
    path_to_file = Path(__file__).absolute().parent.parent.parent / 'assets' / 'sounds' / sound.value
    obj.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
    obj.audio_player.setSource(obj.current_audio_file)
    obj.audio_player.play()

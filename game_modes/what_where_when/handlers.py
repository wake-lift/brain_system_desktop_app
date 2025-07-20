from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QColor

from config.enums import ColorSchemaEnum, GameTypeEnum, SoundFileEnum
from core.timer import CustomTimer
from game_modes.what_where_when.enums import (
    WWWBlitzQuestionCounter,
    WWWGameStatusEnum,
    WWWRoundModeEnum,
    WWWSuperBlitzQuestionCounter,
)
from game_modes.what_where_when.game import WWWGame
from ui.widgets.www_game_timer_widget import WWWGameTimerWidget
from ui.widgets.www_moderator_timer_widget import WwwModeratorTimerWidget


if TYPE_CHECKING:
    from game_modes.player import Player
    from ui.main_window import MainWindow


def www_choose_regular_question_radio_button_handler(obj: MainWindow) -> None:
    """Обработчик выбора чекбокса обычного раунда на панели управления (ЧГК)."""
    initialize_www_timer(obj, initial_time=obj.app_config.www_regular_time)
    initialize_main_window_www_timer_widget(obj)
    initialize_game_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.REGULAR
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = None
        obj.current_game.current_super_blitz_question = None
        set_www_round_status_info_text(obj)


def www_choose_blitz_radio_button_handler(obj: MainWindow) -> None:
    """Обработчик выбора чекбокса блиц-раунда на панели управления (ЧГК)."""
    initialize_www_timer(obj, initial_time=obj.app_config.www_blitz_time)
    initialize_main_window_www_timer_widget(obj)
    initialize_game_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.BLITZ
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = WWWBlitzQuestionCounter.FIRST
        obj.current_game.current_super_blitz_question = None
        set_www_round_status_info_text(obj)


def www_choose_super_blitz_radio_button_handler(obj: MainWindow) -> None:
    """Обработчик выбора чекбокса суперблиц-раунда на панели управления (ЧГК)."""
    initialize_www_timer(obj, initial_time=obj.app_config.www_super_blitz_time)
    initialize_main_window_www_timer_widget(obj)
    initialize_game_window_www_timer_widget(obj)
    if isinstance(obj.current_game, WWWGame):
        obj.current_game.round_mode = WWWRoundModeEnum.SUPER_BLITZ
        obj.current_game.status = WWWGameStatusEnum.READY
        obj.current_game.current_blitz_question = None
        obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
        set_www_round_status_info_text(obj)


def www_time_to_provide_answers_check_box_handler(obj: MainWindow, checkbox_state: int) -> None:
    """Обработчик выбора чекбокса включения/отключения доп. времени на сдачу ответов на панели управления (ЧГК)."""
    if not isinstance(obj.current_game, WWWGame):
        return
    if checkbox_state == 0:
        obj.current_game.enable_time_to_provide_answers = False
    elif checkbox_state == 2:
        obj.current_game.enable_time_to_provide_answers = True


def www_moderator_start_resume_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СТАРТ/ПРОДОЛЖИТЬ" на панели управления (ЧГК)."""
    if obj.game_type != GameTypeEnum.WWW or not isinstance(obj.current_game, WWWGame):
        return
    if obj.current_game.status == WWWGameStatusEnum.READY:
        obj.www_timer.start()
        obj.current_game.status = WWWGameStatusEnum.COUNTDOWN_STARTED


def www_moderator_reset_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СБРОС" на панели управления (ЧГК)."""
    if obj.game_type != GameTypeEnum.WWW or not isinstance(obj.current_game, WWWGame):
        return
    obj.www_timer.reset()
    match obj.current_game.round_mode:
        case WWWRoundModeEnum.REGULAR:
            obj.current_game.current_blitz_question = None
            obj.current_game.current_super_blitz_question = None
            round_info_text = f'{obj.current_game.round_mode.label}'
            initialize_www_timer(obj, initial_time=obj.app_config.www_regular_time)
        case WWWRoundModeEnum.BLITZ:
            obj.current_game.current_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
            obj.current_game.current_super_blitz_question = None
            round_info_text = f'{obj.current_game.round_mode.label}: {obj.current_game.current_blitz_question.value}'
            initialize_www_timer(obj, initial_time=obj.app_config.www_blitz_time)
        case WWWRoundModeEnum.SUPER_BLITZ:
            obj.current_game.current_blitz_question = None
            obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.FIRST
            round_info_text = (
                f'{obj.current_game.round_mode.label}: '
                f'{obj.current_game.current_super_blitz_question.value}'
            )
            initialize_www_timer(obj, initial_time=obj.app_config.www_super_blitz_time)
    initialize_main_window_www_timer_widget(obj)
    initialize_game_window_www_timer_widget(obj)
    obj.main_window_www_game_info_label.setText(round_info_text)
    obj.www_game_window.update_round_info_widget(text=round_info_text)
    obj.current_game.status = WWWGameStatusEnum.READY


def www_player_key_press_handler(obj: MainWindow, player: Player) -> None:
    """TODO: Обработчик нажатия кнопки игрока (ЧГК)."""
    pass


def set_www_round_status_info_text(obj: MainWindow) -> None:
    """Установка текста статуса раунда на информационной панели ведущего и на игровом окне (ЧГК)."""
    if not isinstance(obj.current_game, WWWGame):
        return
    if obj.current_game.round_mode == WWWRoundModeEnum.REGULAR:
        text = obj.current_game.round_mode.label
    elif obj.current_game.round_mode == WWWRoundModeEnum.BLITZ:
        text = f'{obj.current_game.round_mode.label}: {obj.current_game.current_blitz_question.value}'
    else:
        text = f'{obj.current_game.round_mode.label}: {obj.current_game.current_super_blitz_question.value}'
    obj.main_window_www_game_info_label.setText(text)
    obj.www_game_window.update_round_info_widget(text=text)


def www_timer_start_event_handler(obj: MainWindow):
    """Обработчик события старта таймера (ЧГК). В настоящее время нет необходимости в этой логике."""
    pass


def www_timer_run_out_event_handler(obj: MainWindow) -> None:
    """Обработчик события окончания таймера (ЧГК)."""
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
            play_sound_in_www_handlers(obj, sound=SoundFileEnum.TIMER_START_STOP)
            www_moderator_reset_push_button_handler(obj)
            round_info_text = f'{obj.current_game.round_mode.label}'
        case WWWRoundModeEnum.BLITZ:
            if obj.current_game.current_blitz_question == WWWBlitzQuestionCounter.SECOND:
                play_sound_in_www_handlers(obj, sound=SoundFileEnum.TIMER_START_STOP)
                www_moderator_reset_push_button_handler(obj)
            else:
                obj.current_game.current_blitz_question = WWWBlitzQuestionCounter.SECOND
                obj.current_game.status = WWWGameStatusEnum.READY
            round_info_text = (
                f'{obj.current_game.round_mode.label}: '
                f'{obj.current_game.current_blitz_question.value}'
            )
        case WWWRoundModeEnum.SUPER_BLITZ:
            if obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.THIRD:
                play_sound_in_www_handlers(obj, sound=SoundFileEnum.TIMER_START_STOP)
                www_moderator_reset_push_button_handler(obj)
            elif obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.SECOND:
                obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.THIRD
                obj.current_game.status = WWWGameStatusEnum.READY
            elif obj.current_game.current_super_blitz_question == WWWSuperBlitzQuestionCounter.FIRST:
                obj.current_game.current_super_blitz_question = WWWSuperBlitzQuestionCounter.SECOND
                obj.current_game.status = WWWGameStatusEnum.READY
            round_info_text = (
                f'{obj.current_game.round_mode.label}: '
                f'{obj.current_game.current_super_blitz_question.value}'
            )

    obj.main_window_www_game_info_label.setText(round_info_text)
    obj.www_game_window.update_round_info_widget(text=round_info_text)


def www_timer_timer_reset_event_handler(obj: MainWindow):
    """Обработчик события сброса таймера (ЧГК). В настоящее время нет необходимости в этой логике."""
    pass


def www_timer_timer_ten_seconds_left_handler(obj: MainWindow) -> None:
    """Обработчик события: на таймере осталось 10 секунд (ЧГК)."""
    if obj.current_game.round_mode == WWWRoundModeEnum.REGULAR:
        play_sound_in_www_handlers(obj, sound=SoundFileEnum.TIMER_10_SEC_LEFT)
        obj.main_window_www_timer_label.set_font_color(QColor(ColorSchemaEnum.WWW_MODERATOR_TIMER_10_SEC_LEFT))
        obj.www_game_timer_widget.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_10_SEC_LEFT))


def run_timer_to_provide_answers(obj: MainWindow) -> None:
    """Запускает доп. таймер для сбора ответов игроков."""
    obj.www_timer = CustomTimer(obj.app_config.www_time_to_provide_answers, precision=100)
    obj.www_timer.timer_to_provide_answers_run_out.connect(slot=lambda: www_timer_run_out_event_handler(obj))
    obj.www_timer.timer_reset.connect(slot=lambda: www_timer_timer_reset_event_handler(obj))
    initialize_main_window_www_timer_widget(obj)
    initialize_game_window_www_timer_widget(obj)
    obj.current_game.status = WWWGameStatusEnum.PROVIDE_ANSWERS_COUNTDOWN_STARTED
    round_info_text = f'{obj.current_game.status.label}'
    obj.main_window_www_game_info_label.setText(round_info_text)
    obj.www_game_window.update_round_info_widget(text=round_info_text)
    obj.www_timer.start()
    obj.main_window_www_timer_label.set_font_color(QColor(ColorSchemaEnum.WWW_MODERATOR_TIMER_PROVIDE_ANSWERS))
    obj.www_game_timer_widget.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_PROVIDE_ANSWERS))


def initialize_www_timer(obj: MainWindow, initial_time: int, precision: int = 100) -> None:
    """Инициализирует ЧГК-таймер."""
    obj.www_timer = CustomTimer(initial_time=initial_time, precision=precision)
    obj.www_timer.timer_start.connect(slot=lambda: www_timer_start_event_handler(obj))
    obj.www_timer.timer_run_out.connect(slot=lambda: www_timer_run_out_event_handler(obj))
    obj.www_timer.timer_reset.connect(slot=lambda: www_timer_timer_reset_event_handler(obj))
    obj.www_timer.timer_ten_seconds_left.connect(slot=lambda: www_timer_timer_ten_seconds_left_handler(obj))


def initialize_main_window_www_timer_widget(obj: MainWindow) -> None:
    """Инициализирует виджет таймера на панели ведущего."""
    obj.main_window_www_timer_widget_vertical_layout.removeWidget(obj.main_window_www_timer_label)
    obj.main_window_www_timer_label = WwwModeratorTimerWidget(
        parent=obj.brain_ring_game_display_tab,
        timer=obj.www_timer,
        audio_player=obj.audio_player,
        audio_output=obj.audio_output,
    )
    obj.main_window_www_timer_widget_vertical_layout.addWidget(obj.main_window_www_timer_label)


def initialize_game_window_www_timer_widget(obj: MainWindow) -> None:
    """Инициализирует виджет таймера на игровом окне ЧГК."""
    obj.www_game_window.www_window_game_widget_horizontal_layout.removeWidget(obj.www_game_timer_widget)
    obj.www_game_timer_widget = WWWGameTimerWidget(obj.www_game_window, timer=obj.www_timer)
    obj.www_game_window.www_window_game_widget_horizontal_layout.addWidget(obj.www_game_timer_widget)


def play_sound_in_www_handlers(obj: MainWindow, sound: SoundFileEnum) -> None:
    """Воспроизводит звук в обработчиках событий (ЧГК)."""
    path_to_file = Path(__file__).absolute().parent.parent.parent / 'assets' / 'sounds' / sound.value
    obj.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
    obj.audio_player.setSource(obj.current_audio_file)
    obj.audio_player.play()

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTime, Qt
from PyQt6.QtGui import QColor

from config.enums import ColorSchemaEnum, GameTypeEnum, SoundFileEnum
from game_modes.erudite.enums import EruditeGameStatusEnum
from game_modes.erudite.game import EruditeGame
from ui.widgets.icon_widgets import CheckCircleSvgWidget, CircleSvgWidget, CrossSvgWidget


if TYPE_CHECKING:
    from game_modes.player import Player
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
        obj.moderator_erudite_game_status_label.setText(f'{obj.current_game.status.value}')


def erudite_moderator_reset_pause_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СБРОС ПАУЗЫ" на панели управления (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    if obj.current_game.status == EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED:
        obj.current_game.status = EruditeGameStatusEnum.READY_TO_START_COUNTDOWN
        obj.moderator_erudite_game_status_label.setText(f'{obj.current_game.status.value}')
        obj.clear_erudite_info_labels()
        obj.erudite_game_window.clear_all_player_info_horizontal_layouts()
        obj.reset_all_enabled_players_widget_display()
        # Находим на панели заблокированных игроков виджет игрока, давшего неправильный ответ,
        # и меняем его виджет на тот же, что у остальных
        layout = obj.erudite_game_window.erudite_game_window_blocked_players_indicator_widget_horizontal_layout
        for widget_item_number in range(layout.count()):
            widget_item = layout.itemAt(widget_item_number)
            if widget := widget_item.widget():
                if isinstance(widget, CheckCircleSvgWidget):
                    blocked_info_icon_widget = obj.erudite_game_window.build_colored_icon_widget(
                        widget_cls=CrossSvgWidget,
                        background_color=widget.background_color,
                        stroke_color=widget.stroke_color,
                    )
                    widget.deleteLater()
                    obj.erudite_game_window.add_widget_to_blocked_players_indicator_layout(blocked_info_icon_widget)


def erudite_moderator_reset_round_push_button_handler(obj: MainWindow):
    """Обработчик нажатия кнопки ведущего СБРОС РАУНДА" на панели управления (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    obj.erudite_timer.reset()
    obj.reset_all_enabled_players()
    obj.current_game.status = EruditeGameStatusEnum.READY_TO_START_COUNTDOWN
    obj.moderator_erudite_game_status_label.setText(f'{obj.current_game.status.value}')
    obj.clear_erudite_info_labels()
    obj.clear_layout(obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout)
    obj.erudite_game_window.clear_all_player_info_horizontal_layouts()
    obj.erudite_game_window.clear_blocked_players_indicator_layout()


def erudite_player_key_press_handler(obj: MainWindow, player: Player):
    """Обработчик нажатия кнопки игрока (эрудитка)."""
    if any([player.is_blocked, not player.is_enbled, not isinstance(obj.current_game, EruditeGame)]):
        return
    if obj.current_game.status in {
        EruditeGameStatusEnum.COUNTDOWN_STARTED, EruditeGameStatusEnum.READY_TO_START_COUNTDOWN
    }:
        _handle_erudite_player_who_gives_answer(obj=obj, player=player)
    elif obj.current_game.status == EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED:
        _handle_erudite_player_who_was_not_first_to_answer(obj=obj, player=player)


def erudite_timer_run_out_event_handler(obj: MainWindow) -> None:
    """Обработчик события истечения времени таймера (эрудитка)."""
    if obj.game_type != GameTypeEnum.ERUDITE or not isinstance(obj.current_game, EruditeGame):
        return
    obj.current_game.status = EruditeGameStatusEnum.TIME_IS_UP
    obj.moderator_erudite_game_status_label.setText(f'{obj.current_game.status.value}')
    obj.block_all_enabled_players()
    obj.reset_all_enabled_players_widget_display()


def _handle_erudite_player_who_gives_answer(obj: MainWindow, player: Player) -> None:
    """Обработка логики для игрока, который первым нажал кнопку и имеет право дать ответ."""
    player.is_blocked = True
    remaining_time: float | None = obj.erudite_timer.pause() if obj.erudite_timer.is_running else None
    obj.current_game.first_button_pressed_time = QTime.currentTime()
    obj.play_sound_file(SoundFileEnum.BRAIN_PLAYER_BUTTON_PRESSED)
    obj.current_game.status = EruditeGameStatusEnum.PLAYER_BUTTON_PRESSED
    obj.moderator_erudite_game_status_label.setText(f'{obj.current_game.status.value}: {player.name}')
    # добавляем виджет на панель ведущего с информацией об игроках
    obj.set_erudite_info_label(
        player=player,
        game_status=obj.current_game.status,
        remaining_time=obj.app_config.erudite_round_time if remaining_time is None else remaining_time,
    )
    obj.main_window_erudite_blocked_players_indicator_widget_horizontal_layout.addWidget(
        CrossSvgWidget(
            background_color=QColor(player.icon_background_color), stroke_color=QColor(player.icon_stroke_color),
        ),
    )
    # добавляем виджет на игровую панель с информацией об игроках
    icon_widget = obj.erudite_game_window.build_colored_icon_widget(
        widget_cls=CheckCircleSvgWidget,
        background_color=player.icon_background_color,
        stroke_color=player.icon_stroke_color,
    )
    player_name_label = obj.erudite_game_window.build_label_widget(
        text=f'{player.name}',
        color=ColorSchemaEnum.ERUDITE_PLAYER_NAME_LABEL,
        alignment=Qt.AlignmentFlag.AlignCenter,
        bold=True,
    )
    player_time_label = obj.erudite_game_window.build_label_widget(
        horizontal_stretch=30,
        text=f'{obj.app_config.erudite_round_time} sec' if remaining_time is None else f'{remaining_time} sec',
        color=ColorSchemaEnum.ERUDITE_PLAYER_TIME_LABEL,
        alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        bold=True,
    )
    obj.erudite_game_window.populate_player_info_horizontal_layout(
        layout=obj.erudite_game_window.first_unpopulated_player_info_layout,
        left_widget=icon_widget,
        central_widget=player_name_label,
        right_widget=player_time_label,
    )
    # добавляем виджет на игровую панель с информацией о заблокированных игроках
    blocked_info_icon_widget = obj.erudite_game_window.build_colored_icon_widget(
        widget_cls=CheckCircleSvgWidget,
        background_color=player.icon_background_color,
        stroke_color=player.icon_stroke_color,
    )
    obj.erudite_game_window.add_widget_to_blocked_players_indicator_layout(blocked_info_icon_widget)


def _handle_erudite_player_who_was_not_first_to_answer(obj: MainWindow, player: Player) -> None:
    """Обработка логики для игрока, который нажал кнопку, но не был первым, кто это сделал."""
    if obj.current_game.first_button_pressed_time is not None:
        if not player.is_already_displayed_on_widget:
            current_time = QTime.currentTime()
            diff_time = round((obj.current_game.first_button_pressed_time.msecsTo(current_time) / 1000.0), 3)
            # добавляем виджет на панель ведущего с информацией об игроках
            obj.set_erudite_info_label(player=player, game_status=obj.current_game.status, diff_time=diff_time)
            # добавляем виджет на игровую панель с информацией об игроках
            icon_widget = obj.erudite_game_window.build_colored_icon_widget(
                widget_cls=CircleSvgWidget,
                background_color=player.icon_background_color,
                stroke_color=player.icon_stroke_color,
            )
            player_name_label = obj.erudite_game_window.build_label_widget(
                text=f'{player.name}',
                color=ColorSchemaEnum.ERUDITE_NOT_FIRST_PLAYER_NAME_LABEL,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            player_time_label = obj.erudite_game_window.build_label_widget(
                horizontal_stretch=30,
                text=f'+ {diff_time} sec',
                color=ColorSchemaEnum.ERUDITE_NOT_FIRST_PLAYER_TIME_LABEL,
                alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            )
            obj.erudite_game_window.populate_player_info_horizontal_layout(
                layout=obj.erudite_game_window.first_unpopulated_player_info_layout,
                left_widget=icon_widget,
                central_widget=player_name_label,
                right_widget=player_time_label,
            )
            player.is_already_displayed_on_widget = True

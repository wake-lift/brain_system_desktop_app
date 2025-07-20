from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTime, Qt
from PyQt6.QtGui import QColor

from config.enums import ColorSchemaEnum, GameTypeEnum, SoundFileEnum
from game_modes.brain_ring.game import BrainRingGame
from game_modes.player import Player
from game_modes.brain_ring.enums import BrainRingGameStatusEnum
from ui.widgets.icon_widgets import CheckCircleSvgWidget, CircleSvgWidget, CrossSvgWidget


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def brain_ring_moderator_start_resume_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СТАРТ/ПРОДОЛЖИТЬ" на панели управления (брейн-ринг)."""
    if obj.game_type != GameTypeEnum.BRAIN_RING or not isinstance(obj.current_game, BrainRingGame):
        return
    if obj.current_game.status == BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN:
        if obj.brain_ring_timer.is_paused:
            obj.brain_ring_timer.resume()
        else:
            obj.brain_ring_timer.start()
        obj.brain_ring_game_window.activate_time_start_signal()
        obj.current_game.status = BrainRingGameStatusEnum.COUNTDOWN_STARTED
        obj.moderator_brain_game_status_label.setText(f'{BrainRingGameStatusEnum.COUNTDOWN_STARTED.value}')


def brain_ring_moderator_reset_pause_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СБРОС ПАУЗЫ" на панели управления (брейн-ринг)."""
    if obj.game_type != GameTypeEnum.BRAIN_RING or not isinstance(obj.current_game, BrainRingGame):
        return
    if obj.current_game.status in [BrainRingGameStatusEnum.FALSE_START, BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED]:
        obj.current_game.status = BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN
        obj.current_game.is_false_start_active = False
        obj.moderator_brain_game_status_label.setText(
            f'{BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN.value}',
        )
        obj.clear_brain_ring_info_labels()
        obj.brain_ring_game_window.clear_all_player_info_horizontal_layouts()
        obj.reset_all_enabled_players_widget_display()

        # Находим на панели заблокированных игроков виджет игрока, давшего неправильный ответ,
        # и меняем его виджет на тот же, что у остальных
        layout = obj.brain_ring_game_window.brain_game_window_blocked_players_indicator_widget_horizontal_layout
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if widget := item.widget():
                if isinstance(widget, CheckCircleSvgWidget):
                    blocked_info_icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
                        widget_cls=CrossSvgWidget,
                        background_color=widget.background_color,
                        stroke_color=widget.stroke_color,
                    )
                    widget.deleteLater()
                    obj.brain_ring_game_window.add_widget_to_blocked_players_indicator_layout(blocked_info_icon_widget)


def brain_ring_moderator_reset_round_push_button_handler(obj: MainWindow) -> None:
    """Обработчик нажатия кнопки ведущего "СБРОС РАУНДА" на панели управления (брейн-ринг)."""
    if obj.game_type != GameTypeEnum.BRAIN_RING or not isinstance(obj.current_game, BrainRingGame):
        return
    obj.brain_ring_timer.reset()
    obj.reset_all_enabled_players()
    obj.current_game.is_false_start_active = False
    obj.current_game.status = BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN
    obj.moderator_brain_game_status_label.setText(f'{BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN.value}')
    obj.clear_brain_ring_info_labels()
    obj.brain_ring_game_window.clear_all_player_info_horizontal_layouts()
    obj.brain_ring_game_window.clear_blocked_players_indicator_layout()
    obj.clear_layout(obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout)


def brain_ring_player_key_press_handler(obj: MainWindow, player: Player):
    """Обработчик нажатия кнопки игрока (брейн-ринг)."""
    if any([player.is_blocked, not player.is_enbled, not isinstance(obj.current_game, BrainRingGame)]):
        return
    if obj.current_game.status == BrainRingGameStatusEnum.COUNTDOWN_STARTED:
        # Обработка логики для игрока, который первым нажал кнопку и имеет право дать ответ
        obj.brain_ring_game_window.deactivate_time_start_signal()
        player.is_blocked = True
        remaining_time = obj.brain_ring_timer.pause()
        obj.current_game.first_button_pressed_time = QTime.currentTime()
        obj.play_sound_file(SoundFileEnum.BRAIN_PLAYER_BUTTON_PRESSED)
        obj.current_game.status = BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED
        obj.moderator_brain_game_status_label.setText(
            f'{BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED.value}: {player.name}',
        )

        # добавляет виджет на панель модератора с информацией об игроках
        obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status, remaining_time=remaining_time)

        # добавляет виджет на игровую панель с информацией об игроках
        icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
            widget_cls=CheckCircleSvgWidget,
            background_color=player.icon_background_color,
            stroke_color=player.icon_stroke_color,
        )
        player_name_label = obj.brain_ring_game_window.build_label_widget(
            text=f'{player.name}', color=ColorSchemaEnum.BRAIN_PLAYER_NAME_LABEL, bold=True,
        )
        player_time_label = obj.brain_ring_game_window.build_label_widget(
            horizontal_stretch=30,
            text=f'{remaining_time} sec',
            color=ColorSchemaEnum.BRAIN_PLAYER_TIME_LABEL,
            alignment=Qt.AlignmentFlag.AlignLeft,
            bold=True,
        )
        obj.brain_ring_game_window.populate_player_info_horizontal_layout(
            layout=obj.brain_ring_game_window.first_unpopulated_player_info_layout,
            left_widget=icon_widget,
            central_widget=player_name_label,
            right_widget=player_time_label,
        )

        # добавляет виджет на панель модератора с информацией о заблокированных игроках
        obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout.addWidget(
            CrossSvgWidget(
                background_color=QColor(player.icon_background_color), stroke_color=QColor(player.icon_stroke_color),
            ),
        )

        # добавляет виджет на игровую панель с информацией о заблокированных игроках
        blocked_info_icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
            widget_cls=CheckCircleSvgWidget,
            background_color=player.icon_background_color,
            stroke_color=player.icon_stroke_color,
        )
        obj.brain_ring_game_window.add_widget_to_blocked_players_indicator_layout(blocked_info_icon_widget)

    elif obj.current_game.status == BrainRingGameStatusEnum.PLAYER_BUTTON_PRESSED:
        # Обработка логики для игроков, которые нажали кнопку, но не были первыми
        if obj.current_game.first_button_pressed_time is not None:
            if not player.is_already_displayed_on_widget:
                current_time = QTime.currentTime()
                diff_time = round((obj.current_game.first_button_pressed_time.msecsTo(current_time) / 1000.0), 3)

                # добавляет виджет на панель модератора с информацией об игроках
                obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status, diff_time=diff_time)

                # добавляет виджет на игровую панель с информацией об игроках
                icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
                    widget_cls=CircleSvgWidget,
                    background_color=player.icon_background_color,
                    stroke_color=player.icon_stroke_color,
                )
                player_name_label = obj.brain_ring_game_window.build_label_widget(
                    text=f'{player.name}', color=ColorSchemaEnum.BRAIN_NOT_FIRST_PLAYER_NAME_LABEL
                )
                player_time_label = obj.brain_ring_game_window.build_label_widget(
                    horizontal_stretch=30,
                    text=f'+ {diff_time} sec',
                    color=ColorSchemaEnum.BRAIN_NOT_FIRST_PLAYER_TIME_LABEL,
                    alignment=Qt.AlignmentFlag.AlignLeft,
                )
                obj.brain_ring_game_window.populate_player_info_horizontal_layout(
                    layout=obj.brain_ring_game_window.first_unpopulated_player_info_layout,
                    left_widget=icon_widget,
                    central_widget=player_name_label,
                    right_widget=player_time_label,
                )

                player.is_already_displayed_on_widget = True

    elif all([
        obj.current_game.status == BrainRingGameStatusEnum.READY_TO_START_COUNTDOWN,
        not obj.current_game.is_false_start_active,
    ]):
        # Обработка логики для игрока, допустившего фальстарт
        obj.current_game.is_false_start_active = True
        player.is_blocked = True
        obj.play_sound_file(SoundFileEnum.BRAIN_PLAYER_FALSE_START)
        obj.current_game.status = BrainRingGameStatusEnum.FALSE_START
        obj.moderator_brain_game_status_label.setText(f'{BrainRingGameStatusEnum.FALSE_START.value}: {player.name}')

        # добавляет виджет на панель модератора с информацией об игроках
        obj.set_brain_ring_info_label(player=player, game_status=obj.current_game.status)

        # добавляет виджет на игровую панель с информацией об игроках
        icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
            widget_cls=CrossSvgWidget,
            background_color=player.icon_background_color,
            stroke_color=player.icon_stroke_color,
        )
        player_name_label = obj.brain_ring_game_window.build_label_widget(
            text=f'{player.name}', color=ColorSchemaEnum.BRAIN_PLAYER_NAME_LABEL, bold=True,
        )
        player_time_label = obj.brain_ring_game_window.build_label_widget(
            horizontal_stretch=30,
            text='False start',
            color=ColorSchemaEnum.BRAIN_PLAYER_TIME_LABEL,
            alignment=Qt.AlignmentFlag.AlignLeft,
            bold=True,
        )
        obj.brain_ring_game_window.populate_player_info_horizontal_layout(
            layout=obj.brain_ring_game_window.first_unpopulated_player_info_layout,
            left_widget=icon_widget,
            central_widget=player_name_label,
            right_widget=player_time_label,
        )

        # добавляет виджет на панель модератора с информацией о заблокированных игроках
        obj.main_window_brain_blocked_players_indicator_widget_horizontal_layout.addWidget(
            CrossSvgWidget(
                background_color=QColor(player.icon_background_color), stroke_color=QColor(player.icon_stroke_color),
            ),
        )

        # добавляет виджет на игровую панель с информацией о заблокированных игроках
        blocked_info_icon_widget = obj.brain_ring_game_window.build_colored_icon_widget(
            widget_cls=CrossSvgWidget,
            background_color=player.icon_background_color,
            stroke_color=player.icon_stroke_color,
        )
        obj.brain_ring_game_window.add_widget_to_blocked_players_indicator_layout(blocked_info_icon_widget)


def brain_timer_run_out_event_handler(obj: MainWindow) -> None:
    """Обработчик события истечения времени таймера (брейн-ринг)."""
    if obj.game_type != GameTypeEnum.BRAIN_RING or not isinstance(obj.current_game, BrainRingGame):
        return
    obj.brain_ring_game_window.deactivate_time_start_signal()
    obj.current_game.status = BrainRingGameStatusEnum.TIME_IS_UP
    obj.block_all_enabled_players()
    obj.reset_all_enabled_players_widget_display()
    obj.moderator_brain_game_status_label.setText(f'{BrainRingGameStatusEnum.TIME_IS_UP.value}')

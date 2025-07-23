from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QMediaPlayer

from config.enums import ColorSchemaEnum, SoundFileEnum
from core.widgets import TimerAndSoundBaseWidget


if TYPE_CHECKING:
    from PyQt6.QtMultimedia import QAudioOutput

    from core.timer import CustomTimer


class EruditeModeratorTimerWidget(TimerAndSoundBaseWidget):  # noqa: WPS214
    """Widget displayed on moderator's panel. Duplicates info on players main widget."""

    def __init__(
        self,
        parent,
        timer: CustomTimer,
        audio_player: QMediaPlayer,
        audio_output: QAudioOutput,
        font_size_ratio: float = 0.3,
    ):
        super().__init__(parent, timer, audio_player, audio_output)
        self.font_size_ratio = font_size_ratio  # отношение размера текста к размеру виджета
        self.set_font_color()
        self.last_timer_signal_indicator: int = -1

    def resizeEvent(self, event):
        """Переопределение стандартного метода, вызываемого автоматически при изменении размера окна."""
        super().resizeEvent(event)
        self.update_font_size()

    def update_font_size(self):
        """Обновление размера шрифта в соответствии с размером окна."""
        new_size = max(
            self.min_font_size,
            int(self.height() * self.font_size_ratio),
            int(self.width() * self.font_size_ratio),
        )
        font = self.time_label.font()
        font.setPixelSize(new_size)
        self.time_label.setFont(font)

    def update_display(self) -> None:
        """Обновление отображения таймера"""
        remaining_time_int = int(self.timer.remaining_time)
        if self.timer.is_run_out:
            self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_RUN_OUT))
            return
        if self.timer.remaining_time <= 5:
            self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_5_SEC_LEFT))
        self.time_label.setText(self.format_time(self.timer.remaining_time))
        if all([
                remaining_time_int in [0, 1, 2, 3, 4],
                remaining_time_int != self.last_timer_signal_indicator,
                self.audio_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState,
        ]):
            self.last_timer_signal_indicator = remaining_time_int
            self.play_sound(SoundFileEnum.BRAIN_TIMER_CLOSE_TO_END)

    def handle_timer_start(self) -> None:
        """Обработчик начала отсчета таймера"""
        self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_INITIAL))
        if self.timer.remaining_time <= 5:
            self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_5_SEC_LEFT))

    def handle_timer_run_out(self):
        """Обработчик окончания времени"""
        self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_RUN_OUT))
        self.time_label.setText(self.format_time(0))
        self.play_sound(SoundFileEnum.BRAIN_TIMER_START_END)
        self.last_timer_signal_indicator = -1

    def handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        self.set_font_color(QColor(ColorSchemaEnum.ERUDITE_MODERATOR_TIMER_INITIAL))
        self.time_label.setText(self.format_time(self.timer.remaining_time))

    def format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        if self.timer.remaining_time > 5:
            return f'{seconds:.0f}'
        return f'{seconds:.1f}'

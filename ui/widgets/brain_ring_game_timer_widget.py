from PyQt6.QtGui import QColor, QPalette

from core.timer import CustomTimer
from ui.widgets.base_widgets import TimerAndSoundBaseWidget


class BrainRingGameTimerWidget(TimerAndSoundBaseWidget):
    """Виджет таймера, отображаемый в игровом окне брейн-ринга."""

    def __init__(self, parent, timer: CustomTimer):
        super().__init__(parent, timer, audio_player=None, audio_output=None)
        self.last_timer_signal_indicator: int = -1

    def resizeEvent(self, event):
        """Переопределение стандартного метода, вызываемого автоматически при изменении размера окна."""
        super().resizeEvent(event)
        self.update_font_size()

    def set_font_color(self, color: QColor = QColor(0, 0, 0)) -> None:
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

    def update_font_size(self):
        """Обновление размера шрифта в соответствии с размером окна."""
        new_size = max(self.min_font_size, int(self.height() * 0.5), int(self.width() * 0.5))
        font = self.time_label.font()
        font.setPixelSize(new_size)
        self.time_label.setFont(font)

    def update_display(self) -> None:
        """Обновление отображения таймера"""
        if self.timer.is_run_out:
            self.set_font_color(QColor(228, 0, 42))
            return
        if self.timer.remaining_time <= 5:
            self.set_font_color(QColor(255, 153, 0))
        self.time_label.setText(self.format_time(self.timer.remaining_time))

    def handle_timer_start(self) -> None:
        """Обработчик начала отсчета таймера"""
        self.set_font_color(QColor(44, 151, 255))
        if self.timer.remaining_time <= 5:
            self.set_font_color(QColor(255, 153, 0))

    def handle_timer_run_out(self):
        """Обработчик окончания времени"""
        self.time_label.setText(self.format_time(0))
        self.last_timer_signal_indicator = -1

    def handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        self.set_font_color(QColor(44, 151, 255))
        self.time_label.setText(self.format_time(self.timer.remaining_time))

    def format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        if self.timer.remaining_time > 5:
            return f'{seconds:.0f}'
        return f'{seconds:.1f}'

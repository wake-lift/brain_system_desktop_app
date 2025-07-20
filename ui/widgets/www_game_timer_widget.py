from PyQt6.QtGui import QColor, QPalette

from config.enums import ColorSchemaEnum
from core.timer import CustomTimer
from core.widgets import TimerAndSoundBaseWidget


class WWWGameTimerWidget(TimerAndSoundBaseWidget):
    """Виджет таймера, отображаемый в игровом окне брейн-ринга."""

    def __init__(self, parent, timer: CustomTimer, font_size_ratio: float = 0.3):
        super().__init__(parent, timer, audio_player=None, audio_output=None)
        self.font_size_ratio = font_size_ratio  # отношение размера текста к размеру виджета
        self.set_font_color()

    def resizeEvent(self, event):
        """Переопределение стандартного метода, вызываемого автоматически при изменении размера окна."""
        super().resizeEvent(event)
        self.update_font_size()

    def set_font_color(self, color: QColor = QColor(ColorSchemaEnum.WWW_GAME_TIMER_INITIAL)) -> None:
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

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
        if self.timer.is_run_out:
            self.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_INITIAL))
            return
        self.time_label.setText(self.format_time(self.timer.remaining_time))

    def handle_timer_start(self) -> None:
        """Обработчик начала отсчета таймера"""
        self.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_START))

    def handle_timer_run_out(self):
        """Обработчик окончания времени"""
        self.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_INITIAL))
        self.time_label.setText(self.format_time(0))

    def handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        self.set_font_color(QColor(ColorSchemaEnum.WWW_GAME_TIMER_INITIAL))
        self.time_label.setText(self.format_time(self.timer.remaining_time))

    def format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        return f'{seconds:.0f}'

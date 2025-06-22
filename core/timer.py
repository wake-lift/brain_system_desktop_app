from PyQt6.QtCore import pyqtSignal, QObject, QTimer


class CustomTimer(QObject):
    """Custom countdown timer with additional methods and slots."""

    timer_start = pyqtSignal()
    timer_run_out = pyqtSignal()
    timer_reset = pyqtSignal()

    def __init__(self, initial_time: int, precision: int = 1):
        super().__init__()
        self.timer: QTimer = QTimer()
        self.timer.setInterval(precision)
        self.timer.timeout.connect(self._update_time)
        self.initial_time: int = initial_time * 1000
        self._remaining_time: int = self.initial_time
        self.is_running: bool = False
        self.is_paused: bool = False
        self.is_run_out: bool = False

    def start(self) -> None:
        self.is_run_out = False
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.timer.start()
        elif self.is_paused:
            self.resume()
        self.timer_start.emit()

    def pause(self) -> float:
        """Возвращает оставшееся время в секундах"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.timer.stop()
        return self._remaining_time / 1000

    def resume(self) -> None:
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.timer.start()
            self.timer_start.emit()

    def reset(self) -> None:
        self.stop()
        self.is_run_out = False
        self.timer_reset.emit()

    def stop(self) -> None:
        self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self._remaining_time = self.initial_time

    @property
    def remaining_time(self) -> float:
        """Remaining countdown time."""
        return self._remaining_time / 1000

    def _update_time(self):
        """Main update time method."""
        elapsed: int = self.timer.interval()
        self._remaining_time = max(0, self._remaining_time - elapsed)
        if self._remaining_time <= 0:
            self.stop()
            self.is_run_out = True
            self.timer_run_out.emit()

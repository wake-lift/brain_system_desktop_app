from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class CustomTimer(QObject):
    """Кастомный таймер обратного отсчета на базе встроенного в Qt таймера."""

    timer_start = pyqtSignal()
    timer_run_out = pyqtSignal()
    timer_reset = pyqtSignal()
    timer_ten_seconds_left = pyqtSignal()
    timer_to_provide_answers_run_out = pyqtSignal()

    def __init__(self, initial_time: int, precision: int = 1):
        super().__init__()
        self.timer: QTimer = QTimer()
        self.timer.setInterval(precision)  # разрешение таймера (мс)
        self.timer.timeout.connect(self._update_time)
        self.initial_time: int = initial_time * 1000  # с какого времени начинается обратный отсчет
        self._remaining_time: int = self.initial_time
        self.is_running: bool = False
        self.is_paused: bool = False
        self.is_run_out: bool = False

    def start(self) -> None:
        """Запускает таймер."""
        self.is_run_out = False
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.timer.start()
        elif self.is_paused:
            self.resume()
        self.timer_start.emit()

    def pause(self) -> float:
        """Ставит таймер на паузу и возвращает оставшееся время в секундах."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.timer.stop()
        return self._remaining_time / 1000

    def resume(self) -> None:
        """Возобновляет отсчет времени после паузы."""
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.timer.start()
            self.timer_start.emit()

    def reset(self) -> None:
        """Сбрасывает таймер."""
        self.stop()
        self.is_run_out = False
        self.timer_reset.emit()

    def stop(self) -> None:
        """Останавливает таймер."""
        self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self._remaining_time = self.initial_time

    @property
    def remaining_time(self) -> float:
        """Возвращает оставшееся время таймера."""
        return self._remaining_time / 1000

    def _update_time(self):
        """Реализует логику обратного отсчета."""
        elapsed: int = self.timer.interval()
        self._remaining_time = max(0, self._remaining_time - elapsed)
        if self._remaining_time <= 0:
            self.stop()
            self.is_run_out = True
            self.timer_run_out.emit()
            self.timer_to_provide_answers_run_out.emit()

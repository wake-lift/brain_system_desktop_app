from abc import abstractmethod
from pathlib import Path

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import QUrl

from config.enums import SoundFilesEnum
from core.timer import CustomTimer


class MainWindowTimerAndSoundBase(QWidget):
    def __init__(self, parent, timer: CustomTimer, audio_player: QMediaPlayer, audio_output: QAudioOutput):
        super().__init__(parent)
        self.timer: CustomTimer = timer
        self.audio_player: QMediaPlayer = audio_player
        self.audio_output: QAudioOutput = audio_output
        self.initial_time: float = timer.initial_time / 1000
        self.time_label: QLabel | None = None
        self.timer.timer.timeout.connect(self.update_display)
        self.timer.timer_start.connect(self.handle_timer_start)
        self.timer.timer_run_out.connect(self.handle_timer_run_out)
        self.timer.timer_reset.connect(self.handle_timer_reset)

    def set_font_color(self, color: QColor = QColor(0, 0, 0)) -> None:
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

    def play_sound(self, sound_file_name: SoundFilesEnum) -> None:
        path_to_file = Path(__file__).absolute().parent.parent.parent / 'assets' / 'sounds' / sound_file_name.value
        self.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
        self.audio_player.setSource(self.current_audio_file)
        self.audio_player.play()

    @abstractmethod
    def update_display(self) -> None:
        """Обновление отображения таймера"""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_run_out(self):
        """Обработчик окончания времени"""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_start(self) -> None:
        """Обработчик начала отсчета таймера"""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        raise NotImplementedError

    @abstractmethod
    def format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        raise NotImplementedError

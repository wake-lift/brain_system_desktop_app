from pathlib import Path
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import QUrl

from config.enums import SoundFilesEnum
from core.timer import CustomTimer


class BrainRingTimerAndSoundMixin(QWidget):
    def __init__(self, parent, timer: CustomTimer, audio_player: QMediaPlayer, audio_output: QAudioOutput):
        super().__init__(parent)
        self.timer: CustomTimer = timer
        self.audio_player: QMediaPlayer = audio_player
        self.audio_output: QAudioOutput = audio_output
        self.initial_time: float = timer.initial_time / 1000
        self.time_label: QLabel | None = None
        self.timer.timer.timeout.connect(self.update_display)
        self.timer.timer_start.connect(self._handle_timer_start)
        self.timer.timer_run_out.connect(self._handle_timer_run_out)
        self.timer.timer_reset.connect(self._handle_timer_reset)
        self.last_timer_signal_inficator: int = -1

    def update_display(self) -> None:
        """Обновление отображения таймера"""
        remaining_time_int = int(self.timer.remaining_time)
        if self.timer.is_run_out:
            self._set_font_color(QColor(204, 0, 0))
            return
        if self.timer.remaining_time <= 5:
            self._set_font_color(QColor(204, 0, 0))
        self.time_label.setText(self._format_time(self.timer.remaining_time))
        if all([
                remaining_time_int in [0, 1, 2, 3, 4],
                remaining_time_int != self.last_timer_signal_inficator,
                self.audio_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState,
        ]):
            self.last_timer_signal_inficator = remaining_time_int
            self._play_sound(SoundFilesEnum.BRAIN_TIMER_CLOSE_TO_END)

    def _handle_timer_run_out(self):
        """Обработчик окончания времени"""
        self._set_font_color(QColor(0, 0, 0))
        self.time_label.setText(self._format_time(0))
        self._play_sound(SoundFilesEnum.BRAIN_TIMER_START_END)
        self.last_timer_signal_inficator = -1

    def _handle_timer_start(self) -> None:
        """Обработчик ..."""
        self._set_font_color(QColor(0, 0, 0))
        if self.timer.remaining_time <= 5:
            self._set_font_color(QColor(204, 0, 0))
        self._play_sound(SoundFilesEnum.BRAIN_TIMER_START_END)

    def _handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        self._set_font_color(QColor(0, 0, 0))
        self.time_label.setText(self._format_time(self.timer.remaining_time))

    def _set_font_color(self, color: QColor = QColor(0, 0, 0)) -> None:
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

    def _format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        if self.timer.remaining_time > 5:
            return f'{seconds:.0f}'
        return f'{seconds:.1f}'

    def _play_sound(self, sound_file_name: SoundFilesEnum) -> None:
        path_to_file = Path(__file__).absolute().parent.parent.parent / 'assets' / 'sounds' / sound_file_name.value
        self.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
        self.audio_player.setSource(self.current_audio_file)
        self.audio_player.play()


class WWWTimerAndSoundMixin(QWidget):
    def __init__(self, parent, timer: CustomTimer, audio_player: QMediaPlayer, audio_output: QAudioOutput):
        super().__init__(parent)
        self.timer: CustomTimer = timer
        self.audio_player: QMediaPlayer = audio_player
        self.audio_output: QAudioOutput = audio_output
        self.initial_time: float = timer.initial_time / 1000
        self.time_label: QLabel | None = None
        self.timer.timer.timeout.connect(self.update_display)
        self.timer.timer_start.connect(self._handle_timer_start)
        self.timer.timer_run_out.connect(self._handle_timer_run_out)
        self.timer.timer_reset.connect(self._handle_timer_reset)
        self.ten_seconds_left_signal_already_sounded: bool = False

    def update_display(self) -> None:
        """Обновление отображения таймера"""
        remaining_time_int = int(self.timer.remaining_time)
        if self.timer.is_run_out:
            self.set_font_color(QColor(0, 0, 0))
            return
        self.time_label.setText(self._format_time(self.timer.remaining_time))
        if remaining_time_int == 9 and not self.ten_seconds_left_signal_already_sounded:
            self.timer.timer_ten_seconds_left.emit()
            self.ten_seconds_left_signal_already_sounded = True

    def _handle_timer_run_out(self):
        """Обработчик окончания времени"""
        self.set_font_color(QColor(0, 0, 0))
        self.time_label.setText(self._format_time(0))
        self._play_sound(SoundFilesEnum.TIMER_START_STOP)
        self.ten_seconds_left_signal_already_sounded = False

    def _handle_timer_start(self) -> None:
        """Обработчик ..."""
        self.set_font_color(QColor(0, 0, 0))
        self._play_sound(SoundFilesEnum.TIMER_START_STOP)
        self.ten_seconds_left_signal_already_sounded = False

    def _handle_timer_reset(self) -> None:
        """Обработчик сброса таймера"""
        self.set_font_color(QColor(0, 0, 0))
        self.time_label.setText(self._format_time(self.timer.remaining_time))
        self.ten_seconds_left_signal_already_sounded = False

    def set_font_color(self, color: QColor = QColor(0, 0, 0)) -> None:
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

    def _format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения"""
        return f'{seconds:.0f}'

    def _play_sound(self, sound_file_name: SoundFilesEnum) -> None:
        path_to_file = Path(__file__).absolute().parent.parent.parent / 'assets' / 'sounds' / sound_file_name.value
        self.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
        self.audio_player.setSource(self.current_audio_file)
        self.audio_player.play()

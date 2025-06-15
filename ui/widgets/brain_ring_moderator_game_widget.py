from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QSizePolicy, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

from core.timer import CustomTimer
from ui.widgets.mixins import BrainRingTimerAndSoundMixin


class BrainRingModeratorGameWidget(BrainRingTimerAndSoundMixin):
    """Widget displayed on moderator's panel. Duplicates info on players main widget."""

    def __init__(self, parent, timer: CustomTimer, audio_player: QMediaPlayer, audio_output: QAudioOutput):
        super().__init__(parent, timer, audio_player, audio_output)
        self.resize(150, 150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.time_label = QLabel(self._format_time(self.timer.remaining_time))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont()
        font.setFamily('Arial')
        font.setWeight(QFont.Weight.Bold)
        self.time_label.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.min_font_size = 12
        self.update_font_size()

    def resizeEvent(self, event):
        """Is called automatically when window size is changed."""
        super().resizeEvent(event)
        self.update_font_size()

    def update_font_size(self):
        """Update font size to keep relative ratio to window size."""
        new_size = max(self.min_font_size, int(self.height() * 0.3), int(self.width() * 0.3))
        font = self.time_label.font()
        font.setPixelSize(new_size)
        self.time_label.setFont(font)

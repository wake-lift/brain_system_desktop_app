from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer

from config.enums import SoundFileEnum


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def select_audio_track_handler(obj: MainWindow, chosen_text: str):
    chosen_file_name: str = SoundFileEnum.get_item_by_label(chosen_text).value
    path_to_file = Path(__file__).absolute().parent.parent / 'assets' / 'sounds' / chosen_file_name
    obj.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
    obj.audio_player.setSource(obj.current_audio_file)


def start_audio_track_handler(obj: MainWindow) -> None:
    if obj.current_audio_file is None:
        return None
    if obj.audio_player.playbackState() not in [
        QMediaPlayer.PlaybackState.PausedState, QMediaPlayer.PlaybackState.PlayingState,
    ]:
        obj.audio_player.play()


def pause_or_resume_audio_track_handler(obj: MainWindow) -> None:
    if obj.current_audio_file is None:
        return None
    match obj.audio_player.playbackState():
        case QMediaPlayer.PlaybackState.PlayingState:
            obj.audio_player.pause()
            obj.sound_panel_pause_button.setText('Resume')
        case QMediaPlayer.PlaybackState.PausedState:
            obj.audio_player.play()
            obj.sound_panel_pause_button.setText('Pause')
        case QMediaPlayer.PlaybackState.StoppedState:
            return None


def stop_audio_track_handler(obj: MainWindow) -> None:
    if obj.current_audio_file is None:
        return None
    obj.audio_player.stop()


def set_audio_output_volume_handler(obj: MainWindow, value: int) -> None:
    obj.audio_output.setVolume(value / 100)

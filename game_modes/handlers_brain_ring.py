from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def brain_ring_start_push_button_handler(obj: MainWindow):
    obj.timer.start()


def brain_ring_pause_resume_push_button_handler(obj: MainWindow):
    if not obj.timer.is_paused:
        obj.timer.pause()
    else:
        obj.timer.resume()


def brain_ring_reset_push_button_handler(obj: MainWindow):
    obj.timer.reset()

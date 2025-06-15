from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ui.main_window import MainWindow


def brain_ring_key_press_handler(obj: MainWindow, pressed_key: str):
    obj.test_label.setText(f"Нажата клавиша brain_ring: '{pressed_key}'")


def www_key_press_handler(obj: MainWindow, pressed_key: str):
    obj.test_label.setText(f"Нажата клавиша www: '{pressed_key}'")


def erudite_key_press_handler(obj: MainWindow, pressed_key: str):
    obj.test_label.setText(f"Нажата клавиша erudite: '{pressed_key}'")

from pathlib import Path

from PyQt6.QtCore import QSize, Qt, QByteArray
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QColor


class BlockedPlayerIndicatorWidget(QSvgWidget):
    def __init__(self, parent=None, background_color: QColor = QColor(Qt.GlobalColor.transparent)) -> None:
        super().__init__(parent)
        self._background_color = background_color
        self._stroke_color = QColor(Qt.GlobalColor.black)
        self._stroke_width = 6
        self._aspect_ratio = None
        self._indicator_template = self._load_template()
        self.update_svg()

    def _load_template(self) -> str:
        """Loads SVG template from file"""
        path_to_file = (
            Path(__file__).absolute().parent.parent / 'assets' / 'images' / 'blocked_player_indicator_template.svg'
        )
        with open(path_to_file, 'r', encoding='utf-8') as file:
            return file.read()

    def set_style(self, background_color=None, stroke_color=None, stroke_width=None) -> None:
        if background_color is not None:
            self._background_color = QColor(background_color)  # Гарантируем, что это QColor
        if stroke_color is not None:
            self._stroke_color = QColor(stroke_color)
        if stroke_width is not None:
            self._stroke_width = stroke_width
        self.update_svg()

    def update_svg(self):
        svg = self._indicator_template
        svg = svg.replace('%%BG_COLOR%%', self._background_color.name())
        svg = svg.replace('%%STROKE_COLOR%%', self._stroke_color.name())
        svg = svg.replace('%%STROKE_WIDTH%%', str(self._stroke_width))
        self.load(QByteArray(svg.encode('utf-8')))

        if self.renderer().isValid():
            default_size = self.renderer().defaultSize()
            if not default_size.isEmpty():
                self._aspect_ratio = default_size.width() / default_size.height()

    def sizeHint(self) -> QSize:
        if self._aspect_ratio and self._aspect_ratio > 0:
            width = min(self.width(), int(self.height() * self._aspect_ratio))
            return QSize(width, int(width / self._aspect_ratio))
        return super().sizeHint()

    def resizeEvent(self, event) -> None:
        if self._aspect_ratio and self._aspect_ratio > 0:
            new_size = event.size()
            new_width = min(new_size.width(), int(new_size.height() * self._aspect_ratio))
            new_height = int(new_width / self._aspect_ratio)
            self.resize(new_width, new_height)
        super().resizeEvent(event)

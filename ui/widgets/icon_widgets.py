from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.widgets import ScalableColoredSvgWidget


class CheckCircleSvgWidget(ScalableColoredSvgWidget):
    def __init__(
        self,
        parent=None,
        background_color: QColor = QColor(Qt.GlobalColor.white),
        stroke_color: QColor = QColor(Qt.GlobalColor.black),
    ) -> None:
        super().__init__(parent)
        self.background_color = background_color
        self.stroke_color = stroke_color
        self.template_path: Path = (
            Path(__file__).absolute().parent.parent.parent / 'assets' / 'images' / 'check_circle_template.svg'
        )
        self.svg_template: str = self.load_template()
        self.update_svg()


class CircleSvgWidget(ScalableColoredSvgWidget):
    def __init__(
        self,
        parent=None,
        background_color: QColor = QColor(Qt.GlobalColor.white),
        stroke_color: QColor = QColor(Qt.GlobalColor.black),
    ) -> None:
        super().__init__(parent)
        self.background_color = background_color
        self.stroke_color = stroke_color
        self.template_path: Path = (
            Path(__file__).absolute().parent.parent.parent / 'assets' / 'images' / 'circle_template.svg'
        )
        self.svg_template: str = self.load_template()
        self.update_svg()


class CrossSvgWidget(ScalableColoredSvgWidget):
    def __init__(
        self,
        parent=None,
        background_color: QColor = QColor(Qt.GlobalColor.white),
        stroke_color: QColor = QColor(Qt.GlobalColor.black),
    ) -> None:
        super().__init__(parent)
        self.background_color = background_color
        self.stroke_color = stroke_color
        self.template_path: Path = (
            Path(__file__).absolute().parent.parent.parent / 'assets' / 'images' / 'cross_round_template.svg'
        )
        self.svg_template: str = self.load_template()
        self.update_svg()

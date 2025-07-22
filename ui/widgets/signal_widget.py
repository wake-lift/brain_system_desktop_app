from enum import StrEnum

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QColor

from config.enums import ColorSchemaEnum


class ArcLocationEnum(StrEnum):
    """С какой стороны будет отрисована дуга у объекта SignalArcWidget."""
    LEFT = 'Левая сторона вогнутая'
    RIGHT = 'Правая сторона вогнутая'


class SignalArcWidget(QWidget):
    """Виджет, представляющий собой прямоугольник с вогнутой левой или правой стороной."""

    def __init__(
        self,
        parent=None,
        arc_location: ArcLocationEnum = ArcLocationEnum.LEFT,  # сторона, на которой расположен вогнутая дуга
        arc_radius_ratio: float = 0.35,  # степень вогнутости дуги по отношению к горизонтальной стороне виджета
        infill_color: ColorSchemaEnum = ColorSchemaEnum.BRAIN_GAME_WIDGET_BACKGROUND  # исходный цвет виджета
    ):
        super().__init__(parent)
        self.arc_radius_ratio = arc_radius_ratio
        self.arc_location = arc_location
        self.infill_color = infill_color
        
    def update_infill_color(self, color: ColorSchemaEnum):
        """Устанавливает цвет заполнения."""
        self.infill_color = color
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        concavity = width * self.arc_radius_ratio 
        
        path = QPainterPath()
        match self.arc_location:
            case ArcLocationEnum.LEFT:
                path.moveTo(width, 0)
                path.lineTo(width, height)
                path.lineTo(0, height)
                path.cubicTo(concavity, height * 0.75, concavity, height * 0.25, 0, 0)
            case ArcLocationEnum.RIGHT:
                path.moveTo(0, 0)
                path.lineTo(0, height)
                path.lineTo(width, height)
                path.cubicTo(width - concavity, height * 0.75, width - concavity, height * 0.25, width, 0)
        
        path.closeSubpath()
        painter.fillPath(path, QBrush(QColor(self.infill_color)))
        # если нужна обводка виджета:
        # painter.setPen(Qt.GlobalColor.black)
        # painter.drawPath(path)

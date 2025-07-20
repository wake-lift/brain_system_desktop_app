from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QSizePolicy

from config.enums import ColorSchemaEnum
from core.widgets import ScalableLabel, ScalableColoredSvgWidget, ScalableSvgWidget


class WidgetBuilderMixin:
    """Миксин, добавляющий методы создания виджетов из базовых классов."""

    @staticmethod
    def build_icon_widget(
        widget_cls: type[ScalableSvgWidget],
        horizontal_stretch: int = 5,
    ) -> ScalableSvgWidget:
        """Создает автомасштабируемый виджет svg-изображения."""
        icon_widget = widget_cls()
        size_policy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(horizontal_stretch)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(icon_widget.sizePolicy().hasHeightForWidth())
        icon_widget.setSizePolicy(size_policy)
        return icon_widget

    @staticmethod
    def build_colored_icon_widget(
        widget_cls: type[ScalableColoredSvgWidget],
        background_color: ColorSchemaEnum,
        stroke_color: ColorSchemaEnum,
        horizontal_stretch: int = 5,
    ) -> ScalableColoredSvgWidget:
        """Создает автомасштабируемый виджет svg-изображения с возможностью управления цветом."""
        colored_icon_widget = widget_cls(background_color=QColor(background_color), stroke_color=QColor(stroke_color))
        size_policy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(horizontal_stretch)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(colored_icon_widget.sizePolicy().hasHeightForWidth())
        colored_icon_widget.setSizePolicy(size_policy)
        return colored_icon_widget

    @staticmethod
    def build_label_widget(
        horizontal_stretch: int = 65,
        text: str = 'label_text',
        color: ColorSchemaEnum = ColorSchemaEnum.DEFAULT_SCALABLE_LABEL,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        bold: bool = False,
    ) -> ScalableLabel:
        """Создает автомасштабируемый текстовый виджет с указанными параметрами."""
        label_widget = ScalableLabel(alignment=alignment)
        size_policy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        size_policy.setHorizontalStretch(horizontal_stretch)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(label_widget.sizePolicy().hasHeightForWidth())
        label_widget.setSizePolicy(size_policy)
        label_widget.setStyleSheet(f'color: {color};')
        if bold:
            current_style = label_widget.styleSheet()
            new_style = current_style + ' font-weight: bold;'
            label_widget.setStyleSheet(new_style)
        label_widget.setText(text)
        return label_widget

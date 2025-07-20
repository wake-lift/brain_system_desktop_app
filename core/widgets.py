from abc import abstractmethod
from pathlib import Path

from PyQt6.QtGui import QColor, QFont, QPaintEvent, QPainter, QPalette
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import QByteArray, QRectF, QSize, QUrl, Qt
from PyQt6.QtSvgWidgets import QSvgWidget

from config.enums import SoundFileEnum
from core.timer import CustomTimer


class TimerAndSoundBaseWidget(QWidget):
    """Базовый виджет отрисовки игрового таймера и воспроизведения звуковых сигналов"""

    def __init__(
        self,
        parent,
        timer: CustomTimer,
        audio_player: QMediaPlayer | None,
        audio_output: QAudioOutput | None,
    ):
        super().__init__(parent)
        self.timer: CustomTimer = timer
        self.audio_player: QMediaPlayer | None = audio_player
        self.audio_output: QAudioOutput | None = audio_output
        self.initial_time: float = timer.initial_time / 1000
        self.time_label: QLabel | None = None
        self.font_size_ratio: float = 0.3
        self.timer.timer.timeout.connect(self.update_display)
        self.timer.timer_start.connect(self.handle_timer_start)
        self.timer.timer_run_out.connect(self.handle_timer_run_out)
        self.timer.timer_reset.connect(self.handle_timer_reset)
        self.configure_widget_geometry()

    def set_font_color(self, color: QColor = QColor(0, 0, 0)) -> None:
        """Устанавливает цвет шрифта таймера."""
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.time_label.setPalette(palette)

    def play_sound(self, sound_file_name: SoundFileEnum) -> None:
        """Воспроизводит переданный звуковой файл."""
        path_to_file = Path(__file__).absolute().parent.parent / 'assets' / 'sounds' / sound_file_name.value
        self.current_audio_file = QUrl.fromLocalFile(str(path_to_file))
        self.audio_player.setSource(self.current_audio_file)
        self.audio_player.play()

    def configure_widget_geometry(self):
        """Определяет геометрию виджета."""
        self.resize(150, 150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.time_label = QLabel(self.format_time(self.timer.remaining_time))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = QFont()
        font.setFamily('Arial')
        font.setWeight(QFont.Weight.Bold)
        self.time_label.setFont(font)
        palette = self.time_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(44, 151, 255))
        self.time_label.setPalette(palette)
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.min_font_size = 12
        self.update_font_size()

    @abstractmethod
    def update_display(self) -> None:
        """Обновление отображения таймера."""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_run_out(self):
        """Обработчик окончания времени."""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_start(self) -> None:
        """Обработчик начала отсчета таймера."""
        raise NotImplementedError

    @abstractmethod
    def handle_timer_reset(self) -> None:
        """Обработчик сброса таймера."""
        raise NotImplementedError

    @abstractmethod
    def format_time(self, seconds: float) -> str:
        """Форматирование времени для отображения."""
        raise NotImplementedError


class ScalableLabel(QLabel):
    """Базовый класс для автомасштабируемого текстового виджета."""

    def __init__(
        self,
        bold: bool = False,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        *args, **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setAlignment(alignment)
        self.setMinimumSize(3, 3)  # минимальный размер виджета
        self.base_font_size = 3  # минимальный размер шрифта
        self.divisor: int = 2  # настраиваемый делитель, определяющий относительный размер текста
        self.bold = bold
        self.update_font_size()

    def update_font_size(self):
        """Рассчитывает размер шрифта на основе текущего размера виджета."""
        new_size = min(self.width(), self.height()) // self.divisor
        font = self.font()
        font.setBold(self.bold)
        font.setPixelSize(max(new_size, self.base_font_size))
        self.setFont(font)

    def resizeEvent(self, event):
        """Переопределение стандартного метода, автоматически вызываемого при изменении размера виджета."""
        super().resizeEvent(event)
        self.update_font_size()


class ScalableSvgWidget(QSvgWidget):
    """ Базовый класс для автомасштабируемого виджета на основе svg-изображения."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._aspect_ratio = None
        self.template_path: Path = Path('')
        self.svg_template: str = ''

    def load_template(self) -> str:
        """Загружает svg-шаблон из файла."""
        with open(self.template_path, 'r', encoding='utf-8') as file:
            return file.read()

    def update_svg(self):
        """Обновляет цвет svg-изображения."""
        svg = self.svg_template
        self.load(QByteArray(svg.encode('utf-8')))

        if self.renderer().isValid():
            default_size = self.renderer().defaultSize()
            if not default_size.isEmpty():
                self._aspect_ratio = default_size.width() / default_size.height()
                self.updateGeometry()

    def sizeHint(self) -> QSize:
        """Переопределение стандартного метода, отвечающего за расчет размера виджета."""
        if self._aspect_ratio and self._aspect_ratio > 0:
            height = min(self.height(), int(self.width() / self._aspect_ratio))
            return QSize(int(height * self._aspect_ratio), height)
        return super().sizeHint()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Переопределение стандартного метода, отвечающего за отрисовку виджета на экране."""
        if not self.renderer().isValid():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        widget_size = self.size()
        if self._aspect_ratio:
            target_width = min(widget_size.width(), int(widget_size.height() * self._aspect_ratio))
            target_height = int(target_width / self._aspect_ratio)
            target_size = QSize(target_width, target_height)
        else:
            target_size = widget_size

        x = (widget_size.width() - target_size.width()) // 2
        y = (widget_size.height() - target_size.height()) // 2
        self.renderer().render(painter, QRectF(x, y, target_size.width(), target_size.height()))


class ScalableColoredSvgWidget(ScalableSvgWidget):
    """
    Базовый класс для автомасштабируемого виджета на основе svg-изображения с двумя параметрами цвета:
    - BG_COLOR - цвет фона;
    - STROKE_COLOR - цвет обводки и внутренних элементов.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._background_color: QColor = QColor(Qt.GlobalColor.transparent)
        self._stroke_color = QColor(Qt.GlobalColor.black)

    def update_svg(self):
        """Обновляет цвет svg-изображения."""
        svg = self.svg_template
        svg = svg.replace('%%BG_COLOR%%', self.background_color.name())
        svg = svg.replace('%%STROKE_COLOR%%', self.stroke_color.name())
        self.load(QByteArray(svg.encode('utf-8')))

        if self.renderer().isValid():
            default_size = self.renderer().defaultSize()
            if not default_size.isEmpty():
                self._aspect_ratio = default_size.width() / default_size.height()
                self.updateGeometry()

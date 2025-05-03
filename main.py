from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QApplication
)
from PyQt6.QtCore import Qt
import sys

class SecondaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вспомогательное окно")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        label = QLabel("Это вспомогательное окно")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Основное окно")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.open_button = QPushButton("Открыть вспомогательное окно")
        self.open_button.clicked.connect(self.open_secondary_window)
        layout.addWidget(self.open_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def open_secondary_window(self):
        self.secondary_window = SecondaryWindow()
        self.secondary_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QPushButton,
    QVBoxLayout,
)

class LibraryPanel(QDockWidget):
    def __init__(self):
        super().__init__("Library", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        main_layout = QVBoxLayout()

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)
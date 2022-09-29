from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction


class Actions(QObject):
    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self.new_image = QAction("&New Image", self)
        self.new_image.setShortcut("Ctrl+N")

        self.export_image = QAction("&Export Image...", self)
        self.export_image.setShortcut("Ctrl+E")

        self.exit = QAction("&Quit", self)
        self.exit.setShortcut("Alt+F4")

        self.generate = QAction("&Generate Image", self)
        self.generate.setShortcut("F5")

        self.use_as_input_image = QAction("Use As &Input Image", self)
        self.use_as_input_image.setShortcut("Ctrl+I")

        self.open_input_image = QAction("&Open Input Image...", self)
        self.open_input_image.setShortcut("Shift+Ctrl+I")

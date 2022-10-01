from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction


class Actions(QObject):
    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.new_image = QAction("&New Image", self)
        self.new_image.setShortcut("Ctrl+N")

        self.export_image = QAction("&Export Image...", self)
        self.export_image.setShortcut("Ctrl+E")

        self.exit = QAction("&Quit", self)
        self.exit.setShortcut("Alt+F4")

        self.dream_image = QAction("Dream &Image", self)
        self.dream_image.setShortcut("F5")

        self.dream_sequence = QAction("Dream &Sequence", self)
        self.dream_sequence.setShortcut("Shift+F5")

        self.import_image_and_data = QAction("&Import Image and Data...", self)
        self.import_image_and_data.setShortcut("Ctrl+I")

        self.use_as_input_image = QAction("Use As &Input Image", self)
        self.use_as_input_image.setShortcut("Ctrl+U")

        self.open_input_image = QAction("&Open Input Image...", self)
        self.open_input_image.setShortcut("Shift+Ctrl+O")

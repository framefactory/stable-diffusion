from pathlib import Path
import os

from PySide6.QtCore import (
    QObject
)

from .preferences import Preferences


class Library(QObject):
    def __init__(self, parent: QObject, preferences: Preferences):
        super().__init__(parent)
        self.base_path = Path(preferences.library_path)
        os.makedirs(self.base_path, exist_ok=True)

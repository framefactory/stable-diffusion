from typing import Tuple
from pathlib import Path
from datetime import datetime
import os

from PIL.Image import Image

from PySide6.QtCore import (
    QObject
)

from ui.data import Preferences


class Library(QObject):
    def __init__(self, parent: QObject, preferences: Preferences):
        super().__init__(parent)

        self.base_path = Path(preferences.library_path)
        self.current_folder = ""

        os.makedirs(self.base_path, exist_ok=True)

    @staticmethod
    def generate_file_path(ext: str = "") -> str:
        return datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3] + ext

    def compose_path(self, file_path: str, *, suffix: str = "",
        extension: str = "", folder: str = "") -> str:

        if suffix or extension:
            base, ext = os.path.splitext(file_path)
            file_path = base + suffix + (extension if extension else ext)

        folder = folder or self.current_folder
        return str(self.base_path / folder / file_path)

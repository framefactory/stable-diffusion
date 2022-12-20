from typing import Optional
from pathlib import Path
from datetime import datetime
import os

from PIL import Image as PIL_Image
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

    def compose_library_path(self, file_path: str, *, suffix: str = "",
        extension: str = "", folder: str = "") -> str:

        if suffix or extension:
            base, ext = os.path.splitext(file_path)
            file_path = base + suffix + (("." + extension) if extension else ext)

        folder = folder or self.current_folder
        return str(self.base_path / folder / file_path)

    @staticmethod
    def generate_file_path(ext: str = "") -> str:
        return datetime.now().strftime("%Y%m%d-%H%M%S") + ext

    @staticmethod
    def compose_path(file_path: str, *, suffix: str = "",
        extension: str = "", folder: str = "") -> str:

        if suffix or extension:
            base, ext = os.path.splitext(file_path)
            file_path = base + suffix + (("." + extension) if extension else ext)

        return str(Path(folder) / file_path)

    @staticmethod
    def load_image(path: str) -> Optional[Image]:
        try:
            with PIL_Image.open(path) as image:
                image.load()
                return image
        except:
            print(f"failed to load image from: {path}")
            return None
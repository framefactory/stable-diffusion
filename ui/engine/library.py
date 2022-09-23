from pathlib import Path
from datetime import datetime
import random
import json
import os

from PIL.Image import Image

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal
)

from .params import ImageParams
from .image_document import ImageDocument


class Library(QObject):
    def __init__(self, parent: QObject, base_path: str):
        super().__init__(parent)
        self.base_path = Path(base_path)
        os.makedirs(self.base_path, exist_ok=True)

    def save_image(self, image: Image, params: ImageParams) -> ImageDocument:
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        random.seed()
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        rand = "".join([ chars[random.randint(0, 35)] for i in range(4) ])
        base_name =  f"{now}-{rand}"
        image_path = f"{base_name}.png"
        data_path = f"{base_name}.json"

        item = ImageDocument(image, image_path, params)
        image.save(self.base_path / image_path)

        with open(self.base_path / data_path, "w") as json_file:
            json.dump(item.to_dict(), json_file, indent=4)

        return item

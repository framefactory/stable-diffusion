from typing import Optional

from PIL import Image as PIL_Image
from PIL.Image import Image
from PIL.ImageQt import ImageQt

from PySide6.QtCore import (
    Qt,
    QSize
)

from PySide6.QtGui import (
    QPixmap
)

from PySide6.QtWidgets import (
    QSizePolicy,
    QLabel
)

class ImageThumb(QLabel):
    def __init__(self):
        super().__init__("No Image")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignCenter)

    def setImage(self, image: Image):
        w, h = image.size
        a = w / h
        w = 128 if a >= 1 else int(w * a)
        h = 128 if a < 1 else int(w / a)
        resized = image.resize((w, h), PIL_Image.Resampling.BICUBIC)
        left = 64 - w // 2
        top = 64 - h // 2
        thumb = PIL_Image.new("RGB", (128, 128))
        thumb.paste(resized, (left, top, left + w, top + h))
        pixmap = QPixmap.fromImage(ImageQt(thumb))
        self.setPixmap(pixmap)
        self.setText("")

    def loadImage(self, path: str):
        image = PIL_Image.open(path)
        image.load()
        self.setImage(image)

    def clearImage(self):
        self.setPixmap(QPixmap())
        self.setText("No Image")

    def sizeHint(self) -> QSize:
        return QSize(128, 128)
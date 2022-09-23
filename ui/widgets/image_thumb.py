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

        self._path: str = ""
        self._image: Optional[Image] = None

    def setImage(self, path: str, image: Image):
        self._path = path
        self._image = image
        pixmap = QPixmap.fromImage(ImageQt(image))
        self.setPixmap(pixmap)
        self.setText("")

    def loadImage(self, path: str):
        image = PIL_Image.open(path)
        image.load()
        self.setImage(path, image)

    def clearImage(self):
        self._path = ""
        self._image = None
        self.setPixmap(QPixmap())
        self.setText("No Image")

    def sizeHint(self) -> QSize:
        return QSize(128, 128)
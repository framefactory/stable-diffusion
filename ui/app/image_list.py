from typing import Optional

from PySide6.QtCore import (
    QObject
)

from PySide6.QtWidgets import (
    QFileSystemModel
)

class ImageList(QFileSystemModel):
    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QListView
)

class ImageListView(QListView):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
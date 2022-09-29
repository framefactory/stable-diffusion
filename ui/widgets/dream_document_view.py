
from PySide6.QtWidgets import (
    QWidget,
    QMdiSubWindow
)

from ui.app import DreamDocument


class DreamDocumentView(QMdiSubWindow):
    def __init__(self, parent: QWidget, document: DreamDocument):
        super().__init__(parent)
        self.document = document
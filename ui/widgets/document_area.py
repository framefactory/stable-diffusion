from typing import Optional

from PySide6.QtGui import (
    QColor
)

from PySide6.QtWidgets import (
    QWidget,
    QMdiArea
)

from ui.engine.image_document import ImageDocument
from .image_view import ImageDocumentView

class DocumentArea(QMdiArea):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setBackground(QColor("#202020"))
        self.setViewMode(QMdiArea.TabbedView)
        self.setTabsMovable(True)
        self.setTabsClosable(True)

    def addDocument(self, document: Optional[ImageDocument] = None) -> ImageDocumentView:
        document_view = ImageDocumentView(self, document)
        self.addSubWindow(document_view)
        document_view.showMaximized()
        return document_view

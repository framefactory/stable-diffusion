from typing import Optional, cast

from PySide6.QtCore import Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QMdiArea

from ui.app import (
    DreamDocument, 
    Documents
)

from .dream_document_view import DreamDocumentView

class DocumentArea(QMdiArea):
    def __init__(self, parent: QWidget, documents: Documents):
        super().__init__(parent)
        self._documents = documents

        documents.document_added.connect(self.create_view)
        documents.active_document_changed.connect(self.set_active_document)

        self.setBackground(QColor("#202020"))
        self.setViewMode(QMdiArea.TabbedView)
        self.setTabsMovable(True)
        self.setTabsClosable(True)

    @Slot(DreamDocument)
    def create_view(self, document: DreamDocument) -> DreamDocumentView:
        print("create document view")
        image_view = DreamDocumentView(self, document)
        self.addSubWindow(image_view)
        image_view.showMaximized()
        return image_view

    @Slot(DreamDocument)
    def set_active_document(self, document: DreamDocument):
        views = self.subWindowList()
        for view in views:
            document_view = cast(DreamDocumentView, view)
            if document_view.document == document:
                self.setActiveSubWindow(document_view)
                return
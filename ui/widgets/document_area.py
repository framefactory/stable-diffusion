from typing import Optional, cast

from PySide6.QtCore import Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QMdiArea

from ui.app import (
    DreamDocument, 
    DreamImage, 
    DreamSequence, 
    Documents,
    FrameResult
)

from .dream_document_view import DreamDocumentView
from .dream_image_view import DreamImageView
from .dream_sequence_view import DreamSequenceView

class DocumentArea(QMdiArea):
    def __init__(self, parent: QWidget, documents: Documents):
        super().__init__(parent)
        self._documents = documents

        documents.image_added.connect(self.create_image_view)
        documents.sequence_added.connect(self.create_sequence_view)
        documents.active_document_changed.connect(self.set_active_document)

        self.setBackground(QColor("#202020"))
        self.setViewMode(QMdiArea.TabbedView)
        self.setTabsMovable(True)
        self.setTabsClosable(True)

    @Slot(DreamImage)
    def create_image_view(self, document: DreamImage) -> DreamImageView:
        print("create image view")
        image_view = DreamImageView(self, document)
        self.addSubWindow(image_view)
        image_view.showMaximized()
        return image_view

    @Slot(DreamSequence)
    def create_sequence_view(self, document: DreamSequence) -> DreamSequenceView:
        sequence_view = DreamSequenceView(self, document)
        self.addSubWindow(sequence_view)
        sequence_view.showMaximized()
        return sequence_view

    @Slot(DreamDocument)
    def set_active_document(self, document: DreamDocument):
        views = self.subWindowList()
        for view in views:
            document_view = cast(DreamDocumentView, view)
            if document_view.document == document:
                self.setActiveSubWindow(document_view)
                return
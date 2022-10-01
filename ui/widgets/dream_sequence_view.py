from typing import Optional

from PIL.Image import Image
from PIL.ImageQt import ImageQt

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget
)

from ui.app import DreamSequenceDocument
from .dream_document_view import DreamDocumentView


class DreamSequenceView(DreamDocumentView):
    def __init__(self, parent: QWidget, document: DreamSequenceDocument):
        super().__init__(parent, document)

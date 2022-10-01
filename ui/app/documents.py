from typing import Optional, Union, List, cast

from PySide6.QtCore import QObject, Signal, Slot

from ui.data import DreamSequence

from .dreamer import DreamResult
from .dream_document import DreamDocument


class Documents(QObject):
    document_added = Signal(DreamDocument)
    active_document_changed = Signal(DreamDocument)

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self._documents: List[DreamDocument] = []
        self._active_document: Optional[DreamDocument] = None

    @property
    def active_document(self) -> Optional[DreamDocument]:
        return self._active_document

    @Slot(DreamResult)
    def add_generated_image(self, result: DreamResult):
        document = self._active_document
        if document:
            document.set_images(result.dream_image, result.final_image, result.raw_image)
        else:
            new_document = DreamDocument()
            new_document.set_images(result.dream_image, result.final_image, result.raw_image)
            self.add_document(new_document)

    def add_document(self, document: DreamDocument):
        document.setParent(self)
        document.changed.connect(self._document_changed)
        self._documents.append(document)
        self.document_added.emit(document)
        self.set_active_document(document)

    def set_active_document(self, document: DreamDocument):
        self._active_document = document
        self.active_document_changed.emit(document)

    @Slot(DreamDocument)
    def _document_changed(self, document: DreamDocument):
        if document is self.active_document:
            self.active_document_changed.emit(document)

        
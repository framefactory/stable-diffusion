from typing import Optional, Union, List, cast

from PySide6.QtCore import QObject, Signal, Slot

from ui.data import DreamSequence

from .dreamer import DreamResult
from .dream_still_document import DreamStillDocument


class Documents(QObject):
    document_added = Signal(DreamStillDocument)
    active_document_changed = Signal(DreamStillDocument)

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self._base_path = "library"
        self._documents: List[DreamStillDocument] = []
        self._active_document: Optional[DreamStillDocument] = None

    @property
    def active_document(self) -> Optional[DreamStillDocument]:
        return self._active_document

    @Slot(DreamResult)
    def add_generated_frame(self, result: DreamResult):
        document = self._active_document
        assert(document)
        document.add_generated_frame(result)

    @Slot()
    def new_document(self):
        self.add_document(DreamStillDocument(self._base_path))

    def add_document(self, document: DreamStillDocument):
        document.setParent(self)
        document.changed.connect(self._document_changed)
        self._documents.append(document)
        self.document_added.emit(document)
        self.set_active_document(document)

    def set_active_document(self, document: DreamStillDocument):
        self._active_document = document
        self.active_document_changed.emit(document)

    @Slot(DreamStillDocument)
    def _document_changed(self, document: DreamStillDocument):
        if document is self.active_document:
            self.active_document_changed.emit(document)

        
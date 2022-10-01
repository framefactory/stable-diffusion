from typing import Optional, Union, List, cast

from PySide6.QtCore import QObject, Signal, Slot

from .dreamer import DreamResult
from .dream_document import DreamDocument
from .dream_image_document import DreamImageDocument
from .dream_sequence_document import DreamSequenceDocument


class Documents(QObject):
    image_added = Signal(DreamImageDocument)
    sequence_added = Signal(DreamSequenceDocument)
    active_document_changed = Signal(DreamDocument)

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.images: List[DreamImageDocument] = []
        self.sequences: List[DreamSequenceDocument] = []

        self._active_document: Optional[DreamDocument] = None

    @property
    def active_document(self) -> Optional[DreamDocument]:
        return self._active_document

    @Slot(DreamResult)
    def add_generated_image(self, result: DreamResult):
        document = self._active_document
        if isinstance(document, DreamImageDocument):
            document.dream_image = result.dream_image
            document.set_images(result.final_image, result.raw_image)
        else:
            new_document = DreamImageDocument(result.dream_image)
            new_document.set_images(result.final_image, result.raw_image)
            self.add_image_document(new_document)   

    def add_image_document(self, document: DreamImageDocument):
        document.setParent(self)
        document.changed.connect(self._image_document_changed)
        self.images.append(document)
        self.image_added.emit(document)
        self.set_active_document(document)

    def add_sequence_document(self, document: DreamSequenceDocument):
        document.setParent(self)
        document.changed.connect(self._sequence_document_changed)
        self.sequences.append(document)
        self.sequence_added.emit(document)
        self.set_active_document(document)

    def set_active_document(self, document: DreamDocument):
        self._active_document = document
        self.active_document_changed.emit(document)

    @Slot(DreamImageDocument)
    def _image_document_changed(self, document: DreamImageDocument):
        if document is self.active_document:
            self.active_document_changed.emit(document)

    @Slot(DreamSequenceDocument)
    def _sequence_document_changed(self, document: DreamSequenceDocument):
        if document is self.active_document:
            self.active_document_changed.emit(document)

        
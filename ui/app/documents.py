from typing import Optional, Union, List, cast

from PySide6.QtCore import QObject, Signal, Slot

from .dreamer import FrameResult
from .dream_document import DreamDocument
from .dream_image import DreamImage
from .dream_sequence import DreamSequence


class Documents(QObject):
    image_added = Signal(DreamImage)
    sequence_added = Signal(DreamSequence)
    active_document_changed = Signal(DreamDocument)

    def __init__(self, parent: QObject):
        super().__init__(parent)

        self.images: List[DreamImage] = []
        self.sequences: List[DreamSequence] = []

        self._active_document: Optional[DreamDocument] = None

    @property
    def active_document(self) -> Optional[DreamDocument]:
        return self._active_document

    @Slot(FrameResult)
    def add_frame(self, result: FrameResult):
        document = self._active_document
        if isinstance(document, DreamImage):
            document.frame = result.frame
            document.set_images(result.final_image, result.raw_image)
        else:
            new_document = DreamImage(result.frame)
            new_document.set_images(result.final_image, result.raw_image)
            self.add_image_document(new_document)   

    def add_image_document(self, image: DreamImage):
        print("add image document")
        image.setParent(self)
        self.images.append(image)
        self.image_added.emit(image)
        self.set_active_document(image)

    def add_sequence_document(self, sequence: DreamSequence):
        sequence.setParent(self)
        self.sequences.append(sequence)
        self.sequence_added.emit(sequence)
        self.set_active_document(sequence)

    def set_active_document(self, document: DreamDocument):
        print("set active document")
        self._active_document = document
        self.active_document_changed.emit(document)


        
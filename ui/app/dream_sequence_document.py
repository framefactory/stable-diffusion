from typing import List, Optional
from copy import copy

from PIL import Image as PIL_Image
from PIL.Image import Image

from ui.data import DreamSequence

from .dream_document import DreamDocument


class DreamSequenceDocument(DreamDocument):
    def __init__(self, dream_sequence: DreamSequence = DreamSequence()):
        super().__init__()
        self.dream_sequence = dream_sequence

    def to_dict(self) -> dict:
        data = self.dream_sequence.to_dict()
        data["rating"] = self.rating
        data["tags"] = copy(self.tags)
        return data

    @staticmethod
    def from_dict(data: dict) -> 'DreamSequenceDocument':
        document = DreamSequenceDocument(DreamSequence.from_dict(data))
        document.rating = data["rating"]
        document.tags = data["tags"]
        return document
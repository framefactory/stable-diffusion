from typing import List, Optional
from copy import copy

from PIL import Image as PIL_Image
from PIL.Image import Image

from PySide6.QtCore import QObject, Signal

from .dream_params import Dream
from .dream_document import DreamDocument


class DreamSequence(DreamDocument):
    def __init__(self, dream: Dream, rating: int = 0, tags: List[str] = []):
        super().__init__(rating, tags)
        self.dream = dream

    def to_dict(self) -> dict:
        result = self.dream.to_dict()
        result["rating"] = self.rating
        result["tags"] = copy(self.tags)
        return result

    @staticmethod
    def from_dict(params: dict):
        return DreamSequence(
            dream = Dream.from_dict(params),
            rating = params["rating"],
            tags = params["tags"]
        )
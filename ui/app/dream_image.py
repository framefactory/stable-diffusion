from typing import List, Optional
from copy import copy

from PIL import Image as PIL_Image
from PIL.Image import Image

from PySide6.QtCore import Signal

from .library import Library
from .dream_params import DreamFrame
from .dream_document import DreamDocument

class DreamImage(DreamDocument):
    def __init__(self, frame: DreamFrame, rating: int = 0, tags: List[str] = []):
        super().__init__(rating, tags)
        self.frame = frame

        self.final_image: Optional[Image] = None
        self.raw_image: Optional[Image] = None

    def set_images(self, final_image: Image, raw_image: Image):
        self.final_image = final_image
        self.raw_image = raw_image

        self.changed.emit()

    def load_images(self, library: Library):
        if self.final_image is None:
            final_image_path = library.compose_path(self.frame.path)
            self.final_image = self.load_image(final_image_path)

        if self.raw_image is None:
            raw_image_path = library.compose_path(self.frame.path, suffix=".raw")
            self.raw_image = self.load_image(raw_image_path)

        self.changed.emit()

    @staticmethod
    def load_image(abs_path: str) -> Optional[Image]:
        try:
            image = PIL_Image.open(abs_path)
            image.load()
        except:
            return None

        return image        

    def clear_images(self):
        self.final_image = None
        self.raw_image = None

    def to_dict(self) -> dict:
        result = self.frame.to_dict()
        result["rating"] = self.rating
        result["tags"] = copy(self.tags)
        return result

    @staticmethod
    def from_dict(params: dict):
        return DreamImage(
            frame = DreamFrame.from_dict(params),
            rating = params["rating"],
            tags = params["tags"]
        )

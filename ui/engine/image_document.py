from typing import List, Optional
from dataclasses import dataclass, field
from copy import copy
from pathlib import Path

from PIL import Image as PIL_Image
from PIL.Image import Image

from .parameters import ImageParams


@dataclass
class ImageDocument:
    image: Optional[Image]
    params: ImageParams
    rating: int = 0
    tags: List[str] = field(default_factory=list)

    def load_image(self, base_path: Path):
        if self.image is None:
            image_path = base_path / self.params.path
            try:
                self.image = PIL_Image.open(image_path)
                self.image.load()
            except:
                self.image = None
                print(f'failed to load image from {image_path}')

    def clear_image(self):
        self.image = None

    def to_dict(self) -> dict:
        return {
            "params": self.params.to_dict(),
            "rating": self.rating,
            "tags": copy(self.tags)
        }

    @staticmethod
    def from_dict(document: dict):
        return ImageDocument(
            image=None,
            params=ImageParams.from_dict(document["params"]),
            rating=document["rating"],
            tags=document["tags"]
        )

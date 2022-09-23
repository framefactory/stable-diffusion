from typing import List, Optional
from dataclasses import dataclass, field
from copy import copy
from pathlib import Path

from PIL import Image as PIL_Image
from PIL.Image import Image

from .params import ImageParams


@dataclass
class ImageDocument:
    image: Optional[Image]
    path: str
    params: ImageParams
    rating: int = 0
    tags: List[str] = field(default_factory=list)

    def load_image(self, base_path: Path):
        if self.image is None:
            image_path = base_path / self.path
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
            "path": self.path,
            "params": self.params.to_dict(),
            "rating": self.rating,
            "tags": copy(self.tags)
        }
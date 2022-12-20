from typing import Optional
from dataclasses import dataclass

from PIL.Image import Image

from ui.data import DreamStill

from .library import Library


@dataclass
class DreamFrame:
    still: DreamStill
    thumb_image: Optional[Image] = None
    final_image: Optional[Image] = None
    raw_image: Optional[Image] = None

    def load_images(self, base_path: str, *, force=False):
        image_path = Library.compose_path(self.still.path,
            extension=self.still.output.format, folder=base_path)

        if not self.final_image or force:
            self.final_image = Library.load_image(image_path)

        if not self.raw_image or force:
            raw_image_path = Library.compose_path(image_path, suffix=".raw")
            self.raw_image = Library.load_image(raw_image_path)

    @staticmethod
    def from_still_with_images(still: DreamStill, final_image: Image,
        raw_image: Optional[Image] = None):
        
        thumb_image = DreamFrame.make_thumb(final_image)
        return DreamFrame(still, thumb_image, final_image, raw_image)

    @staticmethod
    def from_still(base_path: str, still: DreamStill, thumb_only=True):
        image_path = Library.compose_path(still.path,
            extension=still.output.format, folder=base_path)
        image = Library.load_image(image_path)
        thumb_image = DreamFrame.make_thumb(image) if image else None
        final_image = None if thumb_only else image
        return DreamFrame(still, thumb_image, final_image)

    @staticmethod
    def make_thumb(image: Image) -> Image:
        thumb_image = image.copy()
        thumb_image.thumbnail((256, 256))
        return thumb_image
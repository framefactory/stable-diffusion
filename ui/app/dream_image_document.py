from typing import List, Optional
from copy import copy
import traceback
import json
import os

from PIL import Image as PIL_Image
from PIL.Image import Image

from ui.data import DreamImage, dream

from .library import Library
from .dream_document import DreamDocument


class DreamImageDocument(DreamDocument):
    def __init__(self, dream_image: DreamImage = DreamImage()):
        super().__init__()

        self.dream_image = dream_image
        self.final_image: Optional[Image] = None
        self.raw_image: Optional[Image] = None

    def set_images(self, final_image: Image, raw_image: Image):
        self.final_image = final_image
        self.raw_image = raw_image

        self.changed.emit(self)

    def import_images_and_data(self, path: str) -> bool:
        try:
            dream_image = None
            final_image = None
            raw_image = None

            json_path = Library.compose_path(path, extension="json")
            if os.path.exists(json_path):
                with open(json_path) as json_file:
                    data = json.load(json_file)
                    dream_image = DreamImage.from_dict(data)
                    dream_image.generator.seed_randomize = False

            extension = self.dream_image.output.format
            image_path = Library.compose_path(path, extension=extension)
            if os.path.exists(image_path):
                with PIL_Image.open(image_path) as final_image:
                    final_image.load()

            raw_image_path = Library.compose_path(image_path, suffix=".raw")
            if os.path.exists(raw_image_path):
                with PIL_Image.open(raw_image_path) as raw_image:
                    raw_image.load()

            if dream_image and final_image:
                self.dream_image = dream_image
                self.final_image = final_image
                self.raw_image = raw_image
                self.changed.emit(self)
                return True

        except:
            traceback.print_exc()
            print(f"failed to load image and/or data from: {path}")

        return False

    def load_images(self, library: Library) -> bool:
        extension = self.dream_image.output.format
        path = self.dream_image.path

        try:
            if self.final_image is None:
                final_image_path = library.compose_library_path(path, extension=extension)
                if os.path.exists(final_image_path):
                    with PIL_Image.open(final_image_path) as final_image:
                        final_image.load()
                        self.final_image = final_image

            if self.raw_image is None:
                raw_image_path = library.compose_library_path(path, suffix=".raw", extension=extension)
                if os.path.exists(raw_image_path):
                    with PIL_Image.open(raw_image_path) as raw_image:
                        raw_image.load()
                        self.raw_image = raw_image

            self.changed.emit(self)
            return True

        except:
            print(f"failed to load image(s) from: {path}")

        return False

    def clear_images(self):
        self.final_image = None
        self.raw_image = None

    def to_dict(self) -> dict:
        data = self.dream_image.to_dict()
        data["rating"] = self.rating
        data["tags"] = copy(self.tags)
        return data

    @staticmethod
    def from_dict(data: dict) -> 'DreamImageDocument':
        document = DreamImageDocument(DreamImage.from_dict(data))
        document.rating = data["rating"]
        document.tags = data["tags"]
        return document

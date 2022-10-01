from typing import List, Any, Optional
from copy import copy
import traceback
import json
import os

from PIL import Image as PIL_Image
from PIL.Image import Image
from PySide6.QtCore import QObject, Signal

from ui.data import DreamImage, DreamSequence, GeneratorKey

from .library import Library


class DreamDocument(QObject):
    changed = Signal(QObject)

    def __init__(self, dream_sequence: DreamSequence = DreamSequence()):
        super().__init__()

        self._dream_sequence = dream_sequence

        self._current_frame = 0
        self._current_generator = dream_sequence.interpolate(self._current_frame)

        self._final_image: Optional[Image] = None
        self._raw_image: Optional[Image] = None

    def set_images(self, dream_image: DreamImage, final_image: Image, raw_image: Image):
        self._dream_sequence.path = dream_image.path
        self._dream_sequence.output = dream_image.output
        self._dream_sequence.keys = [ GeneratorKey(0, dream_image.generator) ]

        self._final_image = final_image
        self._raw_image = raw_image

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

            extension = self._dream_sequence.output.format
            image_path = Library.compose_path(path, extension=extension)
            if os.path.exists(image_path):
                with PIL_Image.open(image_path) as final_image:
                    final_image.load()

            raw_image_path = Library.compose_path(image_path, suffix=".raw")
            if os.path.exists(raw_image_path):
                with PIL_Image.open(raw_image_path) as raw_image:
                    raw_image.load()

            if dream_image and final_image:
                self._dream_sequence = DreamSequence(
                    path = dream_image.path,
                    length = 1,
                    keys = [ GeneratorKey(0, dream_image.generator )],
                    output = dream_image.output
                )
                self._dream_image = dream_image
                self._final_image = final_image
                self._raw_image = raw_image
                self.changed.emit(self)
                return True

        except:
            traceback.print_exc()
            print(f"failed to load image and/or data from: {path}")

        return False

    def clear_images(self):
        self.final_image = None
        self.raw_image = None

    def to_dict(self):
        data = self._dream_sequence.to_dict()
        return data

    @staticmethod
    def from_dict(data: dict) -> 'DreamDocument':
        sequence = DreamSequence.from_dict(data)
        document = DreamDocument(sequence)
        return document

    @staticmethod
    def from_dream_image(dream_image: DreamImage) -> 'DreamDocument':
        key = GeneratorKey(0, dream_image.generator)
        sequence = DreamSequence(output=dream_image.output, keys=[ key ])
        document = DreamDocument(sequence)
        return document
from typing import List, Optional
from enum import Enum
import json
import os

from PySide6.QtCore import QObject, Signal

from ui.data import (
    GeneratorSettings,
    OutputSettings,
    DreamStill,
    DreamSequence,
    GeneratorKey
)

from .library import Library
from .dreamer import DreamResult
from .dream_frame import DreamFrame

# class DreamDocumentChange(Enum):
#     all = "all"
#     current = "current"
#     history = "history"

class DreamDocument(QObject):
    changed = Signal()

    def __init__(self, base_path: str, sequence = DreamSequence(),
        history: List[DreamFrame] = []):

        super().__init__()

        self._base_path = base_path
        self._sequence = sequence

        first_key = sequence.keys[0]
        self._generator = first_key.generator
        self._frame = first_key.frame
        self._begin = 0
        self._end = sequence.count

        # history of generated frames
        self._history: List[DreamFrame] = []

        # the active frame from history
        self._active_index: int = -1
        self._active_frame: Optional[DreamFrame] = None

    @property
    def path(self) -> str:
        return self._sequence.path

    @property
    def output(self) -> OutputSettings:
        return self._sequence.output

    @property
    def generator(self) -> GeneratorSettings:
        return self._generator

    @property
    def active_frame(self) -> Optional[DreamFrame]:
        return self._active_frame

    @property
    def history_size(self) -> int:
        return len(self._history)

    def set_frame_current(self, index: int, *, force=False):
        frame = self._history[index]
        if frame.final_image is None:
            frame.load_images(self._base_path, force=force)

        self._active_frame = frame
        self._active_index = index
        self.changed.emit()

    def add_generated_frame(self, result: DreamResult):
        self.add_frame(result.still, result.final_image, result.raw_image)

    def add_frame(self, still: DreamStill, final_image: Image,
        raw_image: Optional[Image] = None):

        still.generator.seed_a_randomize = False
        still.generator.seed_b_randomize = False

        frame = DreamFrame.from_still_with_images(still, final_image, raw_image)
        index = self.history_size
        self._history.append(frame)
        self.set_frame_current(index)

    def import_frame(self, path: str) -> bool:
        still = None
        final_image = None
        raw_image = None

        json_path = Library.compose_path(path, extension="json")
        try:
            with open(json_path) as json_file:
                data = json.load(json_file)
                still = DreamStill.from_dict(data)
        except:
            print(f"failed to open json file: {json_path}")
            return False

        base_path = os.path.dirname(json_path)
        image_path = Library.compose_path(base_path, extension=still.output.format)
        final_image = Library.load_image(image_path)
        if final_image is None:
            return False

        raw_image_path = Library.compose_path(image_path, suffix=".raw")
        raw_image = Library.load_image(raw_image_path)

        self.add_frame(still, final_image, raw_image)
        return True

    def clear_image_cache(self):
        for frame in self._history:
            frame.final_image = None
            frame.raw_image = None

    def to_dict(self) -> dict:
        return {
            "history": [ frame.still.to_dict() for frame in self._history ]
        }

    @staticmethod
    def from_dict(base_path: str, data: dict) -> 'DreamDocument':
        document = DreamDocument(base_path)

        stills = [ DreamStill.from_dict(s) for s in data["history"]]
        document._history = [ DreamFrame.from_still(base_path, still) for still in stills ]
        if document.history_size > 0:
            document.set_frame_current(0)

        return document

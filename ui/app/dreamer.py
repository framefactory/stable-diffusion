from typing import cast, Optional, Union
from dataclasses import dataclass
from copy import deepcopy
from enum import Enum
from queue import Queue
import os
import json
import traceback

import torch
from PIL.Image import Image

from PySide6.QtCore import QObject, QThread, Signal

from ui.data import Preferences, DreamStill, DreamSequence, GeneratorSettings

from .generator import Generator
from .library import Library


class DreamerState(Enum):
    READY = 0
    DREAMING = 1
    LOADING = 2


@dataclass
class DreamProgress:
    state: DreamerState
    text: str
    step: int = 0
    total_steps: int = 0
    frame: int = 0
    total_frames: int = 0


@dataclass
class DreamResult:
    still: DreamStill
    final_image: Image
    raw_image: Image


Dream = Union[DreamStill, DreamSequence]


class Dreamer(QThread):
    image_ready = Signal(DreamResult)
    progress_update = Signal(DreamProgress)

    def __init__(self, parent: QObject, preferences: Preferences, library: Library):
        super().__init__(parent)

        self._library = library
        self._generator = Generator(preferences.model_params, self._cb_sequence_step)
        self._queue: Queue[Dream] = Queue()
        self._current_dream: Optional[Dream] = None
        self._current_generator: Optional[GeneratorSettings] = None
        self._current_frame: int = 0
        self._cancel_requested = False
        self._stop_requested = False

    def dream(self, dream: Dream):
        self._queue.put(deepcopy(dream))

    def run(self):
        self._set_state(DreamerState.LOADING, "Loading Models...")
        self._generator.load()
        self._set_state(DreamerState.READY, "Ready.")

        while(not self._stop_requested):
            try:
                dream = self._queue.get(block=True, timeout=0.25)
            except:
                continue

            self._current_dream = dream
            self._set_state(DreamerState.DREAMING, "Dreaming...")

            try:
                if not dream.path:
                    dream.path = Library.generate_file_path()

                if type(dream) is DreamStill:
                    self._current_generator = dream.generator
                    self._current_frame = 0

                    dream_image = DreamStill(dream.path, dream.generator, dream.output)
                    final_image, raw_image = self._generator.generate(dream_image)
                    result = self._save_generated(dream_image, final_image, raw_image)
                    self.image_ready.emit(result)

                elif type(dream) is DreamSequence:
                    for frame_index in range(dream.length):
                        if self._cancel_requested:
                            break

                        self._current_generator = dream.interpolate(frame_index)
                        self._current_frame = frame_index

                        root, ext = os.path.splitext(dream.path)
                        file_path = f"{root}_{frame_index:04}{ext}"

                        dream_image = DreamStill(file_path, self._current_generator, dream.output)
                        final_image, raw_image = self._generator.generate(dream_image)
                        result = self._save_generated(dream_image, final_image, raw_image)
                        self.image_ready.emit(result)

            except Exception as e:
                traceback.print_exc()

            self._set_state(DreamerState.READY, "Ready.")
            self._queue.task_done()

    def stop(self):
        self._stop_requested = True
        self.wait()

    def _cb_sequence_step(self, gpu_data: torch.Tensor, step: int):
        dream = cast(Dream, self._current_dream)
        generator = cast(GeneratorSettings, self._current_generator)
        progress = None

        if type(dream) is DreamStill:
            progress = DreamProgress(DreamerState.DREAMING, "Dreaming...",
                step, generator.steps)

        elif type(dream) is DreamSequence:
            text = ("Dreaming..." if dream.length == 1
                else f"Dreaming {self._current_frame + 1} of {dream.length}...")
            progress = DreamProgress(DreamerState.DREAMING, text, step, generator.steps,
                self._current_frame, dream.length)

        self.progress_update.emit(progress)

    def _set_state(self, state: DreamerState, text: str):
        progress = DreamProgress(state, text)
        self.progress_update.emit(progress)

    def _save_generated(self, dream: DreamStill, final_image: Image, raw_image: Image) -> DreamResult:
        image_ext = dream.output.format

        final_file_path = self._library.compose_library_path(dream.path, extension=image_ext)
        final_image.save(final_file_path)

        if raw_image != final_image:
            raw_file_path = self._library.compose_library_path(dream.path, suffix=".raw", extension=image_ext)
            raw_image.save(raw_file_path)

        json_file_path = self._library.compose_library_path(dream.path, extension="json")

        with open(json_file_path, "w") as json_file:
            json.dump(dream.to_dict(), json_file, indent=4)

        return DreamResult(dream, final_image, raw_image)


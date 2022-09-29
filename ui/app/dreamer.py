from typing import cast, Optional
from dataclasses import dataclass
from enum import Enum
from queue import Queue
import os
import json
import traceback

import torch
from PIL.Image import Image

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal
)

from ui.data import Preferences, DreamVariables

from .dream_params import Dream, DreamFrame
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
class FrameResult:
    frame: DreamFrame
    final_image: Image
    raw_image: Image
    

class Dreamer(QThread):
    frame_ready = Signal(FrameResult)
    progress_update = Signal(DreamProgress)

    def __init__(self, parent: QObject, preferences: Preferences, library: Library):
        super().__init__(parent)

        self._library = library
        self._generator = Generator(preferences.model_params, self._cb_sequence_step)
        self._queue: Queue[Dream] = Queue()
        self._current_dream: Optional[Dream] = None
        self._current_variables: Optional[DreamVariables] = None
        self._current_frame: int = 0
        self._cancel_requested = False
        self._stop_requested = False

    def add_dream(self, dream: Dream):
        self._queue.put(dream)

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
                    dream.path = Library.generate_file_path(".png")

                for frame in range(dream.length):
                    if self._cancel_requested:
                        break

                    variables = dream.interpolate(frame)
                    self._current_variables = variables
                    self._current_frame = frame

                    file_path = dream.path
                    if dream.length > 1:
                        root, ext = os.path.splitext(file_path)
                        file_path = f"{root}-{frame:04}{ext}"

                    frame = DreamFrame(file_path, dream.constants, variables)
                    final_image, raw_image = self._generator.generate(frame)
                    result = self._save_generated(frame, final_image, raw_image)
                    self.frame_ready.emit(result)

            except Exception as e:
                traceback.print_exc()

            self._set_state(DreamerState.READY, "Ready.")
            self._queue.task_done()

    def stop(self):
        self._stop_requested = True
        self.wait()

    def _cb_sequence_step(self, gpu_data: torch.Tensor, step: int):
        dream = cast(Dream, self._current_dream)
        variables = cast(DreamVariables, self._current_variables)

        text = ("Dreaming..." if dream.length == 1
            else f"Dreaming {self._current_frame + 1} of {dream.length}...")

        progress = DreamProgress(DreamerState.DREAMING, text, step, variables.steps,
            self._current_frame, dream.length)

        self.progress_update.emit(progress)

    def _set_state(self, state: DreamerState, text: str):
        progress = DreamProgress(state, text)
        self.progress_update.emit(progress)

    def _save_generated(self, frame: DreamFrame, final_image: Image, raw_image: Image) -> FrameResult:
        file_path = self._library.compose_path(frame.path)
        final_image.save(file_path)

        if raw_image != final_image:
            raw_file_path = self._library.compose_path(frame.path, suffix=".raw")
            raw_image.save(raw_file_path)

        json_file_path = self._library.compose_path(frame.path, extension=".json")

        with open(json_file_path, "w") as json_file:
            json.dump(frame.to_dict(), json_file, indent=4)

        return FrameResult(frame, final_image, raw_image)


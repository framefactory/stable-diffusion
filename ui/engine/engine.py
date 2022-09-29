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

from .jobs import Job, ImageJob, SequenceJob
from .preferences import Preferences
from .parameters import ContentParams, ImageParams
from .image_document import ImageDocument
from .generator import Generator
from .utils import generate_file_name_now

class EngineState(Enum):
    READY = "Ready"
    DREAMING = "Dreaming..."
    LOADING = "Loading Models..."

@dataclass
class EngineProgress:
    state: EngineState
    step: int = 0
    total_steps: int = 0
    frame: int = 0
    total_frames: int = 0

class Engine(QThread):
    image_ready = Signal(ImageDocument)
    progress_update = Signal(EngineProgress)

    def __init__(self, parent: QObject, preferences: Preferences):
        super().__init__(parent)

        self._library_path = preferences.library_path
        self._generator = Generator(preferences.model_params)
        self._queue: Queue[Job] = Queue()
        self._current_job: Optional[Job] = None
        self._current_content: Optional[ContentParams] = None
        self._current_frame: int = 0
        self._cancel_requested = False
        self._stop_requested = False

    def post_job(self, job: Job):
        self._queue.put(job)

    def run(self):
        self._set_state(EngineState.LOADING)
        self._generator.load()
        self._set_state(EngineState.READY)

        while(not self._stop_requested):
            try:
                job = self._queue.get(block=True, timeout=0.25)
            except:
                continue

            self._current_job = job
            self._set_state(EngineState.DREAMING)

            try:
                if job.type == ImageJob.type:
                    job = cast(ImageJob, job)
                    self._current_content = job.params.content

                    if not job.params.path:
                        job.params.path = generate_file_name_now(".png")

                    image = self._generator.generate(job.params, self._cb_image_step)
                    document = self._save_generated(image, job.params)
                    self.image_ready.emit(document)

                elif job.type == SequenceJob.type:
                    job = cast(SequenceJob, job)

                    if not job.params.path:
                        job.params.path = generate_file_name_now(".png")

                    for frame in range(job.params.length):
                        if self._cancel_requested:
                            break

                        content = job.get_interpolated_content(frame)
                        self._current_content = content
                        self._current_frame = frame

                        root, ext = os.path.splitext(job.params.path)
                        path = f"{root}-{frame:04}{ext}"
                        params = ImageParams(path, job.params.format, content)
                        image = self._generator.generate(params, self._cb_sequence_step)
                        document = self._save_generated(image, params)
                        self.image_ready.emit(document)

            except Exception as e:
                traceback.print_exc()

            self._set_state(EngineState.READY)
            self._queue.task_done()

    def stop(self):
        self._stop_requested = True
        self.wait()

    def _cb_image_step(self, gpu_data: torch.Tensor, step: int):
        content = cast(ContentParams, self._current_content)
        progress = EngineProgress(EngineState.DREAMING, step, content.steps)
        self.progress_update.emit(progress)

    def _cb_sequence_step(self, gpu_data: torch.Tensor, step: int):
        job = cast(SequenceJob, self._current_job)
        content = cast(ContentParams, self._current_content)
        progress = EngineProgress(EngineState.DREAMING, step, content.steps,
            self._current_frame, job.params.length)
        self.progress_update.emit(progress)

    def _set_state(self, state: EngineState):
        progress = EngineProgress(state)
        self.progress_update.emit(progress)

    def _save_generated(self, image: Image, params: ImageParams) -> ImageDocument:
        file_path = os.path.join(self._library_path, params.path)
        image.save(file_path)

        file_base, _ = os.path.splitext(file_path)
        document_path = f"{file_base}.json"
        document = ImageDocument(image, params)
        with open(document_path, "w") as json_file:
            json.dump(document.to_dict(), json_file, indent=4)

        return document


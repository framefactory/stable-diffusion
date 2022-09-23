from typing import Optional
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from queue import Queue
from threading import Thread
from queue import Queue

import torch
from ldm.generate import Generate

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot
)

from .params import ModelParams, ImageParams, ImageResult

class EngineState(Enum):
    READY = "Ready"
    CALCULATING = "Calculating"
    LOADING = "Loading"

@dataclass
class EngineProgress:
    state: EngineState
    percent: int
    params: Optional[ImageParams]


class Engine(QThread):
    image_ready = Signal(ImageResult)
    progress_update = Signal(EngineProgress)

    def __init__(self, parent: QObject, params = ModelParams()):
        super().__init__(parent)

        self._pipeline = Generate(**params.to_dict())
        self._queue: Queue[ImageParams] = Queue()
        self._params: Optional[ImageParams] = None
        self._stop_requested = False

    def generate(self, params: ImageParams):
        self._queue.put(deepcopy(params))

    def run(self):
        self._set_state(EngineState.LOADING, 0)
        self._pipeline.load_model()
        self._set_state(EngineState.READY, 0)

        while(not self._stop_requested):
            try:
                params = self._queue.get(block=True, timeout=0.25)
            except:
                continue

            self._params = params
            self._set_state(EngineState.CALCULATING, 0)

            result = self._pipeline.prompt2image(
                step_callback=self._step_callback,
                **params.to_dict()
            )

            params.seed = result[0][1]
            result = ImageResult(params, result[0][0])
            self.image_ready.emit(result) # type:ignore

            self._set_state(EngineState.READY, 0)
            self._queue.task_done()

    def stop(self):
        self._stop_requested = True
        self.wait()

    def _step_callback(self, gpu_data: torch.Tensor, step: int):
        progress = step / (self._params.steps - 1) if self._params else 0
        self._set_state(EngineState.CALCULATING, int(progress * 100))

    def _set_state(self, state: EngineState, percent: int):
        progress = EngineProgress(state, percent, self._params)
        self.progress_update.emit(progress) # type:ignore


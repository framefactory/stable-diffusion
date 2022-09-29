from typing import Optional
import random

from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QPushButton,
    QVBoxLayout,
)

from ui.engine import (
    ImageParams,
    Sampler
)

from .controls import (
    SliderControl, 
    ComboControl, 
    CheckBoxControl, 
    SeedControl
)

class SettingsPanel(QDockWidget):
    generate = Signal(int)

    def __init__(self, params: ImageParams):
        super().__init__("Settings", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.iterations = 1
        self.params = params

        main_layout = QVBoxLayout()

        self._seed_control = SeedControl("Seed")
        self._seed_control.changed.connect(self._seed_changed)
        main_layout.addWidget(self._seed_control)

        self._steps_control = SliderControl("Steps", 1, 200, 1, 0)
        self._steps_control.changed.connect(self._steps_changed)
        main_layout.addWidget(self._steps_control)

        self._cfg_control = SliderControl("CFG Scale", 1, 20, 0.1, 1)
        self._cfg_control.changed.connect(self._cfg_changed)
        main_layout.addWidget(self._cfg_control)

        self._image_strength_control = SliderControl("Input Image Strength", 0, 1, 0.01, 2)
        self._image_strength_control.changed.connect(self._image_strength_changed)
        main_layout.addWidget(self._image_strength_control)

        self._feedback_strength_control = SliderControl("Feedback Image Strength", 0, 1, 0.01, 2)
        self._feedback_strength_control.changed.connect(self._image_feedback_changed)
        main_layout.addWidget(self._feedback_strength_control)

        samplers = [ s.value for s in Sampler ]
        sampler_labels = [ s.label for s in Sampler ]
        self._sampler_control = ComboControl("Sampler", samplers, sampler_labels)
        self._sampler_control.changed.connect(self._sampler_changed)
        main_layout.addWidget(self._sampler_control)

        self._eta_control = SliderControl("DDIM Eta", 0, 1, 0.01, 2)
        self._eta_control.setEnabled(False)
        self._eta_control.changed.connect(self._eta_changed)
        main_layout.addWidget(self._eta_control)

        self._width_control = SliderControl("Image Width", 256, 1024, 64)
        self._width_control.changed.connect(self._width_changed)
        main_layout.addWidget(self._width_control)

        self._height_control = SliderControl("Image Height", 256, 1024, 64)
        self._height_control.changed.connect(self._height_changed)
        main_layout.addWidget(self._height_control)

        self._upscale_factor_control = ComboControl("Upscaling Factor", [ "Off", "2x", "4x" ])
        self._upscale_factor_control.changed.connect(self._upscale_factor_changed)
        main_layout.addWidget(self._upscale_factor_control)

        self._upscale_strength_control = SliderControl("Upscaling Strength", 0, 1, 0.01, 2)
        self._upscale_strength_control.changed.connect(self._upscale_strength_changed)
        main_layout.addWidget(self._upscale_strength_control)

        self._seamless_control = CheckBoxControl("Seamless")
        self._seamless_control.changed.connect(self._seamless_changed)
        main_layout.addWidget(self._seamless_control)

        self._iterations_control = SliderControl("Iterations", 1, 1000, 1, 0)
        self._iterations_control.changed.connect(self._iterations_changed)
        main_layout.addWidget(self._iterations_control)

        command_layout = QVBoxLayout()
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self._generate_clicked) #type:ignore
        command_layout.addWidget(generate_button)

        main_layout.addStretch(1)
        main_layout.addLayout(command_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

        self.update()

    def update(self, params: Optional[ImageParams] = None):
        if params:
            self.params = params

        format = self.params.format
        content = self.params.content

        self._seed_control.value = content.seed
        self._steps_control.value = content.steps
        self._cfg_control.value = content.cfg_scale
        self._image_strength_control.value = content.image_strength
        self._feedback_strength_control.value = content.feedback_strength
        self._sampler_control.option = content.sampler
        self._eta_control.value = content.ddim_eta
        self._width_control.value = format.width
        self._height_control.value = format.height
        self._seamless_control.checked = format.seamless
        self._upscale_factor_control.index = max(0, int(format.upscale_factor) - 1)
        self._upscale_strength_control.value = format.upscale_strength
        self._iterations_control.value = self.iterations


    def sizeHint(self) -> QSize:
        return QSize(380, 640)

    @Slot()
    def _seed_changed(self, value: int):
        self.params.content.seed = value

    @Slot()
    def _steps_changed(self, value: float):
        self.params.content.steps = int(value)

    @Slot()
    def _cfg_changed(self, value: float):
        self.params.content.cfg_scale = value

    @Slot()
    def _image_strength_changed(self, value: float):
        self.params.content.image_strength = value

    @Slot()
    def _image_feedback_changed(self, value: float):
        self.params.content.feedback_strength = value

    @Slot()
    def _eta_changed(self, value: float):
        self.params.content.ddim_eta = value

    @Slot()
    def _sampler_changed(self, index: int):
        sampler_name = self._sampler_control.option
        self.params.content.sampler = sampler_name

        if sampler_name == "ddim":
            self._eta_control.setEnabled(True)
        else:
            self._eta_control.value = 0
            self._eta_control.setEnabled(False)

    @Slot()
    def _width_changed(self, value: float):
        self.params.format.width = int(value)

    @Slot()
    def _height_changed(self, value: float):
        self.params.format.height = int(value)

    @Slot()
    def _upscale_factor_changed(self, index: int):
        self.params.format.upscale_factor = index * 2

    @Slot()
    def _upscale_strength_changed(self, value: float):
        self.params.format.upscale_strength = value

    @Slot()
    def _seamless_changed(self, value: bool):
        self.params.format.seamless = value

    @Slot()
    def _iterations_changed(self, value: float):
        self.iterations = int(value)

    @Slot()
    def _generate_clicked(self):
        self.generate.emit(self.iterations) #type:ignore
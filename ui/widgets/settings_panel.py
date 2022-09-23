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

from ui.engine import ImageParams, Sampler

from .controls import (
    SliderControl, 
    ComboControl, 
    CheckBoxControl, 
    SeedControl
)

class SettingsPanel(QDockWidget):
    generate = Signal()

    def __init__(self, params: ImageParams):
        super().__init__("Settings", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

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

        self._strength_control = SliderControl("Input Image Strength", 0, 1, 0.01, 2)
        self._strength_control.changed.connect(self._image_strength_changed)
        main_layout.addWidget(self._strength_control)

        samplers = [ s.value for s in Sampler]
        self._sampler_control = ComboControl("Sampler", samplers)
        self._sampler_control.changed.connect(self._sampler_changed)
        main_layout.addWidget(self._sampler_control)

        self._eta_control = SliderControl("DDIM Eta", 0, 1, 0.01, 2)
        self._eta_control.setEnabled(False)
        self._eta_control.changed.connect(self._eta_changed)
        main_layout.addWidget(self._eta_control)

        self._skipnorm_control = CheckBoxControl("Skip Normalize")
        self._skipnorm_control.changed.connect(self._skipnorm_changed)
        main_layout.addWidget(self._skipnorm_control)

        self._logtoken_control = CheckBoxControl("Log Tokenization")
        self._logtoken_control.changed.connect(self._logtoken_changed)
        main_layout.addWidget(self._logtoken_control)

        self._width_control = SliderControl("Image Width", 256, 1024, 64)
        self._width_control.changed.connect(self._width_changed)
        main_layout.addWidget(self._width_control)

        self._height_control = SliderControl("Image Height", 256, 1024, 64)
        self._height_control.changed.connect(self._height_changed)
        main_layout.addWidget(self._height_control)

        self._upscale_control = ComboControl("Upscaling", [ "Off", "2x", "4x" ])
        self._upscale_control.changed.connect(self._upscaling_changed)
        main_layout.addWidget(self._upscale_control)

        self._seamless_control = CheckBoxControl("Seamless")
        self._seamless_control.changed.connect(self._seamless_changed)
        main_layout.addWidget(self._seamless_control)

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

        self._seed_control.value = self.params.seed
        self._steps_control.value = self.params.steps
        self._cfg_control.value = self.params.cfg_scale
        self._strength_control.value = 1 - self.params.strength
        self._sampler_control.option = self.params.sampler_name
        self._eta_control.value = self.params.ddim_eta
        self._skipnorm_control.checked = self.params.skip_normalize
        self._logtoken_control.checked = self.params.log_tokenization
        self._width_control.value = self.params.width
        self._height_control.value = self.params.height
        self._seamless_control.checked = self.params.seamless

        if self.params.upscale is None:
            self._upscale_control.index = 0
        elif self.params.upscale == 2:
            self._upscale_control.index = 1
        else:
            self._upscale_control.index = 2

    def sizeHint(self) -> QSize:
        return QSize(380, 640)

    @Slot()
    def _seed_changed(self, value: int):
        self.params.seed = value

    @Slot()
    def _steps_changed(self, value: float):
        self.params.steps = int(value)

    @Slot()
    def _cfg_changed(self, value: float):
        self.params.cfg_scale = value

    @Slot()
    def _image_strength_changed(self, value: float):
        self.params.strength = 1 - value

    @Slot()
    def _eta_changed(self, value: float):
        self.params.ddim_eta = value

    @Slot()
    def _skipnorm_changed(self, value: bool):
        self.params.skip_normalize = value

    @Slot()
    def _logtoken_changed(self, value: bool):
        self.params.log_tokenization = value

    @Slot()
    def _sampler_changed(self, index: int):
        option = self._sampler_control.option
        self.params.sampler_name = option

        if option == "ddim":
            self._eta_control.setEnabled(True)
        else:
            self._eta_control.value = 0
            self._eta_control.setEnabled(False)

    @Slot()
    def _width_changed(self, value: float):
        self.params.width = int(value)

    @Slot()
    def _height_changed(self, value: float):
        self.params.height = int(value)

    @Slot()
    def _upscaling_changed(self, index: int):
        if index == 0:
            self.params.upscale = None
        else:
            factor = index * 2
            self.params.upscale = (factor, 0.75)

    @Slot()
    def _seamless_changed(self, value: bool):
        self.params.seamless = value

    @Slot()
    def _generate_clicked(self):
        self.generate.emit() #type:ignore
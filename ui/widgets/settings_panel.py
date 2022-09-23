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
    QSlider,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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

    def __init__(self, parent: QWidget, params: ImageParams):
        super().__init__(parent)
        self.params = params
        self.setWindowTitle("Settings")

        main_layout = QVBoxLayout()

        self.seed_control = SeedControl("Seed")
        self.seed_control.changed.connect(self._seed_changed)
        main_layout.addWidget(self.seed_control)

        self.steps_control = SliderControl("Steps", 1, 200, 1, 0)
        self.steps_control.changed.connect(self._steps_changed)
        main_layout.addWidget(self.steps_control)

        self.cfg_control = SliderControl("CFG Scale", 1, 20, 0.1, 1)
        self.cfg_control.changed.connect(self._cfg_changed)
        main_layout.addWidget(self.cfg_control)

        samplers = [ s.value for s in Sampler]
        self.sampler_control = ComboControl("Sampler", samplers)
        self.sampler_control.changed.connect(self._sampler_changed)
        main_layout.addWidget(self.sampler_control)

        self.eta_control = SliderControl("DDIM Eta", 0, 1, 0.01, 2)
        self.eta_control.setEnabled(False)
        self.eta_control.changed.connect(self._eta_changed)
        main_layout.addWidget(self.eta_control)

        self.skipnorm_control = CheckBoxControl("Skip Normalize")
        self.skipnorm_control.changed.connect(self._skipnorm_changed)
        main_layout.addWidget(self.skipnorm_control)

        self.logtoken_control = CheckBoxControl("Log Tokenization")
        self.logtoken_control.changed.connect(self._logtoken_changed)
        main_layout.addWidget(self.logtoken_control)

        self.width_control = SliderControl("Image Width", 256, 1024, 64)
        self.width_control.changed.connect(self._width_changed)
        main_layout.addWidget(self.width_control)

        self.height_control = SliderControl("Image Height", 256, 1024, 64)
        self.height_control.changed.connect(self._height_changed)
        main_layout.addWidget(self.height_control)

        self.upscale_control = ComboControl("Upscaling", [ "Off", "2x", "4x" ])
        self.upscale_control.changed.connect(self._upscaling_changed)
        main_layout.addWidget(self.upscale_control)

        self.seamless_control = CheckBoxControl("Seamless")
        self.seamless_control.changed.connect(self._seamless_changed)
        main_layout.addWidget(self.seamless_control)

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

        self.seed_control.value = self.params.seed
        self.steps_control.value = self.params.steps
        self.cfg_control.value = self.params.cfg_scale
        self.sampler_control.option = self.params.sampler_name
        self.eta_control.value = self.params.ddim_eta
        self.skipnorm_control.checked = self.params.skip_normalize
        self.logtoken_control.checked = self.params.log_tokenization
        self.width_control.value = self.params.width
        self.height_control.value = self.params.height
        self.seamless_control.checked = self.params.seamless

        if self.params.upscale is None:
            self.upscale_control.index = 0
        elif self.params.upscale == 2:
            self.upscale_control.index = 1
        else:
            self.upscale_control.index = 2

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
        option = self.sampler_control.option
        self.params.sampler_name = option

        if option == "ddim":
            self.eta_control.setEnabled(True)
        else:
            self.eta_control.value = 0
            self.eta_control.setEnabled(False)

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
        if self.seed_control.auto_generate:
            self.seed_control.generate()

        for key, value in self.params.to_dict().items():
            print(f'{key}: {value}')
        self.generate.emit() #type:ignore
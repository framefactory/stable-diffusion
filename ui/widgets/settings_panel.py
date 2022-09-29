from PySide6.QtCore import (
    QSize,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QVBoxLayout,
)

from ui.data import (
    DreamConstants,
    DreamVariables,
    Sampler
)

from .controls import (
    SliderControl, 
    ComboControl, 
    CheckBoxControl,
    SeedControl
)

class SettingsPanel(QDockWidget):
    def __init__(self, constants: DreamConstants, variables: DreamVariables):
        super().__init__("Settings", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self._constants = constants
        self._variables = variables

        main_layout = QVBoxLayout()

        self._seed_a_control = SeedControl("Seed A")
        self._seed_a_control.changed.connect(self._seed_a_changed)
        self._seed_a_control.randomize_changed.connect(self._seed_a_randomize_changed)
        main_layout.addWidget(self._seed_a_control)

        self._seed_b_control = SeedControl("Seed B")
        self._seed_b_control.changed.connect(self._seed_b_changed)
        self._seed_b_control.randomize_changed.connect(self._seed_b_randomize_changed)
        main_layout.addWidget(self._seed_b_control)

        self._seed_blend_control = SliderControl("Seed Blend A/B", 0, 1, 0.01, 2)
        self._seed_blend_control.changed.connect(self._seed_blend_changed)
        main_layout.addWidget(self._seed_blend_control)

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

        self._face_strength_control = SliderControl("Face Reconstruction Strength", 0, 1, 0.01, 2)
        self._face_strength_control.changed.connect(self._face_strength_changed)
        main_layout.addWidget(self._face_strength_control)

        self._seamless_control = CheckBoxControl("Seamless")
        self._seamless_control.changed.connect(self._seamless_changed)
        main_layout.addWidget(self._seamless_control)

        main_layout.addStretch()

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

        self.update()

    def randomize_seeds(self):
        if self._seed_a_control.randomize_enabled:
            self._seed_a_control.randomize()

        if self._seed_b_control.randomize_enabled:
            self._seed_b_control.randomize()

    def set_constants(self, constants: DreamConstants):
        self._constants = constants
        self.update()

    def set_variables(self, variables: DreamVariables):
        self._variables = variables
        self.update()

    def update(self):
        constants = self._constants
        variables = self._variables

        self._seed_a_control.value = variables.seed_a
        self._seed_b_control.value = variables.seed_b
        self._seed_blend_control.value = variables.seed_blend
        self._steps_control.value = variables.steps
        self._cfg_control.value = variables.cfg_scale
        self._image_strength_control.value = variables.image_strength
        self._feedback_strength_control.value = variables.feedback_strength
        self._sampler_control.option = variables.sampler
        self._eta_control.value = variables.ddim_eta
        self._width_control.value = constants.width
        self._height_control.value = constants.height
        self._seamless_control.checked = constants.seamless
        self._upscale_factor_control.index = max(0, int(constants.upscale_factor) - 1)
        self._upscale_strength_control.value = constants.upscale_strength
        self._face_strength_control.value = constants.gfpgan_strength
        self._seed_a_control.randomize_enabled = constants.seed_a_random
        self._seed_b_control.randomize_enabled = constants.seed_b_random


    def sizeHint(self) -> QSize:
        return QSize(380, 640)

    @Slot()
    def _seed_a_changed(self, value: int):
        self._variables.seed_a = value

    @Slot(bool)
    def _seed_a_randomize_changed(self, state: bool):
        self._constants.seed_a_random = state

    @Slot()
    def _seed_b_changed(self, value: int):
        self._variables.seed_b = value

    @Slot(bool)
    def _seed_b_randomize_changed(self, state: bool):
        self._constants.seed_b_random = state

    @Slot()
    def _seed_blend_changed(self, value: float):
        self._variables.seed_blend = value

    @Slot()
    def _steps_changed(self, value: float):
        self._variables.steps = int(value)

    @Slot()
    def _cfg_changed(self, value: float):
        self._variables.cfg_scale = value

    @Slot()
    def _image_strength_changed(self, value: float):
        self._variables.image_strength = value

    @Slot()
    def _image_feedback_changed(self, value: float):
        self._variables.feedback_strength = value

    @Slot()
    def _eta_changed(self, value: float):
        self._variables.ddim_eta = value

    @Slot()
    def _sampler_changed(self, index: int):
        sampler_name = self._sampler_control.option
        self._variables.sampler = sampler_name

        if sampler_name == "ddim":
            self._eta_control.setEnabled(True)
        else:
            self._eta_control.value = 0
            self._eta_control.setEnabled(False)

    @Slot()
    def _width_changed(self, value: float):
        self._constants.width = int(value)

    @Slot()
    def _height_changed(self, value: float):
        self._constants.height = int(value)

    @Slot()
    def _upscale_factor_changed(self, index: int):
        self._constants.upscale_factor = index * 2

    @Slot()
    def _upscale_strength_changed(self, value: float):
        self._constants.upscale_strength = value

    @Slot()
    def _face_strength_changed(self, value: float):
        self._constants.gfpgan_strength = value

    @Slot()
    def _seamless_changed(self, value: bool):
        self._constants.seamless = value

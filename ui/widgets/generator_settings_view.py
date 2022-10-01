from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.data import GeneratorSettings, Sampler

from .field_controls import (
    FieldControl,
    SliderControl,
    ComboControl,
    SeedControl
)


class GeneratorSettingsView(QWidget):
    def __init__(self, settings: GeneratorSettings):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._controls: List[FieldControl] = []

        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self._seed_control = SeedControl("Seed A",
            settings, "seed_a", "seed_randomize")
        self._add(layout, self._seed_control)

        self._add(layout, SeedControl("Seed B", 
            settings, "seed_b"))
        self._add(layout, SliderControl("Seed Blend A/B",
            settings, "seed_blend", float, 0, 1, 0.01, 2))
        self._add(layout, SliderControl("Steps",
            settings, "steps", int, 1, 200, 1, 0))
        self._add(layout, SliderControl("CFG Scale",
            settings, "cfg_scale", float, 1, 20, 0.1, 1))
        self._add(layout, SliderControl("Input Image Strength",
            settings, "image_strength", float, 0, 1, 0.01, 2))
        self._add(layout, SliderControl("Feedback Image Strength",
            settings, "feedback_strength", float, 0, 1, 0.01, 2))

        samplers = [ s.value for s in Sampler ]
        sampler_labels = [ s.label for s in Sampler ]
        self._add(layout, ComboControl("Sampler",
            settings, "sampler", samplers, sampler_labels))

        self._add(layout, SliderControl("DDIM Eta",
            settings, "ddim_eta", float, 0, 1, 0.01, 2))

        layout.addStretch()
        self.setLayout(layout)

    def update(self, settings: Optional[GeneratorSettings] = None):
        for control in self._controls:
            if settings:
                control.set_target(settings)
            control.update()

    def randomize_seed(self):
        if self._seed_control.randomize_enabled:
            self._seed_control.randomize()   

    def _add(self, layout: QVBoxLayout, control: FieldControl):
        layout.addWidget(control)
        self._controls.append(control)
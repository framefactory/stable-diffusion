from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.data import OutputSettings

from .field_controls import (
    FieldControl,
    SliderControl,
    ComboControl,
    CheckBoxControl
)


class OutputSettingsView(QWidget):
    def __init__(self, settings: OutputSettings):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._controls: List[FieldControl] = []

        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self._add(layout, ComboControl("Image Format",
            settings, "format", [ "png", "jpg" ]))
        self._add(layout, SliderControl("Image Width",
            settings, "width", int, 256, 1024, 64))
        self._add(layout, SliderControl("Image Height",
            settings, "height", int, 256, 1024, 64))
        self._add(layout, CheckBoxControl("Seamless",
            settings, "seamless"))
        self._add(layout, ComboControl("Upscaling Factor",
            settings, "upscale_factor", [ 1, 2, 4 ], [ "Off", "2x", "4x" ]))
        self._add(layout, SliderControl("Upscaling Strength",
            settings, "upscale_strength", float, 0, 1, 0.01, 2))
        self._add(layout, SliderControl("Face Reconstruction Strength",
            settings, "gfpgan_strength", float, 0, 1, 0.01, 2))

        layout.addStretch()
        self.setLayout(layout)

    def update(self, settings: Optional[OutputSettings] = None):
        for control in self._controls:
            if settings:
                control.set_target(settings)
            control.update()

    def _add(self, layout: QVBoxLayout, control: FieldControl):
        layout.addWidget(control)
        self._controls.append(control)
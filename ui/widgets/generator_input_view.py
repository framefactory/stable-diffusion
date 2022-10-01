from typing import Optional

from PySide6.QtCore import Qt, Slot

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton
)

from ui.data import GeneratorSettings
from .image_thumb import ImageThumb

class GeneratorInputView(QWidget):
    def __init__(self, settings: GeneratorSettings):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._settings = settings

        horz_layout = QHBoxLayout()

        vert_layout = QVBoxLayout()
        self._prompt_edit = QTextEdit()
        self._prompt_edit.setFontPointSize(16.0)
        self._prompt_edit.textChanged.connect(self._prompt_changed) # type:ignore
        vert_layout.addWidget(QLabel("Prompt"))
        vert_layout.addWidget(self._prompt_edit, 3)

        self._neg_prompt_edit = QTextEdit()
        self._neg_prompt_edit.setFontPointSize(16.0)
        self._neg_prompt_edit.textChanged.connect(self._neg_prompt_changed) #type:ignore
        vert_layout.addWidget(QLabel("Negative Prompt"))
        vert_layout.addWidget(self._neg_prompt_edit, 1)
        horz_layout.addLayout(vert_layout, 1)

        vert_layout = QVBoxLayout()
        self._image_thumb = ImageThumb()
        vert_layout.addWidget(QLabel("Image"))
        vert_layout.addWidget(self._image_thumb)
        self._clear_button = QPushButton("Clear Image")
        self._clear_button.clicked.connect(self._clear_input_image) #type:ignore
        vert_layout.addWidget(self._clear_button)
        vert_layout.addStretch()
        horz_layout.addLayout(vert_layout, 0)

        self.setLayout(horz_layout)
        self.update()

    def update(self, settings: Optional[GeneratorSettings] = None):
        if settings:
            self._settings = settings

        self._prompt_edit.setText(self._settings.prompt)
        self._neg_prompt_edit.setText(self._settings.negative_prompt)
        self._image_thumb.loadImage(self._settings.image_path)

    @Slot()
    def _prompt_changed(self):
        self._settings.prompt = self._prompt_edit.toPlainText().strip()

    @Slot()
    def _neg_prompt_changed(self):
        self._settings.negative_prompt = self._neg_prompt_edit.toPlainText().strip()

    @Slot()
    def _clear_input_image(self):
        self._settings.image_path = ""
        self.update()
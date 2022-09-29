from PIL.Image import Image

from PySide6.QtCore import (
    Qt,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton
)

from ui.app import DreamConstants, DreamVariables
from .image_thumb import ImageThumb

class InputPanel(QDockWidget):
    def __init__(self, constants: DreamConstants, variables: DreamVariables):
        super().__init__("Input", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self._constants = constants
        self._variables = variables

        main_widget = QWidget(self)
        horz_layout = QHBoxLayout()

        vert_layout = QVBoxLayout()
        self._prompt_edit = QTextEdit()
        self._prompt_edit.textChanged.connect(self._prompt_changed) # type:ignore
        vert_layout.addWidget(QLabel("Prompt"))
        vert_layout.addWidget(self._prompt_edit, 3)

        self._neg_prompt_edit = QTextEdit()
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

        main_widget.setLayout(horz_layout)
        self.setWidget(main_widget)

        self.update()

    def set_constants(self, constants: DreamConstants):
        self._constants = constants
        self.update()

    def set_variables(self, variables: DreamVariables):
        self._variables = variables
        self.update()

    def update(self):
        self._prompt_edit.setText(self._variables.prompt)
        self._neg_prompt_edit.setText(self._variables.negative_prompt)
        self._image_thumb.loadImage(self._constants.image_path)

    @Slot()
    def _prompt_changed(self):
        self._variables.prompt = self._prompt_edit.toPlainText().strip()

    @Slot()
    def _neg_prompt_changed(self):
        self._variables.negative_prompt = self._neg_prompt_edit.toPlainText().strip()

    @Slot()
    def _clear_input_image(self):
        self._constants.image_path = ""
        self.update()
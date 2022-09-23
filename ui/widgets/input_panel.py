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
    QCheckBox
)

from ui.engine import ImageParams
from .image_thumb import ImageThumb

class InputPanel(QDockWidget):
    def __init__(self, params: ImageParams):
        super().__init__("Input", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.params = params

        main_widget = QWidget(self)
        horz_layout = QHBoxLayout()

        vert_layout = QVBoxLayout()
        self._prompt_edit = QTextEdit(params.prompt)
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
        self._image_check = QCheckBox("Use Image")
        vert_layout.addWidget(self._image_check)
        vert_layout.addStretch()
        horz_layout.addLayout(vert_layout, 0)

        main_widget.setLayout(horz_layout)
        self.setWidget(main_widget)

    @Slot()
    def _prompt_changed(self):
        self.params.prompt = self._prompt_edit.toPlainText()

    @Slot()
    def _neg_prompt_changed(self):
        pass
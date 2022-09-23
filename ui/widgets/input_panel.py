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
        self._clear_button = QPushButton("Clear Image")
        self._clear_button.clicked.connect(self.clearInputImage) #type:ignore
        vert_layout.addWidget(self._clear_button)
        vert_layout.addStretch()
        horz_layout.addLayout(vert_layout, 0)

        main_widget.setLayout(horz_layout)
        self.setWidget(main_widget)

    def setInputImage(self, path: str, image: Image):
        self.params.init_img = path
        self._image_thumb.setImage(image)

    @Slot()
    def clearInputImage(self):
        self.params.init_img = None
        self._image_thumb.clearImage()

    @Slot()
    def _prompt_changed(self):
        self.params.prompt = self._prompt_edit.toPlainText()

    @Slot()
    def _neg_prompt_changed(self):
        pass

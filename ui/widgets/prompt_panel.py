from PySide6.QtCore import (
    Qt,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QSlider,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QGridLayout
)

from ui.engine import ImageParams

class PromptPanel(QDockWidget):
    def __init__(self, parent: QWidget, params: ImageParams):
        super().__init__(parent)
        self.params = params

        main_widget = QWidget(self)
        main_layout = QVBoxLayout()

        self.prompt_edit = prompt_edit = QTextEdit(params.prompt)
        prompt_edit.textChanged.connect(self._on_prompt_changed) # type:ignore
        main_layout.addWidget(QLabel("Prompt"))
        main_layout.addWidget(prompt_edit)

        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)
        self.setWindowTitle("Prompt")

    @Slot()
    def _on_prompt_changed(self):
        self.params.prompt = self.prompt_edit.toPlainText()
        print(self.params.prompt)

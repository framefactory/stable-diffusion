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

class SettingsPanel(QDockWidget):
    generate = Signal()

    def __init__(self, parent: QWidget, params: ImageParams):
        super().__init__(parent)
        self.params = params

        main_layout = QVBoxLayout()
        param_layout = QGridLayout()

        param_layout.addWidget(QLabel("Seed"), 0, 0)
        self.seed_edit = seed_edit = QLineEdit()
        seed_edit.textChanged.connect(self._seed_changed) #type:ignore
        param_layout.addWidget(seed_edit, 0, 1)
        seed_button = QPushButton("\u21bb")
        seed_button.clicked.connect(self._seed_clicked) #type:ignore
        param_layout.addWidget(seed_button, 0, 2)

        param_layout.addWidget(QLabel("Steps"), 1, 0)
        steps_slider = self.steps_slider = QSlider(Qt.Horizontal)
        steps_slider.setMinimum(1)
        steps_slider.setMaximum(200)
        param_layout.addWidget(self.steps_slider, 1, 1)
        self.steps_text = QLabel()
        self.steps_text.setAlignment(Qt.AlignRight)
        param_layout.addWidget(self.steps_text, 1, 2)
        steps_slider.valueChanged.connect(self._steps_changed) #type:ignore

        param_layout.addWidget(QLabel("CFG scale"), 2, 0)
        cfg_slider = self.cfg_slider = QSlider(Qt.Horizontal)
        cfg_slider.setMinimum(10)
        cfg_slider.setMaximum(100)
        param_layout.addWidget(self.cfg_slider, 2, 1)
        self.cfg_text = QLabel()
        self.cfg_text.setAlignment(Qt.AlignRight)
        param_layout.addWidget(self.cfg_text, 2, 2)
        cfg_slider.valueChanged.connect(self._cfg_changed) #type:ignore

        param_layout.addWidget(QLabel("Sampler"), 3, 0)
        sampler_combo = self.sampler_combo = QComboBox()
        sampler_combo.addItems([ s.value for s in Sampler])
        param_layout.addWidget(sampler_combo, 3, 1)
        sampler_combo.currentIndexChanged.connect(self._sampler_changed) #type:ignore


        command_layout = QVBoxLayout()
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self._generate_clicked) #type:ignore
        command_layout.addWidget(generate_button)

        main_layout.addLayout(param_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(command_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

        self.update()

    def update(self, params: Optional[ImageParams] = None):
        if params:
            self.params = params

        self.seed_edit.setText(str(self.params.seed))
        self.steps_slider.setValue(self.params.steps)
        self.cfg_slider.setValue(int(self.params.cfg_scale * 10))
        self.sampler_combo.setCurrentText(self.params.sampler_name)

    def sizeHint(self) -> QSize:
        return QSize(380, 640)

    @Slot()
    def _seed_changed(self):
        self.params.seed = int(self.seed_edit.text())

    @Slot()
    def _seed_clicked(self):
        random.seed()
        self.params.seed = random.randint(0, 2**31-1)
        self.seed_edit.setText(str(self.params.seed))

    @Slot()
    def _cfg_changed(self):
        self.params.cfg_scale = self.cfg_slider.value() / 10.0
        self.cfg_text.setText(f"{self.params.cfg_scale:.2f}")

    @Slot()
    def _steps_changed(self):
        self.params.steps = self.steps_slider.value()
        self.steps_text.setText(f"{self.params.steps}")

    @Slot()
    def _sampler_changed(self):
        self.params.sampler_name = self.sampler_combo.currentText()

    @Slot()
    def _generate_clicked(self):
        for key, value in self.params.to_dict().items():
            print(f'{key}: {value}')
        self.generate.emit() #type:ignore
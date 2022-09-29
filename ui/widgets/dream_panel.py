from copy import copy

from PySide6.QtCore import (
    Signal,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

from ui.app import Engine

from .controls import SpinBoxControl
from .settings_panel import SettingsPanel
from .input_panel import InputPanel

class DreamPanel(QDockWidget):
    generate = Signal()

    def __init__(self, engine: Engine, settings: SettingsPanel, input: InputPanel):
        super().__init__("Generator", None)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self._engine = engine
        self._settings_panel = settings
        self._input_panel = input

        main_layout = QVBoxLayout()

        seq_layout = QHBoxLayout()
        main_layout.addLayout(seq_layout)

        key0_button = QPushButton("Begin")
        key0_button.clicked.connect(self._key0_clicked) #type:ignore
        seq_layout.addWidget(key0_button)
        copy0to1_button = QPushButton("Copy >>")
        copy0to1_button.clicked.connect(self._copy0to1_clicked) #type:ignore
        seq_layout.addWidget(copy0to1_button)
        copy1to0_button = QPushButton("<< Copy")
        copy1to0_button.clicked.connect(self._copy1to0_clicked) #type:ignore
        seq_layout.addWidget(copy1to0_button)
        key1_button = QPushButton("End")
        key1_button.clicked.connect(self._key1_clicked) #type:ignore
        seq_layout.addWidget(key1_button)

        cmd_layout = QVBoxLayout()
        main_layout.addLayout(cmd_layout)

        self._iterations_control = SpinBoxControl("Iterations", 1, 10000)
        self._iterations_control.changed.connect(self._iterations_changed)
        cmd_layout.addWidget(self._iterations_control)

        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self._generate_clicked) #type:ignore
        cmd_layout.addWidget(generate_button)

        main_layout.addStretch()

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)

    @Slot()
    def _key0_clicked(self):
        variables = self._engine.dream.keys[0].variables
        self._settings_panel.set_variables(variables)
        self._input_panel.set_variables(variables)

    @Slot()
    def _key1_clicked(self):
        variables = self._engine.dream.keys[1].variables
        self._settings_panel.set_variables(variables)
        self._input_panel.set_variables(variables)

    @Slot()
    def _copy0to1_clicked(self):
        dream = self._engine.dream
        dream.keys[1].variables = copy(dream.keys[0].variables)
        self._key1_clicked()

    @Slot()
    def _copy1to0_clicked(self):
        dream = self._engine.dream
        dream.keys[0].variables = copy(dream.keys[1].variables)
        self._key0_clicked()

    @Slot(int)
    def _iterations_changed(self, value: int):
        dream = self._engine.dream
        dream.length = value
        dream.keys[1].frame = max(1, value - 1)

    @Slot()
    def _generate_clicked(self):
        self._settings_panel.randomize_seeds()
        self._engine.generate_dream()

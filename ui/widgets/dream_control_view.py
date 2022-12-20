from copy import copy

from PySide6.QtCore import Qt, Slot

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

from ui.app import Engine

from .field_controls import SpinBoxControl
from .generator_input_view import GeneratorInputView
from .generator_settings_view import GeneratorSettingsView
from .output_settings_view import OutputSettingsView

class DreamControlView(QWidget):
    def __init__(self, engine: Engine, output_view: OutputSettingsView,
        settings_view: GeneratorSettingsView, input_view: GeneratorInputView):
        
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._engine = engine
        self._document = engine.documents.active_document
        engine.documents.active_document_changed.connect(self._document_changed)

        self._output_view = output_view
        self._settings_view = settings_view
        self._input_view = input_view

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

        

        # self._iterations_control = SpinBoxControl("Iterations",
        #     self._document.dream, "length", 1, 10000)
        # self._iterations_control.changed.connect(self._iterations_changed)
        # cmd_layout.addWidget(self._iterations_control)

        button_layout = QHBoxLayout()
        cmd_layout.addLayout(button_layout)

        generate_sequence_button = QPushButton("Dream Image (F5)")
        generate_sequence_button.clicked.connect(self._generate_image_clicked) #type:ignore
        button_layout.addWidget(generate_sequence_button)

        generate_sequence_button = QPushButton("Dream Sequence (Shift-F5)")
        generate_sequence_button.clicked.connect(self._generate_sequence_clicked) #type:ignore
        button_layout.addWidget(generate_sequence_button)

        main_layout.addStretch()
        self.setLayout(main_layout)

    # @Slot()
    # def _key0_clicked(self):
    #     settings = self._engine.dream.keys[0].generator
    #     self._settings_view.update(settings)
    #     self._input_view.update(settings)

    # @Slot()
    # def _key1_clicked(self):
    #     settings = self._engine.dream.keys[1].generator
    #     self._settings_view.update(settings)
    #     self._input_view.update(settings)

    # @Slot()
    # def _copy0to1_clicked(self):
    #     dream = self._engine.dream
    #     dream.keys[1].generator = copy(dream.keys[0].generator)
    #     self._key1_clicked()

    # @Slot()
    # def _copy1to0_clicked(self):
    #     dream = self._engine.dream
    #     dream.keys[0].generator = copy(dream.keys[1].generator)
    #     self._key0_clicked()

    # @Slot(int)
    # def _iterations_changed(self, value: int):
    #     self._engine.dream.keys[1].frame = max(1, value - 1)

    @Slot()
    def _generate_image_clicked(self):
        self._settings_view.randomize_seed()
        self._engine.dream_still()

    @Slot()
    def _generate_sequence_clicked(self):
        self._engine.dream_sequence()

    @Slot()
    def _document_changed(self):
        document = self._engine.documents.active_document
        assert(document)
        self._output_view.update(document.output)
        self._settings_view.update(document.generator)
        self._input_view.update(document.generator)
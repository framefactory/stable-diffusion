from typing import cast, Optional
import PIL.Image as PIL_Image

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QCloseEvent

from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QDockWidget,
    QScrollArea,
    QProgressBar,
    QFileDialog,
    QLabel
)

from ui.app import (
    Engine,
    DreamerState,    
    DreamProgress
)
from ui.app.dream_image_document import DreamImageDocument

from .document_area import DocumentArea
from .library_panel import LibraryPanel

from .generator_input_view import GeneratorInputView
from .generator_settings_view import GeneratorSettingsView
from .output_settings_view import OutputSettingsView
from .dream_control_view import DreamControlView


class DockPanel(QDockWidget):
    def __init__(self, title: str, widget: QWidget):
        super().__init__(title)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.setWidget(widget)


class ScrollPanel(QDockWidget):
    def __init__(self, title: str, widget: QWidget):
        super().__init__(title)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        self.setWidget(scroll_area)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._engine = Engine(self)
        self._engine.dreamer.progress_update.connect(self.update_progress)

        self._createMenu()
        self._createStatusBar()
        self._createDockPanels()

        self._document_area = DocumentArea(self, self._engine.documents)
        self.setCentralWidget(self._document_area)

        self.setDockNestingEnabled(True)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.setWindowTitle("Diffusion Lab")
        self.resize(QApplication.primaryScreen().availableSize() * (3 / 4))

        # actions handled by MainWindow
        actions = self._engine.actions
        actions.import_image_and_data.triggered.connect(self.import_image_and_data) #type:ignore
        actions.dream_image.triggered.connect(self._control_view._generate_image_clicked) #type:ignore
        actions.dream_sequence.triggered.connect(self._control_view._generate_sequence_clicked) #type:ignore

        self._engine.start()

    def closeEvent(self, event: QCloseEvent):
        self._engine.stop()
        event.accept()

    def _createMenu(self):
        actions = self._engine.actions
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(actions.new_image)
        file_menu.addSeparator()
        file_menu.addAction(actions.import_image_and_data)
        file_menu.addAction(actions.export_image)
        file_menu.addSeparator()
        file_menu.addAction(actions.exit)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(actions.dream_image)
        edit_menu.addAction(actions.dream_sequence)
        edit_menu.addSeparator()
        edit_menu.addAction(actions.use_as_input_image)
        edit_menu.addAction(actions.open_input_image)

    def _createStatusBar(self):
        self._status_label = QLabel()
        self._status_progress = QProgressBar()
        self._status_progress.setTextVisible(False)
        self._status_progress.setMinimum(0)
        self._status_progress.setMaximum(100)

        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().addPermanentWidget(self._status_label)
        self.statusBar().addPermanentWidget(self._status_progress, 1)

    def _createDockPanels(self):
        dream = self._engine.dream

        self._library_panel = LibraryPanel()
        self.addDockWidget(Qt.LeftDockWidgetArea, self._library_panel)

        self._settings_view = GeneratorSettingsView(dream.keys[0].settings)
        self.addDockWidget(Qt.RightDockWidgetArea, ScrollPanel("Generator", self._settings_view))

        self._output_view = OutputSettingsView(dream.output)
        self.addDockWidget(Qt.RightDockWidgetArea, ScrollPanel("Output", self._output_view))

        self._input_view = GeneratorInputView(dream.keys[0].settings)
        self.addDockWidget(Qt.BottomDockWidgetArea, DockPanel("Input", self._input_view))

        self._control_view = DreamControlView(self._engine, self._output_view, self._settings_view, self._input_view)
        self.addDockWidget(Qt.RightDockWidgetArea, DockPanel("Dream", self._control_view))

    @Slot()
    def close_image(self):
        pass

    @Slot()
    def import_image_and_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image and Data", filter="Image/Data Files (*.png *.jpg *.json)")
        if file_path:
            active_document = self._engine.documents.active_document
            if type(active_document) is DreamImageDocument:
                active_document.import_images_and_data(file_path)
            else:
                document = DreamImageDocument()
                if document.import_images_and_data(file_path):
                    self._engine.documents.add_image_document(document)

    @Slot(DreamProgress)
    def update_progress(self, progress: DreamProgress):
        self._status_label.setText(progress.text)

        if progress.state == DreamerState.DREAMING:
            completed = progress.step / float(progress.total_steps - 1)
            if progress.total_frames > 1:
                completed = (progress.frame + completed) / progress.total_frames

            self._status_progress.setTextVisible(True)
            self._status_progress.setMaximum(100)
            self._status_progress.setValue(int(completed * 100))

        elif progress.state == DreamerState.LOADING:
            self._status_progress.setTextVisible(False)
            self._status_progress.setMaximum(0)
        
        else:
            self._status_progress.setTextVisible(False)
            self._status_progress.setMaximum(100)
            self._status_progress.setValue(0)

from typing import cast, Optional
import os
import PIL.Image as PIL_Image

from PySide6.QtCore import (
    Qt,
    Slot
)

from PySide6.QtGui import (
    QAction,
    QCloseEvent
)

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QProgressBar,
    QFileDialog
)

from ui.data import (
    Preferences
)

from ui.app import (
    Actions,
    Engine,
    DreamerState,    
    DreamProgress,
    Dream,
    DreamImage
)

from .document_area import DocumentArea
from .dream_image_view import DreamImageView
from .dream_panel import DreamPanel
from .input_panel import InputPanel
from .settings_panel import SettingsPanel
from .library_panel import LibraryPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._engine = Engine(self)
        self._engine.dreamer.progress_update.connect(self._progress_update)

        self._createMenu()
        self._createStatusBar()
        self._createDockPanels()

        self._document_area = DocumentArea(self, self._engine.documents)
        self.setCentralWidget(self._document_area)

        #self._new_image()

        self.setDockNestingEnabled(True)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.setWindowTitle("Diffusion Lab")
        self.resize(QApplication.primaryScreen().availableSize() * (3 / 4))

        self._engine.start()

        #self._renderer.image_ready.connect(self._image_ready) #type:ignore
        #self._renderer.progress_update.connect(self._progress_update) #type:ignore
        #self._renderer.start()

    def show(self):
        super().show()
        self.resizeDocks([self._library_panel], [340], Qt.Horizontal)
        self.resizeDocks([self._settings_panel], [340], Qt.Horizontal)
        self.resizeDocks([self._input_panel], [240], Qt.Vertical)

    def closeEvent(self, event: QCloseEvent):
        self._engine.stop()
        event.accept()

    def _createMenu(self):
        actions = self._engine.actions
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(actions.new_image)
        file_menu.addAction(actions.export_image)
        file_menu.addSeparator()
        file_menu.addAction(actions.exit)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(actions.generate)
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
        actions = self._engine.actions
        dream = self._engine.dream

        self._library_panel = LibraryPanel()
        self.addDockWidget(Qt.LeftDockWidgetArea, self._library_panel)

        self._settings_panel = SettingsPanel(dream.constants, dream.keys[0].variables)
        self.addDockWidget(Qt.RightDockWidgetArea, self._settings_panel)

        self._input_panel = InputPanel(dream.constants, dream.keys[0].variables)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._input_panel)

        self._dream_panel = DreamPanel(self._engine, self._settings_panel, self._input_panel)
        self._dream_panel.generate.connect(actions.generate.trigger)
        self.addDockWidget(Qt.RightDockWidgetArea, self._dream_panel)

    @Slot()
    def _close_image(self):
        pass

    @Slot(DreamProgress)
    def _progress_update(self, progress: DreamProgress):
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

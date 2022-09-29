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

from ui.engine import (
    Preferences,
    Library,
    Engine,
    EngineProgress,
    EngineState,    
    ImageParams,
    ImageJob
)
from ui.engine.image_document import ImageDocument

from .document_area import DocumentArea
from .image_view import ImageDocumentView
from .input_panel import InputPanel
from .settings_panel import SettingsPanel
from .library_panel import LibraryPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._preferences = Preferences()
        self._params = ImageParams()
        self._library = Library(self, self._preferences)

        self._createActions()
        self._createMenu()
        self._createStatusBar()
        self._createDockPanels()

        self._document_area = DocumentArea(self)
        self.setCentralWidget(self._document_area)

        #self._new_image()

        self.setDockNestingEnabled(True)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.setWindowTitle("Diffusion Lab")
        self.resize(QApplication.primaryScreen().availableSize() * (3 / 5))

        self.engine = Engine(self, self._preferences)
        self.engine.image_ready.connect(self._image_ready) #type:ignore
        self.engine.progress_update.connect(self._progress_update) #type:ignore
        self.engine.start()

    def show(self):
        super().show()
        self.resizeDocks([self._library_panel], [340], Qt.Horizontal)
        self.resizeDocks([self._settings_panel], [340], Qt.Horizontal)
        self.resizeDocks([self._prompt_panel], [240], Qt.Vertical)

    def closeEvent(self, event: QCloseEvent):
        self.engine.stop()
        event.accept()

    def _createActions(self):
        self._new_image_action = QAction("&New Image", self)
        self._new_image_action.setShortcut("Ctrl+N")
        self._new_image_action.triggered.connect(self._new_image) #type:ignore

        self._export_image_action = QAction("&Export Image...", self)
        self._export_image_action.setShortcut("Ctrl+E")
        self._export_image_action.triggered.connect(self._export_image) #type:ignore

        self._exit_action = QAction("&Quit", self)
        self._exit_action.setShortcut("Alt+F4")
        self._exit_action.triggered.connect(self.close) #type:ignore

        self._generate_action = QAction("&Generate Image", self)
        self._generate_action.setShortcut("F5")
        self._generate_action.triggered.connect(self._generate) #type:ignore

        self._use_as_input_image_action = QAction("Use As &Input Image", self)
        self._use_as_input_image_action.setShortcut("Ctrl+I")
        self._use_as_input_image_action.triggered.connect(self._use_as_input_image) #type:ignore

        self._open_input_image_action = QAction("&Open Input Image...", self)
        self._open_input_image_action.setShortcut("Shift+Ctrl+I")
        self._open_input_image_action.triggered.connect(self._open_input_image) #type:ignore

    def _createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self._new_image_action)
        file_menu.addAction(self._export_image_action)
        file_menu.addSeparator()
        file_menu.addAction(self._exit_action)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self._generate_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self._use_as_input_image_action)
        edit_menu.addAction(self._open_input_image_action)

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
        self._library_panel = LibraryPanel()
        self.addDockWidget(Qt.LeftDockWidgetArea, self._library_panel)

        self._settings_panel = SettingsPanel(self._params)
        self._settings_panel.generate.connect(self._generate_action.trigger)
        self.addDockWidget(Qt.RightDockWidgetArea, self._settings_panel)

        self._prompt_panel = InputPanel(self._params)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._prompt_panel)

    def _get_active_document(self) -> Optional[ImageDocument]:
        image_view = cast(ImageDocumentView, self._document_area.activeSubWindow())
        return None if image_view is None else image_view.document

    @Slot()
    def _new_image(self) -> ImageDocumentView:
        return self._document_area.addDocument()

    @Slot()
    def _export_image(self):
        document = self._get_active_document()
        if document is not None and document.image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Image", filter="Image Files (*.png *.jpg *.bmp)")
            print(file_path)
            


    @Slot()
    def _close_image(self):
        pass

    @Slot()
    def _open_input_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", filter="Image Files (*.png *.jpg *.bmp)")
        image = PIL_Image.open(file_path)
        image.load()
        self._prompt_panel.setInputImage(file_path, image)

    @Slot()
    def _use_as_input_image(self):
        document = self._get_active_document()
        if document is None:
            print("no active document")
        else:
            path = os.path.join(self._preferences.library_path, document.params.path)
            image = document.image
            if image is None:
                print("document has no image")
            else:
                self._prompt_panel.setInputImage(path, image)

    @Slot(int)
    def _generate(self, iterations: int):
        if self._settings_panel._seed_control.auto_generate:
            self._settings_panel._seed_control.generate()

        # print("\nParameters")
        # for key, value in self._params.to_dict().items():
        #     print(f'  {key}: {value}')

        job = ImageJob(self._params)
        self.engine.post_job(job)

    @Slot(EngineProgress)
    def _progress_update(self, progress: EngineProgress):
        text = progress.state.value
        self._status_label.setText(text)

        if progress.state == EngineState.DREAMING:
            completed = progress.step / float(progress.total_steps - 1)
            if progress.total_frames > 1:
                completed = (progress.frame + completed) / progress.total_frames

            self._status_progress.setTextVisible(True)
            self._status_progress.setMaximum(100)
            self._status_progress.setValue(int(completed * 100))

        elif progress.state == EngineState.LOADING:
            self._status_progress.setTextVisible(False)
            self._status_progress.setMaximum(0)
        
        else:
            self._status_progress.setTextVisible(False)
            self._status_progress.setMaximum(100)
            self._status_progress.setValue(0)

    @Slot(ImageDocument)
    def _image_ready(self, document: ImageDocument):
        image_view = cast(ImageDocumentView, self._document_area.activeSubWindow())
        if image_view is None:
            image_view = self._new_image()

        image_view.setImageDocument(document)
from PySide6.QtCore import (
    Qt,
    Slot
)

from PySide6.QtGui import (
    QCloseEvent
)

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QDockWidget,
    QLabel,
    QProgressBar
)

from ui.engine import (
    Library,
    Engine,
    EngineProgress,
    EngineState,
    ImageParams,
    ImageResult
)

from .document_area import DocumentArea
from .document_view import DocumentView
from .prompt_panel import PromptPanel
from .settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.params = ImageParams()

        self.status_label = QLabel()
        self.status_progress = QProgressBar()
        self.status_progress.setTextVisible(False)
        self.status_progress.setMinimum(0)
        self.status_progress.setMaximum(100)

        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().addPermanentWidget(self.status_label)
        self.statusBar().addPermanentWidget(self.status_progress, 1)

        self.document_area = DocumentArea(self)
        self.setCentralWidget(self.document_area)

        self.document_view = DocumentView(self)
        self.document_area.addSubWindow(self.document_view)
        self.document_area.addSubWindow(DocumentView(self))
        self.document_area.addSubWindow(DocumentView(self))

        self.setDockNestingEnabled(True)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.settings_panel = SettingsPanel(self, self.params)
        self.settings_panel.generate.connect(self._generate) #type:ignore
        self.addDockWidget(Qt.RightDockWidgetArea, self.settings_panel)

        self.prompt_panel = PromptPanel(self, self.params)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.prompt_panel)

        self.setWindowTitle("Diffusion Lab")
        self.resize(QApplication.primaryScreen().availableSize() * (2 / 5))

        self.library = Library(self, "library")

        self.engine = Engine(self)
        self.engine.image_ready.connect(self._image_ready) #type:ignore
        self.engine.progress_update.connect(self._progress_update) #type:ignore
        self.engine.start()

    def show(self):
        super().show()
        self.resizeDocks([self.settings_panel], [360], Qt.Horizontal)
        self.resizeDocks([self.prompt_panel], [180], Qt.Vertical)

    def closeEvent(self, event: QCloseEvent):
        self.engine.stop()
        event.accept()

    def _generate(self):
        self.engine.post_job(self.params)

    @Slot(EngineProgress)
    def _progress_update(self, progress: EngineProgress):
        text = progress.state.value
        self.status_label.setText(text)

        if progress.state == EngineState.CALCULATING:
            self.status_progress.setTextVisible(True)
            self.status_progress.setValue(progress.percent)
        else:
            self.status_progress.setTextVisible(False)
            self.status_progress.setValue(0)

    @Slot(ImageResult)
    def _image_ready(self, result: ImageResult):
        self.library.save_image(result.image, result.params)
        self.document_view.show_image(result.image)
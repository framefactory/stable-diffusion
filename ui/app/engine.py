from typing import Optional
from copy import deepcopy

from PySide6.QtCore import QObject, Signal, Slot

from ui.data import Preferences, DreamImage, DreamSequence, GeneratorKey

from .dream_document import DreamDocument
from .dream_image_document import DreamImageDocument
from .dream_sequence_document import DreamSequenceDocument

#from ui.widgets import ImageDocumentView

from .actions import Actions
from .documents import Documents
from .dreamer import Dreamer
from .library import Library

class Engine(QObject):
    close_application = Signal()
    dream_changed = Signal()

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self.actions = Actions(self)
        self.preferences = Preferences()
        self.documents = Documents(self)
        self.documents.active_document_changed.connect(self._document_changed)
        self.library = Library(self, self.preferences)
        self.dreamer = Dreamer(self, self.preferences, self.library)
        self.dreamer.image_ready.connect(self.documents.add_generated_image)

        self.dream = DreamSequence()
        self.dream.keys.append(GeneratorKey(0))
        self.dream.keys.append(GeneratorKey(1))

        actions = self.actions
        actions.new_image.triggered.connect(self._new_image) #type:ignore
        actions.export_image.triggered.connect(self._export_image) #type:ignore
        actions.exit.triggered.connect(self.close_application) #type:ignore
        actions.use_as_input_image.triggered.connect(self._use_as_input_image) #type:ignore
        actions.open_input_image.triggered.connect(self._open_input_image) #type:ignore        

    def start(self):
        self.dreamer.start()

    def stop(self):
        self.dreamer.stop()

    def dream_image(self):
        generator = self.dream.keys[0].settings
        dream = DreamImage("", generator, self.dream.output)
        self.dreamer.dream(dream)

    def dream_sequence(self):
        self.dreamer.dream(self.dream)

    @Slot()
    def _document_changed(self, document: DreamDocument):
        if type(document) is DreamImageDocument:
            dream_image = deepcopy(document.dream_image)
            self.dream.output = dream_image.output
            self.dream.keys[0].settings = dream_image.generator
            self.dream_changed.emit()

    @Slot()
    def _new_image(self):
        pass
        #return self._document_area.addDocument()

    @Slot()
    def _export_image(self):
        pass
        # document = self._get_active_document()
        # if document is not None and document.image is not None:
        #     file_path, _ = QFileDialog.getSaveFileName(self, "Export Image", filter="Image Files (*.png *.jpg *.bmp)")
        #     print(file_path)
            
    @Slot()
    def _close_image(self):
        pass

    @Slot()
    def _open_input_image(self):
        pass
        # file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", filter="Image Files (*.png *.jpg *.bmp)")
        # image = PIL_Image.open(file_path)
        # image.load()
        # self._prompt_panel.setInputImage(file_path, image)

    @Slot()
    def _use_as_input_image(self):
        pass
        # document = self._get_active_document()
        # if document is None:
        #     print("no active document")
        # else:
        #     path = os.path.join(self._preferences.library_path, document.params.path)
        #     image = document.image
        #     if image is None:
        #         print("document has no image")
        #     else:
        #         self._prompt_panel.setInputImage(path, image)


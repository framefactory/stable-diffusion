from typing import Optional
from copy import deepcopy

from PySide6.QtCore import QObject, Signal, Slot

from ui.data import Preferences

from .dream_params import Dream, DreamVariables, VariableKey
from .dream_image import DreamImage

#from ui.widgets import ImageDocumentView

from .actions import Actions
from .documents import Documents
from .dreamer import Dreamer
from .library import Library

class Engine(QObject):
    close_application = Signal()

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)

        self.actions = Actions(self)
        self.preferences = Preferences()
        self.documents = Documents(self)
        self.library = Library(self, self.preferences)
        self.dreamer = Dreamer(self, self.preferences, self.library)
        self.dreamer.frame_ready.connect(self.documents.add_frame)

        self.dream = Dream()

        key0 = VariableKey(0, DreamVariables())
        key1 = VariableKey(1, DreamVariables())
        self.dream.keys.append(key0)
        self.dream.keys.append(key1)


        actions = self.actions
        actions.new_image.triggered.connect(self._new_image) #type:ignore
        actions.export_image.triggered.connect(self._export_image) #type:ignore
        actions.exit.triggered.connect(self.close_application) #type:ignore
        actions.generate.triggered.connect(self.generate_dream) #type:ignore
        actions.use_as_input_image.triggered.connect(self._use_as_input_image) #type:ignore
        actions.open_input_image.triggered.connect(self._open_input_image) #type:ignore        

    def start(self):
        self.dreamer.start()

    def stop(self):
        self.dreamer.stop()

    @Slot()
    def generate_dream(self):
        self.dreamer.add_dream(self.dream)

    # @Slot(DreamImage)
    # def _image_ready(self, document: DreamImage):
    #     self.documents.add_image_document(document)


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


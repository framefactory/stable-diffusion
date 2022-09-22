from PIL.Image import Image
from PIL.ImageQt import ImageQt

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QImage,
    QPixmap,
    QPalette
)

from PySide6.QtWidgets import (
    QWidget,
    QMdiSubWindow,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy
)

class DocumentView(QMdiSubWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.image_label = QLabel()
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        scroll_area = QScrollArea()
        scroll_area.setBackgroundRole(QPalette.Dark)
        scroll_area.setWidget(self.image_label)
        scroll_area.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setWidget(main_widget)
        self.setWindowTitle("Image")
        

    def show_image(self, image: Image):
        pixmap = QPixmap.fromImage(ImageQt(image))
        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.size())
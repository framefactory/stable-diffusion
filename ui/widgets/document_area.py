from PySide6.QtWidgets import (
    QWidget,
    QMdiArea
)

class DocumentArea(QMdiArea):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setViewMode(QMdiArea.TabbedView)

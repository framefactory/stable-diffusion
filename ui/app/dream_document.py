from typing import List, Any

from PySide6.QtCore import QObject, Signal


class DreamDocument(QObject):
    changed = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.rating: int = 0
        self.tags: List[str] = []
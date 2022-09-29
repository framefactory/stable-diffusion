from typing import List, Optional

from PySide6.QtCore import QObject, Signal


class DreamDocument(QObject):
    changed = Signal()

    def __init__(self, rating: int, tags: List[str]):
        super().__init__()

        self.rating = rating
        self.tags = tags
import sys
import math
import torch

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

class SystemInfoView(QWidget):
    def __init__(self):
        super().__init__()

        cuda_available = torch.cuda.is_available()

        grid = QGridLayout()
        grid.setContentsMargins(4, 4, 4, 4)
        self._add_info(grid, "Python Version", sys.version)
        self._add_info(grid, "Torch Version", torch.__version__)
        self._add_info(grid, "CUDA available", "Yes" if cuda_available else "No")
        if cuda_available:
            cuda_device_id = torch.cuda.current_device()
            device_props = torch.cuda.get_device_properties(cuda_device_id)
            total_memory = math.floor(device_props.total_memory / (1 << 20))
            self._add_info(grid, "CUDA Version", torch.version.cuda) #type:ignore
            self._add_info(grid, "GPU Name", device_props.name)
            self._add_info(grid, "GPU Total Memory", f"{total_memory} MB")

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    @staticmethod
    def _add_info(grid: QGridLayout, key: str, value: str):
        row = grid.rowCount()
        
        key_label = QLabel(key)
        key_label.setWordWrap(True)
        key_label.setAlignment(Qt.AlignTop)
        key_label.setMargin(4)
        grid.addWidget(key_label, row, 0)

        value_label = QLabel(value)
        value_label.setWordWrap(True)
        value_label.setAlignment(Qt.AlignTop)
        value_label.setMargin(4)
        grid.addWidget(value_label, row, 1)
from typing import List, Optional
import random

from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    Slot
)

from PySide6.QtWidgets import (
    QWidget,
    QDockWidget,
    QSlider,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

class SliderControl(QWidget):
    changed = Signal(float)

    def __init__(self, title: str, min: float, max: float, step: float, precision = 0):
        super().__init__()

        self._value = min
        self._min = min
        self._max = max
        self._step = step
        self._precision = precision

        total_steps = int((max - min) / step)

        vert_layout = QVBoxLayout()
        horz_layout = QHBoxLayout()

        self.title_label = QLabel(title)
        horz_layout.addWidget(self.title_label, 1)

        self.value_label = QLabel("0.0")
        horz_layout.addWidget(self.value_label, 0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(total_steps)
        
        vert_layout.addLayout(horz_layout)
        vert_layout.addWidget(self.slider)
        self.setLayout(vert_layout)

        self.slider.valueChanged.connect(self._value_changed) #type:ignore
        self._value_changed(silent=True)
    
    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float):
        val = max(self._min, min(self._max, val))
        self.slider.setValue(int((val - self._min) / self._step))

    @Slot()
    def _value_changed(self, *, silent=False):
        self._value = self._min + self.slider.value() * self._step
        fmt = f'{{:.{self._precision}f}}'
        self.value_label.setText(fmt.format(self._value))
        if not silent:
            self.changed.emit(self._value)


class ComboControl(QWidget):
    changed = Signal(int)

    def __init__(self, title: str, options: List[str], texts: Optional[List[str]] = None):
        super().__init__()

        if texts is not None:
            assert(len(options) == len(texts))

        self._options = options

        horz_layout = QHBoxLayout()

        self.title_label = QLabel(title)
        horz_layout.addWidget(self.title_label, 1)    

        self.combo_box = QComboBox()
        self.combo_box.addItems(texts or options)
        horz_layout.addWidget(self.combo_box, 1)

        self.setLayout(horz_layout)

        self.combo_box.currentIndexChanged.connect(self._index_changed) #type:ignore

    @property
    def index(self) -> int:
        return self.combo_box.currentIndex()

    @index.setter
    def index(self, idx: int):
        idx = max(0, min(len(self._options) - 1, idx))
        self.combo_box.setCurrentIndex(idx)

    @property
    def option(self) -> str:
        return self.combo_box.currentText()

    @option.setter
    def option(self, opt: str):
        idx = self._options.index(opt)
        self.combo_box.setCurrentIndex(idx)

    @Slot()
    def _index_changed(self):
        self.changed.emit(self.combo_box.currentIndex())


class CheckBoxControl(QWidget):
    changed = Signal(bool)

    def __init__(self, title: str):
        super().__init__()

        horz_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        horz_layout.addWidget(self.title_label, 1)

        self.check_box = QCheckBox()
        horz_layout.addWidget(self.check_box, 0)
        self.setLayout(horz_layout)

        self.check_box.stateChanged.connect(self._checked_changed) #type:ignore

    @property
    def checked(self) -> bool:
        return self.check_box.isChecked()

    @checked.setter
    def checked(self, state: bool):
        self.check_box.setChecked(state)

    @Slot()
    def _checked_changed(self):
        self.changed.emit(self.checked)


class SeedControl(QWidget):
    changed = Signal(int)

    def __init__(self, title: str):
        super().__init__()

        vert_layout = QVBoxLayout()

        horz_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        horz_layout.addWidget(self.title_label, 1)

        self.line_edit = QLineEdit("0")
        horz_layout.addWidget(self.line_edit, 1)

        vert_layout.addLayout(horz_layout)
        horz_layout = QHBoxLayout()

        self.auto_check = QCheckBox("Auto Generate")
        self.auto_check.setChecked(True)
        horz_layout.addStretch(1)
        horz_layout.addWidget(self.auto_check)
        horz_layout.addSpacing(10)
        
        self.randomize_button = QPushButton("\u2684")
        horz_layout.addWidget(self.randomize_button)
        
        vert_layout.addLayout(horz_layout)
        self.setLayout(vert_layout)

        self.line_edit.textChanged.connect(self._text_changed) #type:ignore
        self.randomize_button.clicked.connect(self.generate) #type:ignore

    @property
    def value(self) -> int:
        try:
            return int(self.line_edit.text())
        except:
            return 0

    @value.setter
    def value(self, seed: int):
        self.line_edit.setText(str(seed))
    
    @property
    def auto_generate(self) -> bool:
        return self.auto_check.isChecked()

    @auto_generate.setter
    def auto_generate(self, state: bool):
        self.auto_check.setChecked(state)

    @Slot()
    def generate(self):
        random.seed()
        self.value = random.randint(0, 2**31-1)

    @Slot()
    def _text_changed(self):
        self.changed.emit(self.value)


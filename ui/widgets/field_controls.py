from typing import List, Optional, Any

from PySide6.QtCore import Qt, Signal, Slot

from PySide6.QtWidgets import (
    QWidget,
    QSlider,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
)

from ui.app.utils import generate_random_seed


class FieldControl(QWidget):
    def __init__(self, target: object):
        super().__init__()
        self._target = target

    def update(self):
        raise RuntimeError("must override")

    def set_target(self, target: object):
        self._target = target


class SliderControl(FieldControl):
    changed = Signal(float)

    def __init__(self, title: str, target: object, field: str, type: type,
        min: float, max: float, step: float, precision = 0):
        
        super().__init__(target)

        self._field = field
        self._type = type

        self._value = min
        self._min = min
        self._max = max
        self._step = step
        self._precision = precision

        total_steps = int((max - min) / step)

        vert_layout = QVBoxLayout()
        horz_layout = QHBoxLayout()

        title_label = QLabel(title)
        horz_layout.addWidget(title_label, 1)

        self._value_label = QLabel()
        horz_layout.addWidget(self._value_label, 0)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(total_steps)
        
        vert_layout.addLayout(horz_layout)
        vert_layout.addWidget(self._slider)
        self.setLayout(vert_layout)

        self._slider.valueChanged.connect(self._value_changed) #type:ignore
        self.update()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float):
        val = max(self._min, min(self._max, val))
        self._slider.setValue(int((val - self._min) / self._step))    

    def update(self):
        self.value = float(getattr(self._target, self._field))

    @Slot()
    def _value_changed(self, *, silent=False):
        self._value = self._min + self._slider.value() * self._step
        fmt = f'{{:.{self._precision}f}}'
        self._value_label.setText(fmt.format(self._value))

        setattr(self._target, self._field, self._type(self._value))

        if not silent:
            self.changed.emit(self._value)


class ComboControl(FieldControl):
    changed = Signal(int)

    def __init__(self, title: str, target: object, field: str,
        options: List[Any], labels: Optional[List[str]] = None):
        
        super().__init__(target)

        self._field = field
        self._type = type

        if labels is not None:
            assert(len(options) == len(labels))

        self._options = options
        self._labels = labels

        horz_layout = QHBoxLayout()

        title_label = QLabel(title)
        horz_layout.addWidget(title_label, 1)    

        self._combo_box = QComboBox()
        items = labels if labels else [ str(opt) for opt in options ]
        self._combo_box.addItems(items)
        horz_layout.addWidget(self._combo_box, 1)

        self.setLayout(horz_layout)

        self._combo_box.currentIndexChanged.connect(self._index_changed) #type:ignore
        self.update()

    @property
    def index(self) -> int:
        return self._combo_box.currentIndex()

    @index.setter
    def index(self, idx: int):
        idx = max(0, min(len(self._options) - 1, idx))
        self._combo_box.setCurrentIndex(idx)

    @property
    def option(self) -> Any:
        index = self._combo_box.currentIndex()
        return self._options[index]

    @option.setter
    def option(self, opt: Any):
        idx = self._options.index(opt)
        self._combo_box.setCurrentIndex(idx)

    def update(self):
        self.option = getattr(self._target, self._field)

    @Slot()
    def _index_changed(self):
        setattr(self._target, self._field, self.option)
        self.changed.emit(self.index)


class CheckBoxControl(FieldControl):
    changed = Signal(bool)

    def __init__(self, title: str, target: object, field: str):
        super().__init__(target)

        self._field = field

        horz_layout = QHBoxLayout()
        title_label = QLabel(title)
        horz_layout.addWidget(title_label, 1)

        self._check_box = QCheckBox()
        horz_layout.addWidget(self._check_box, 0)
        self.setLayout(horz_layout)

        self._check_box.stateChanged.connect(self._checked_changed) #type:ignore
        self.update()

    @property
    def checked(self) -> bool:
        return self._check_box.isChecked()

    @checked.setter
    def checked(self, state: bool):
        self._check_box.setChecked(state)

    def update(self):
        self.checked = getattr(self._target, self._field)

    @Slot()
    def _checked_changed(self):
        checked = self.checked
        setattr(self._target, self._field, checked)
        self.changed.emit(checked)


class SpinBoxControl(FieldControl):
    changed = Signal(int)

    def __init__(self, title: str, target: object, field: str, min: int, max: int):
        super().__init__(target)

        self._field = field

        horz_layout = QHBoxLayout()
        title_label = QLabel(title)
        horz_layout.addWidget(title_label, 1)

        self._spin_box = QSpinBox()
        self._spin_box.setMinimum(min)
        self._spin_box.setMaximum(max)
        horz_layout.addWidget(self._spin_box, 0)
        self.setLayout(horz_layout)

        self._spin_box.valueChanged.connect(self._value_changed) #type:ignore
        self.update()

    @property
    def value(self) -> int:
        return self._spin_box.value()

    @value.setter
    def value(self, val: int):
        self._spin_box.setValue(val)

    def update(self):
        self.value = getattr(self._target, self._field)

    @Slot()
    def _value_changed(self):
        value = self.value
        setattr(self._target, self._field, value)
        self.changed.emit(value)


class SeedControl(FieldControl):
    changed = Signal(int)
    randomize_changed = Signal(bool)

    def __init__(self, title: str, target: object,
        value_field: str, randomize_enabled_field: str = ""):
        
        super().__init__(target)

        self._value_field = value_field
        self._randomize_enabled_field = randomize_enabled_field

        vert_layout = QVBoxLayout()

        horz_layout = QHBoxLayout()
        title_label = QLabel(title)
        horz_layout.addWidget(title_label, 1)

        self._line_edit = QLineEdit("0")
        horz_layout.addWidget(self._line_edit, 1)

        vert_layout.addLayout(horz_layout)
        horz_layout = QHBoxLayout()
        horz_layout.addStretch(1)

        if randomize_enabled_field:
            self._random_check = QCheckBox("Randomize")
            self._random_check.setChecked(True)
            horz_layout.addWidget(self._random_check)
            horz_layout.addSpacing(10)
        
        self._randomize_button = QPushButton("\u2684")
        horz_layout.addWidget(self._randomize_button)
        
        vert_layout.addLayout(horz_layout)
        self.setLayout(vert_layout)

        self._line_edit.textChanged.connect(self._text_changed) #type:ignore
        self._randomize_button.clicked.connect(self.randomize) #type:ignore

        if randomize_enabled_field:
            self._random_check.stateChanged.connect(self._randomize_changed) #type:ignore

        self.update()

    @property
    def value(self) -> int:
        try:
            return int(self._line_edit.text())
        except:
            return 0

    @value.setter
    def value(self, seed: int):
        self._line_edit.setText(str(seed))
    
    @property
    def randomize_enabled(self) -> bool:
        if self._randomize_enabled_field:
            return self._random_check.isChecked()
        else:
            raise RuntimeError("no randomize option")

    @randomize_enabled.setter
    def randomize_enabled(self, state: bool):
        if self._randomize_enabled_field:
            self._random_check.setChecked(state)
        else:
            raise RuntimeError("no randomize option")

    def update(self):
        self.value = getattr(self._target, self._value_field)
        if self._randomize_enabled_field:
            self.randomize_enabled = getattr(self._target, self._randomize_enabled_field)

    @Slot()
    def randomize(self):
        self.value = generate_random_seed()

    @Slot()
    def _text_changed(self):
        value = self.value
        setattr(self._target, self._value_field, value)
        self.changed.emit(value)

    @Slot()
    def _randomize_changed(self):
        enabled = self.randomize_enabled
        setattr(self._target, self._randomize_enabled_field, enabled)
        self.randomize_changed.emit(enabled)
import sys
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication

from ui.widgets import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    style_path = Path(__file__).parent / "styles.qss"
    style_file = QFile(style_path)
    if style_file.open(QFile.ReadOnly):
        style_sheet = style_file.readAll().toStdString()
        app.setStyleSheet(style_sheet)
    else:
        print(f"failed to read style file: {style_path}")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


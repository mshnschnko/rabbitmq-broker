from PyQt5.QtWidgets import QMessageBox, QWidget

class ErrorMessageBox(QMessageBox):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Ошибка')
        self.setText(text)
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Ok)
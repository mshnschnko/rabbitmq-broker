from PyQt5.QtWidgets import QMessageBox, QWidget

class ServerErrorMessageBox(QMessageBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Ошибка")
        self.setText("Не удалось связаться с сервером")
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Ok)
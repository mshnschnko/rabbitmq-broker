from PyQt5.QtWidgets import QMessageBox

from main_window import MainWindow
from broker_interactions import Interacter

from config import SERVER_ERROR_MESSAGE, ERROR_WINDOW_TITLE

class Controller:
    def __init__(self) -> None:
        self.broker_interacter = Interacter()
        self.main_window = MainWindow()
        self.main_window.multiply_btn_clicked.connect(self.__on_multiply_btn_clicked)
        self.main_window.show()

    def __on_multiply_btn_clicked(self, number: str) -> None:
        try:
            result = self.broker_interacter.call(int(number))
            self.main_window.set_response_number(str(result))
        except TypeError as te:
            result = ''
            self.main_window.set_response_number(str(result))
            mb = QMessageBox(self.main_window)
            mb.setWindowTitle(ERROR_WINDOW_TITLE)
            mb.setText(SERVER_ERROR_MESSAGE)
            mb.setIcon(QMessageBox.Critical)
            mb.setStandardButtons(QMessageBox.Ok)
            mb.exec()
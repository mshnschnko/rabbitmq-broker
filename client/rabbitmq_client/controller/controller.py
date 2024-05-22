from PyQt5.QtWidgets import QMessageBox

from widgets import MainWindow
from broker_interactions import Interacter

from log_config import LOGGER_NAME
from logger import get_logger

logger = get_logger(LOGGER_NAME)

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
            mb.setWindowTitle("Ошибка")
            mb.setText("Не удалось связаться с сервером")
            mb.setIcon(QMessageBox.Critical)
            mb.setStandardButtons(QMessageBox.Ok)
            mb.exec()
        except ValueError as ve:
            logger.error(f"Invalid data: {ve}")
            raise ve
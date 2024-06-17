from PyQt5.QtWidgets import QMessageBox

from widgets import MainWindow, ErrorMessageBox
from broker_interactions import Interacter

from logger import Logger

logger = Logger()

class Controller:
    def __init__(self) -> None:
        self.broker_interacter = Interacter()
        self.main_window = MainWindow()
        self.main_window.server_connect.connect(self.__change_server_connection_status)
        self.main_window.multiply_btn_clicked.connect(self.__on_multiply_btn_clicked)
        self.main_window.show()

    def __change_server_connection_status(self, to_connect: bool) -> None:
        if to_connect:
            try:
                self.broker_interacter.connect()
                self.main_window.connected_succesfully.emit(True)
            except:
                self.main_window.connected_succesfully.emit(False)
        else:
            self.broker_interacter.disconnect()

    def __on_multiply_btn_clicked(self, number: str) -> None:
        try:
            result = self.broker_interacter.call(int(number))
            self.main_window.set_response_number(str(result))
        except TypeError as te:
            logger.error(f"Failed to connect to server")
            self.main_window.set_response_number('')
            mb = ErrorMessageBox("Не удалось связаться с сервером", self.main_window)
            mb.exec()
        except ValueError as ve:
            logger.error(f"Invalid data: {ve}")
            mb = ErrorMessageBox("Неверное число", self.main_window)
            mb.exec()
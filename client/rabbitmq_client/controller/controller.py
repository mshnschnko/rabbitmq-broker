from PyQt5.QtWidgets import QMessageBox

from widgets import MainWindow, ServerErrorMessageBox
from broker_interactions import Interacter

from log_config import LogConfig
from logger import get_logger

log_config = LogConfig()
logger = get_logger(log_config.logger_name)

class Controller:
    def __init__(self) -> None:
        self.broker_interacter = None
        self.main_window = MainWindow()
        self.main_window.server_connect.connect(self.__change_server_connection_status)
        self.main_window.multiply_btn_clicked.connect(self.__on_multiply_btn_clicked)
        self.main_window.show()

    def __change_server_connection_status(self, to_connect: bool) -> None:
        print(to_connect)
        if to_connect:
            try:
                self.broker_interacter = Interacter()
                self.main_window.connected_succesfully.emit(True)
            except:
                self.main_window.connected_succesfully.emit(False)
        else:
            print('else')
            if self.broker_interacter:
                print('del')
                del self.broker_interacter

    def __on_multiply_btn_clicked(self, number: str) -> None:
        try:
            result = self.broker_interacter.call(int(number))
            self.main_window.set_response_number(str(result))
        except TypeError as te:
            result = ''
            self.main_window.set_response_number(str(result))
            mb = ServerErrorMessageBox(self.main_window)
            mb.exec()
        except ValueError as ve:
            logger.error(f"Invalid data: {ve}")
            raise ve
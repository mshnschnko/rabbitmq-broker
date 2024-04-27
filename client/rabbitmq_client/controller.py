from main_window import MainWindow
from broker_interactions import Interacter

class Controller:
    def __init__(self) -> None:
        self.broker_interacter = Interacter()
        self.main_window = MainWindow()
        self.main_window.multiply_btn_clicked.connect(self.__on_multiply_btn_clicked)
        self.main_window.show()

    def __on_multiply_btn_clicked(self, number: str) -> None:
        result = self.broker_interacter.call(number)
        self.main_window.set_response_number(result)
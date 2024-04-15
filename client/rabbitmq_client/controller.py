from main_window import MainWindow
from broker_interactions import Sender, Receiver

class Controller:
    def __init__(self) -> None:
        self.broker_sender = Sender()
        self.main_window = MainWindow()
        self.main_window.multiply_btn_clicked.connect(self.__on_multiply_btn_clicked)
        self.main_window.show()
        self.broker_receiver = Receiver()

    def __on_multiply_btn_clicked(self, number: str) -> None:
        self.broker_sender.send_message(number)
from PyQt5.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QRegularExpressionValidator

from ui.main_window import Ui_MainWindow
from . import ConfigEditor

from config import HOST, PORT

class MainWindow(QMainWindow):
    multiply_btn_clicked = pyqtSignal(str)
    server_connect = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.__is_connected = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow=self)
        
        self.ui.address_label.setText(f'{HOST}:{PORT}')

        self.ui.connect_btn.clicked.connect(self.connect_server)

        self.ui.settings_btn.clicked.connect(self.__on_settings_btn_clicked)
        
        regex = QRegularExpression("^-?[0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.ui.number_line_edit.setValidator(validator)
        self.ui.number_line_edit.textChanged.connect(lambda: self.ui.multiply_btn.setEnabled(len(self.ui.number_line_edit.text()) > 0))
        
        self.ui.multiply_btn.setEnabled(False)
        self.ui.multiply_btn.clicked.connect(self.__on_multiply_btn_clicked)

    def connect_server(self) -> None:
        if self.__is_connected:
            self.ui.connect_btn.setText("Подключиться")
        else:
            self.ui.connect_btn.setText("Отключиться")
        self.__is_connected = not self.__is_connected
        self.ui.number_line_edit.setEnabled(self.__is_connected)
        self.ui.multiply_btn.setEnabled(self.__is_connected)

    def __on_settings_btn_clicked(self):
        config_editor = ConfigEditor('rabbitmq_client/app.ini', 'rabbitmq_client/logger.ini')
        config_editor.show()

    def __on_multiply_btn_clicked(self) -> None:
        self.multiply_btn_clicked.emit(self.ui.number_line_edit.text())

    def set_response_number(self, n: str) -> None:
        self.ui.multiplied_number_label.setText(n)
        
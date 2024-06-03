from PyQt5.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QRegularExpressionValidator

from ui.main_window import Ui_MainWindow
from . import ConfigEditor
from . import ErrorMessageBox

from config import Config

class MainWindow(QMainWindow):
    multiply_btn_clicked = pyqtSignal(str)
    server_connect = pyqtSignal(bool)
    connected_succesfully = pyqtSignal(bool)

    config = Config()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__is_connected = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow=self)
        
        self.ui.address_label.setText(f'{self.config.host}:{self.config.port}')

        regex = QRegularExpression("^-?[0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.ui.number_line_edit.setValidator(validator)
        
        self.ui.multiply_btn.setEnabled(False)

        self.ui.number_line_edit.textChanged.connect(lambda: self.ui.multiply_btn.setEnabled(len(self.ui.number_line_edit.text()) > 0))
        self.ui.connect_btn.clicked.connect(self.__connect_server)
        self.ui.settings_btn.clicked.connect(self.__on_settings_btn_clicked)
        self.ui.multiply_btn.clicked.connect(self.__on_multiply_btn_clicked)
        self.connected_succesfully.connect(self.__on_connected)

    def __connect_server(self) -> None:
        if self.__is_connected:
            self.ui.connect_btn.setText("Подключиться")
            self.server_connect.emit(False)
            self.__is_connected = False
            self.ui.number_line_edit.setEnabled(False)
            self.ui.multiply_btn.setEnabled(False)
            self.ui.number_line_edit.setText('')
            self.ui.multiplied_number_label.setText('')
        else:
            self.server_connect.emit(True)

    def __on_connected(self, connected: bool) -> None:
        if connected:
            self.__is_connected = True
            self.ui.connect_btn.setText("Отключиться")
            self.ui.number_line_edit.setEnabled(True)
            self.ui.multiply_btn.setEnabled(True)
        else:
            self.__is_connected = False
            self.ui.number_line_edit.setEnabled(False)
            self.ui.multiply_btn.setEnabled(False)
            mb = ErrorMessageBox("Не удалось связаться с сервером", self)
            mb.exec()


    def __on_settings_btn_clicked(self):
        config_editor = ConfigEditor('rabbitmq_client/app.ini', 'rabbitmq_client/logger.ini')
        config_editor.settings_changed.connect(self.__on_settings_changed)
        config_editor.show()

    def __on_multiply_btn_clicked(self) -> None:
        self.multiply_btn_clicked.emit(self.ui.number_line_edit.text())

    def __on_settings_changed(self):
        self.ui.address_label.setText(f'{self.config.host}:{self.config.port}')
        self.ui.connect_btn.click()

    def set_response_number(self, n: str) -> None:
        self.ui.multiplied_number_label.setText(n)

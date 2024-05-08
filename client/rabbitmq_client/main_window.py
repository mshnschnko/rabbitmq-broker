from PyQt5.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QRegularExpressionValidator

from ui.main_window import Ui_MainWindow
from config_editor import ConfigEditor


class MainWindow(QMainWindow):
    multiply_btn_clicked = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow=self)
        
        self.ui.settings_btn.clicked.connect(self.__on_settings_btn_clicked)
        
        regex = QRegularExpression("^-?[0-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.ui.number_line_edit.setValidator(validator)
        self.ui.number_line_edit.textChanged.connect(lambda: self.ui.multiply_btn.setEnabled(len(self.ui.number_line_edit.text()) > 0))
        
        self.ui.multiply_btn.setEnabled(False)
        self.ui.multiply_btn.clicked.connect(self.__on_multiply_btn_clicked)

    def __on_settings_btn_clicked(self):
        config_editor = ConfigEditor('rabbitmq_client/app.ini')
        config_editor.show()

    def __on_multiply_btn_clicked(self) -> None:
        self.multiply_btn_clicked.emit(self.ui.number_line_edit.text())

    def set_response_number(self, n: str) -> None:
        self.ui.multiplied_number_label.setText(n)
        
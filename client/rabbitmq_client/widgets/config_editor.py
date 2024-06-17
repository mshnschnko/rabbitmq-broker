import re

from PyQt5.QtWidgets import QWidget, QFileDialog, QDialog
from PyQt5.QtCore import QRegularExpression, QDir, Qt, pyqtSignal
from PyQt5.QtGui import QRegularExpressionValidator, QFontMetrics

from ui.config_edit_window import Ui_Config_edit_window

from config import Config
from log_config import LogConfig
from logger import Logger


class ConfigEditor(QDialog):
    settings_changed = pyqtSignal()
    config = Config()
    log_config = LogConfig()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.logfile_path = None

        self.ui = Ui_Config_edit_window()
        self.ui.setupUi(Config_edit_window=self)


        regex = QRegularExpression("^[1-9]+$")
        validator = QRegularExpressionValidator(regex)
        self.ui.time_limit_edit.setValidator(validator)

        self.ui.logfile_name_label.setMinimumWidth(300)
        self.ui.logfile_name_label.setWordWrap(False)
        self.ui.logfile_name_label.setTextInteractionFlags(self.ui.logfile_name_label.textInteractionFlags() | Qt.TextSelectableByMouse)

        self.set_current_settings_into_window()
        self.ui.time_limit_checkbox.stateChanged.connect(self.on_time_limit_checkbox_state_changed)

        self.ui.browse_logfile_btn.clicked.connect(self.on_browse_logfile_button_clicked)
        
        self.ui.cancel_btn.clicked.connect(lambda: self.close())
        self.ui.save_btn.clicked.connect(self.on_save_button_clicked)

    def set_current_settings_into_window(self) -> None:
        self.ui.host_ip_edit.setText(self.config.host)
        self.ui.port_edit.setText(str(self.config.port))
        self.ui.server_queue_edit.setText(self.config.server_queue)
        self.ui.log_level_combobox.setCurrentText(self.log_config.level)
        self.ui.logfile_name_label.setText(self.log_config.filename)
        self.ui.logfile_name_label.setToolTip(self.log_config.filename)
        self.elideText()
        if self.config.waiting_time != 'None':
            self.ui.time_limit_edit.setText(self.config.waiting_time)
            self.ui.time_limit_checkbox.setChecked(True)
            self.ui.time_limit_edit.setEnabled(True)
            self.ui.time_limit_label.setEnabled(True)
        else:
            self.ui.time_limit_checkbox.setChecked(False)

    def on_time_limit_checkbox_state_changed(self) -> None:
        self.ui.time_limit_edit.setEnabled(self.ui.time_limit_checkbox.isChecked())
        self.ui.time_limit_label.setEnabled(self.ui.time_limit_checkbox.isChecked())

    def on_browse_logfile_button_clicked(self) -> None:
        self.logfile_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", QDir.homePath(), "Log (*.log)")
        if self.logfile_path:
            self.ui.logfile_name_label.setText(self.logfile_path)
            self.ui.logfile_name_label.setToolTip(self.logfile_path)
            self.elideText()

    def elideText(self):
        metrics = QFontMetrics(self.ui.logfile_name_label.font())
        elidedText = metrics.elidedText(self.ui.logfile_name_label.text(), Qt.ElideRight, self.ui.logfile_name_label.width())
        self.ui.logfile_name_label.setText(elidedText)

    def on_save_button_clicked(self) -> None:
        self.config.host = self.ui.host_ip_edit.text()
        self.config.port = self.ui.port_edit.text()
        self.config.server_queue = self.ui.server_queue_edit.text()
        self.config.waiting_time = "None" if not self.ui.time_limit_checkbox.isChecked() or len(self.ui.time_limit_edit.text()) == 0 else self.ui.time_limit_edit.text()

        self.config.update_config_file()

        self.log_config.level = self.ui.log_level_combobox.currentText()
        self.log_config.filename = self.logfile_path

        self.log_config.update_config_file()
        logger = Logger()
        logger.update_config()

        self.close()
        self.settings_changed.emit()


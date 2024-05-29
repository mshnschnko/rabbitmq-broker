import re

from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import QRegularExpression, QDir, Qt, pyqtSignal
from PyQt5.QtGui import QRegularExpressionValidator, QFontMetrics

from ui.config_edit_window import Ui_Config_edit_window

from config import Config
from log_config import LogConfig


class ConfigEditor(QWidget):
    settings_changed = pyqtSignal()
    config = Config()
    log_config = LogConfig()

    def __init__(self, app_config_path: str, logger_config_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        print('editor conf', self.config)

        self.__app_config_path = app_config_path
        self.__logger_config_path = logger_config_path
        
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

    def on_time_limit_checkbox_state_changed(self) -> None:
        self.ui.time_limit_edit.setEnabled(self.ui.time_limit_checkbox.isChecked())
        self.ui.time_limit_label.setEnabled(self.ui.time_limit_checkbox.isChecked())

    def on_browse_logfile_button_clicked(self) -> None:
        logfile_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", QDir.homePath(), "Log (*.log)")
        if logfile_path:
            self.ui.logfile_name_label.setText(logfile_path)
            self.ui.logfile_name_label.setToolTip(logfile_path)
            self.elideText()

    def elideText(self):
        metrics = QFontMetrics(self.ui.logfile_name_label.font())
        elidedText = metrics.elidedText(self.ui.logfile_name_label.text(), Qt.ElideRight, self.ui.logfile_name_label.width())
        self.ui.logfile_name_label.setText(elidedText)

    def on_save_button_clicked(self) -> None:
        with open(self.__app_config_path, 'w') as app_confige_file:
            app_confige_file.write('[broker]\n')
            app_confige_file.write(f'host={self.ui.host_ip_edit.text()}\n')
            app_confige_file.write(f'port={self.ui.port_edit.text()}\n')
            app_confige_file.write(f'waiting_time={"None" if not self.ui.time_limit_checkbox.isChecked() else self.ui.time_limit_edit.text()}\n')
            app_confige_file.write('\n[server]\n')
            app_confige_file.write(f'queue={self.ui.server_queue_edit.text()}\n')

        with open(self.__logger_config_path, 'r+') as logger_config_file:
            data = logger_config_file.read()
            print(self.ui.log_level_combobox.currentText())
            data = re.sub(r'^level=.*$', f'level={self.ui.log_level_combobox.currentText()}', data, flags=re.MULTILINE)
            data = re.sub(r'^file=.*$', f'file = {self.ui.logfile_name_label.text()}', data, flags=re.MULTILINE)
            logger_config_file.seek(0)
            logger_config_file.write(data)
            logger_config_file.truncate()

        self.config.read_config()
        self.log_config.read_config()
        self.close()
        self.settings_changed.emit()


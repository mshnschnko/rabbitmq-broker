import sys
import os
import subprocess

from PyQt5.QtWidgets import QWidget, QMessageBox

from ui.config_edit_window import Ui_Config_edit_window

from config import REBOOT_WARNING_MESSAGE, REBOOT_WARNING_TITLE

def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def restart_with_venv():
    venv_python = os.path.join(sys.prefix, 'bin', 'python')
    if sys.platform.startswith('win'):
        venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')
    subprocess.Popen([venv_python] + sys.argv)
    sys.exit()



class ConfigEditor(QWidget):
    def __init__(self, config_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.config_path = config_path
        
        self.ui = Ui_Config_edit_window()
        self.ui.setupUi(Config_edit_window=self)

        self.set_current_config_text()
        
        self.ui.cancel_btn.clicked.connect(lambda: self.close())
        self.ui.save_btn.clicked.connect(self.on_save_button_clicked)

    def set_current_config_text(self) -> None:
        with open(self.config_path, 'r') as confige_file:
            text = confige_file.read()
        self.ui.config_edit.setText(text)

    def on_save_button_clicked(self) -> None:
        mb = QMessageBox(self)
        mb.setWindowTitle(REBOOT_WARNING_TITLE)
        mb.setText(REBOOT_WARNING_MESSAGE)
        mb.setIcon(QMessageBox.Warning)
        yes_btn = mb.addButton(QMessageBox.Yes)
        yes_btn.setText('Да')
        no_btn = mb.addButton(QMessageBox.No)
        no_btn.setText('Нет')
        result = mb.exec()
        
        if result == QMessageBox.Yes:
            with open(self.config_path, 'w') as confige_file:
                confige_file.write(self.ui.config_edit.toPlainText())
            self.close()
            restart_with_venv()
        else:
            self.close()

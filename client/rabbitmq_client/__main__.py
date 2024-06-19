import sys
from PyQt5.QtWidgets import QApplication
from controller import Controller

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    app.exec()


if __name__ == '__main__':
    sys.exit(main())

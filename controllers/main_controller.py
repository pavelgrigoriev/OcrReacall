from PyQt6 import QtWidgets
from ui_mainwindow import Ui_MainWindow
import sys


class MainController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(self.MainWindow)

    def show(self):
        self.MainWindow.show()
        sys.exit(self.app.exec())

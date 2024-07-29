from PyQt6 import QtWidgets
from views.main_view import MainView
import sys


class MainController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        ui = MainView()
        ui.setupUi(self.MainWindow)

    def show(self):
        self.MainWindow.show()
        sys.exit(self.app.exec())

from PyQt6 import QtWidgets
from views.main_view import MainView
import sys


class MainController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.view = MainView()

    def show(self):
        self.view.show()
        sys.exit(self.app.exec())

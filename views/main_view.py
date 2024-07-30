import logging
from PyQt6 import QtWidgets, uic, QtGui
from logger import setup_logging

setup_logging()


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        uic.loadUi('views/ui/mainwindow.ui', self)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        logging.info("Application is closing")
        event.accept()

import logging
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from logger import setup_logging

setup_logging()


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        uic.loadUi('views/ui/mainwindow.ui', self)
        self.image_paths = []

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        logging.info("Application is closing")
        event.accept()

    # def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
    #     super().resizeEvent(event)
    #     self.resize_timer.start(200)  # Delay resize handling by 200 ms

    # def update_display_images(self):
    #     if self.image_paths:
    #         self.display_images(self.image_paths)

    def display_images(self, image_paths):
        pass

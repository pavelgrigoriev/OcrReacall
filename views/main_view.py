import logging
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from logger import setup_logging

setup_logging()


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        uic.loadUi('views/ui/mainwindow.ui', self)
        self.image_paths = []
        self.image_grid_layout = self.findChild(
            QtWidgets.QGridLayout, 'gridLayout_3')

        # Add a timer to delay textChanged event handling
        self.search_timer = QtCore.QTimer()
        self.search_timer.setSingleShot(True)

        self.lineEdit.textChanged.connect(self.on_text_changed)

        # Resize timer for handling window resize events
        self.resize_timer = QtCore.QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_display_images)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        logging.info("Application is closing")
        event.accept()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize_timer.start(200)  # Delay resize handling by 200 ms

    def on_text_changed(self):
        self.search_timer.start(300)  # Delay search handling by 300 ms

    def display_images(self, image_paths):
        self.clear_layout(self.image_grid_layout)  # Clear existing images
        self.image_paths = image_paths

        # Get the size of the scroll area to adjust image size
        scroll_area_size = self.scrollArea.size()
        min_image_size = 100
        max_columns = max(1, scroll_area_size.width() // (min_image_size + 10))

        row = 0
        col = 0
        for index, image_path in enumerate(image_paths):
            label = QLabel()
            pixmap = QPixmap(image_path)
            image_size = min(scroll_area_size.width() //
                             max_columns - 10, min_image_size)
            label.setPixmap(pixmap.scaled(image_size, image_size,
                            QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.image_grid_layout.addWidget(label, row, col)
            col += 1
            if col >= max_columns:  # Adjust number of columns as needed
                col = 0
                row += 1

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_display_images(self):
        if self.image_paths:
            self.display_images(self.image_paths)

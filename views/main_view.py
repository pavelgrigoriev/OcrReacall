import logging
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel
from logger import setup_logging

setup_logging()


class ImageLoader(QtCore.QObject):
    image_loaded = QtCore.pyqtSignal(str, QPixmap)

    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def load_images(self):
        for image_path in self.image_paths:
            pixmap = QPixmap(image_path)
            self.image_loaded.emit(image_path, pixmap)


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

        # Image cache to store scaled pixmaps
        self.image_cache = {}

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        logging.info("Application is closing")
        event.accept()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize_timer.start(200)  # Delay resize handling by 200 ms

    def on_text_changed(self):
        self.search_timer.start(300)  # Delay search handling by 300 ms

    def display_images(self, results):
        self.clear_layout(self.image_grid_layout)  # Clear existing images
        self.image_paths = [result[0] for result in results]

        # Asynchronously load images
        self.thread = QtCore.QThread()
        self.image_loader = ImageLoader(self.image_paths)
        self.image_loader.moveToThread(self.thread)
        self.image_loader.image_loaded.connect(self.on_image_loaded)
        self.thread.started.connect(self.image_loader.load_images)
        self.thread.start()

    def on_image_loaded(self, image_path, pixmap):
        if pixmap.isNull():
            logging.error(f"Failed to load image: {image_path}")
            return

        self.image_cache[image_path] = pixmap
        self.update_display_images()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_display_images(self):
        self.clear_layout(self.image_grid_layout)
        scroll_area_size = self.scrollArea.size()
        min_image_size = 500
        max_columns = max(1, scroll_area_size.width() // (min_image_size + 10))

        row = 0
        col = 0
        for image_path in self.image_paths:
            if image_path in self.image_cache:
                pixmap = self.image_cache[image_path]
                label = QLabel()
                image_size = min(scroll_area_size.width() //
                                 max_columns - 10, min_image_size)
                scaled_pixmap = pixmap.scaled(
                    image_size, image_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(scaled_pixmap)
                self.image_grid_layout.addWidget(label, row, col)
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

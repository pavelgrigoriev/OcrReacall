import logging
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
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

        self.load_stylesheet()

    def load_stylesheet(self):
        # Load the stylesheet from an external file
        with open("views/styles/styles.css", "r") as file:
            self.setStyleSheet(file.read())

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
        self.image_paths = [(result[0], result[2])
                            for result in results]  # Store path and caption

        # Asynchronously load images
        self.thread = QtCore.QThread()
        self.image_loader = ImageLoader([path for path, _ in self.image_paths])
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
        for image_path, caption in self.image_paths:
            if image_path in self.image_cache:
                pixmap = self.image_cache[image_path]
                image_size = min(scroll_area_size.width() //
                                 max_columns - 10, min_image_size)

                # Create container widget
                container = QWidget()
                container_layout = QVBoxLayout()
                container.setLayout(container_layout)
                container.setObjectName("container")

                # Create and set image label
                image_label = QLabel()
                scaled_pixmap = pixmap.scaled(
                    image_size, image_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)

                # Create and set caption label
                caption_label = QLabel(caption)
                caption_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                caption_label.setObjectName("caption")

                # Add image and caption to the container layout
                container_layout.addWidget(image_label)
                container_layout.addWidget(caption_label)

                # Add container to the grid layout
                self.image_grid_layout.addWidget(container, row, col)

                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

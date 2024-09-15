import logging
from PyQt6.QtWidgets import QLabel, QPushButton, QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import uic, QtWidgets


class FullscreenImageDialog(QDialog):
    def __init__(self, image_paths, current_index=0):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.image_paths = image_paths
        self.current_index = current_index

        uic.loadUi('views/ui/fullscreen_image_dialog.ui', self)

        self.image_label = self.findChild(QLabel, "imageLabel")
        self.prev_button = self.findChild(QPushButton, "prevButton")
        self.next_button = self.findChild(QPushButton, "nextButton")

        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)

        self.update_image()
        self.showMaximized()

    def update_image(self):
        image_path = self.image_paths[self.current_index][0]
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            logging.error(f"Failed to load image: {
                          self.image_paths[self.current_index]}")
            return

        # Automatically scale the pixmap to fit within the window while preserving the aspect ratio
        window_size = self.size()
        scaled_pixmap = pixmap.scaled(
            window_size.width(), window_size.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)

        # Enable/Disable buttons based on the current image index
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(
            self.current_index < len(self.image_paths) - 1)

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.update_image()

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap


class ImageLoader(QtCore.QThread):
    image_loaded = QtCore.pyqtSignal(str, QPixmap)

    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def run(self):
        for image_path in self.image_paths:
            pixmap = QPixmap(image_path)
            thumbnail_pixmap = pixmap.scaled(
                499, 400, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            self.image_loaded.emit(image_path, thumbnail_pixmap)

from PyQt6.QtGui import QPixmap
import logging
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from logger import setup_logging
from PyQt6.QtCore import Qt

from views.fullscreen_image_dialog import FullscreenImageDialog

setup_logging()


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        uic.loadUi('views/ui/mainwindow.ui', self)
        self.image_paths = []
        self.current_page = 1
        self.images_per_page = 12
        self.total_pages = 1

        self.image_grid_layout = self.findChild(
            QtWidgets.QGridLayout, 'gridLayout_3')
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, 'scrollArea')

        self.prev_button = self.findChild(QPushButton, 'pushButton')
        self.next_button = self.findChild(QPushButton, 'pushButton_2')
        self.page_info_label = self.findChild(QLabel, 'label')

        self.search_timer = QtCore.QTimer()
        self.search_timer.setSingleShot(True)
        self.lineEdit.textChanged.connect(self.on_text_changed)

        self.resize_timer = QtCore.QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_display_images)

        self.image_cache = {}
        # Таймер для постепенной отрисовки миниатюр
        self.render_timer = QtCore.QTimer()
        self.render_timer.timeout.connect(self.update_display_images)
        self.render_timer.setInterval(100)  # Отрисовывать с паузой в 100 мс

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        logging.info("Application is closing")
        event.accept()

    def open_fullscreen_image(self, current_index):
        dialog = FullscreenImageDialog(self.image_paths, current_index)
        dialog.exec()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize_timer.start(100)

    def on_text_changed(self):
        self.search_timer.start(300)

    def refresh_images(self, results):
        self.clear_image_grid()
        self.set_page_info(results)

    def clear_image_grid(self):
        self.clear_layout(self.image_grid_layout)

    def set_page_info(self, results):
        self.image_paths = [(result[0], result[2]) for result in results]
        self.total_pages = (len(self.image_paths) +
                            self.images_per_page - 1) // self.images_per_page
        self.current_page = 1

    def on_image_loaded(self, image_path, pixmap):
        if pixmap.isNull():
            logging.error(f"Failed to load image: {image_path}")
            return

        self.image_cache[image_path] = pixmap
        self.render_timer.start()  # Запускаем/перезапускаем таймер для постепенной отрисовки

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_display_images(self):
        # Загружаем изображения по одному
        if not self.image_paths:
            return

        scroll_area_size = self.scroll_area.size()
        min_image_size = 500
        max_columns = max(1, scroll_area_size.width() // (min_image_size + 10))

        start_index = (self.current_page - 1) * self.images_per_page
        end_index = min(start_index + self.images_per_page,
                        len(self.image_paths))

        row = 0
        col = 0
        for image_path, caption in self.image_paths[start_index:end_index]:
            pixmap = self.image_cache.get(image_path, QPixmap())

            image_size = min(scroll_area_size.width() //
                             max_columns - 10, min_image_size)

            # Создаем контейнер и миниатюру
            container = QtWidgets.QWidget()
            container_layout = QtWidgets.QVBoxLayout()
            container.setLayout(container_layout)

            image_label = QtWidgets.QLabel()
            scaled_pixmap = pixmap.scaled(
                image_size, image_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)

            caption_label = QtWidgets.QLabel(caption)
            caption_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            container_layout.addWidget(image_label)
            container_layout.addWidget(caption_label)

            self.image_grid_layout.addWidget(container, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        # Останавливаем таймер, если все изображения отрисованы
        if len(self.image_paths) == len(self.image_cache):
            self.render_timer.stop()

        self.update_page_info()

    def update_page_info(self):
        self.page_info_label.setText(
            f"Страница {self.current_page} из {self.total_pages}")
        self.prev_button.setEnabled(self.current_page > 1)
        self.next_button.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_display_images()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_display_images()
            self.update_display_images()

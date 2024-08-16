from PyQt6.QtCore import QObject
from views.main_view import MainView
from controllers.db_controller import DbController
from controllers.ocr_controller import OcrController
from workers.ocr_worker import OcrWorker
from workers.image_loader import ImageLoader


class MainController(QObject):
    def __init__(self, config_manager):
        super().__init__()
        self.db_controller = DbController(config_manager)
        self.ocr_controller = OcrController(config_manager, self.db_controller)
        self.view = MainView()
        self.view.search_timer.timeout.connect(self.search_ocr_results)
        self.view.prev_button.clicked.connect(self.prev_page)
        self.view.next_button.clicked.connect(self.next_page)
        self.ocr_worker = OcrWorker(
            self.ocr_controller.ocr_model, self.db_controller)
        self.ocr_worker.start()
        self.image_loader = None

    def search_ocr_results(self):
        search_term = self.view.lineEdit.text()
        if not search_term.strip():
            return
        results = self.db_controller.search_like(search_term)
        self.view.refresh_images(results)
        self.load_images([result[0] for result in results])

    def load_images(self, image_paths):
        if self.image_loader is not None:
            self.image_loader.quit()
            self.image_loader.wait()

        # Список путей изображений только для текущей страницы
        start_index = (self.view.current_page - 1) * self.view.images_per_page
        end_index = min(
            start_index + self.view.images_per_page, len(image_paths))
        page_image_paths = image_paths[start_index:end_index]

        self.image_loader = ImageLoader(page_image_paths)
        self.image_loader.image_loaded.connect(self.view.on_image_loaded)
        self.image_loader.start()

    def prev_page(self):
        if self.view.current_page > 1:
            self.view.current_page -= 1
            # Загрузка изображений для новой страницы
            self.load_images([result[0] for result in self.view.image_paths])
            self.view.update_display_images()

    def next_page(self):
        if self.view.current_page < self.view.total_pages:
            self.view.current_page += 1
            # Загрузка изображений для новой страницы
            self.load_images([result[0] for result in self.view.image_paths])
            self.view.update_display_images()

    def run(self):
        self.view.show()

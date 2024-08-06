from views.main_view import MainView
from controllers.db_controller import DbController
from controllers.ocr_controller import OcrController


class MainController():
    def __init__(self, config_manager):
        self.db_controller = DbController(config_manager)
        self.ocr_controller = OcrController(
            config_manager, self.db_controller)
        self.view = MainView()
        self.setup_connections()

    def setup_connections(self):
        # Подключение сигнала textChanged к методу поиска
        self.view.lineEdit.textChanged.connect(self.search_ocr_results)

    def search_ocr_results(self):
        search_term = self.view.lineEdit.text()
        results = self.db_controller.search_like(search_term)
        image_paths = [result[0] for result in results]
        self.view.display_images(image_paths)

    def run(self):
        self.view.show()
        self.ocr_controller.start_screenshot_loop()

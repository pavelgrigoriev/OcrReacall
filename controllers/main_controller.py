from views.main_view import MainView
from controllers.db_controller import DbController
from controllers.ocr_controller import OcrController


class MainController():
    def __init__(self, config_manager):
        self.db_controller = DbController(config_manager)
        self.ocr_controller = OcrController(
            config_manager, self.db_controller)
        self.view = MainView()

    def setup_connections(self):
        self.view.pushButton.clicked.connect(self.search_ocr_results)

    def search_ocr_results(self):
        search_term = self.view.lineEdit.text()
        results = self.db_controller.search_exact_match(search_term)
        for result in results:
            print(
                f"Путь к изображению: {result[0]}, OCR результат: {result[1]}, Время: {result[2]}")

    def run(self):
        self.view.show()
        self.ocr_controller.start_screenshot_loop()

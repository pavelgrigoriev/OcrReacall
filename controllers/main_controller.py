from views.main_view import MainView
from controllers.db_controller import DbController
from controllers.ocr_controller import OcrController


class MainController():
    def __init__(self, config_manager):
        self.db_controller = DbController(config_manager)
        self.ocr_controller = OcrController(config_manager, self.db_controller)
        self.view = MainView()
        self.view.search_timer.timeout.connect(self.search_ocr_results)

    def search_ocr_results(self):
        search_term = self.view.lineEdit.text()
        if not search_term.strip():
            return
        results = self.db_controller.search_like(search_term)
        self.view.display_images(results)

    def run(self):
        self.view.show()
        self.ocr_controller.start_screenshot_loop()

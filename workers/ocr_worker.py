from PyQt6.QtCore import QThread
import time
import logging
from logger import setup_logging

setup_logging()


class OcrWorker(QThread):
    def __init__(self, ocr_model, db_controller):
        super().__init__()
        self.ocr_model = ocr_model
        self.db_controller = db_controller
        self.last_screenshot = None

    def run(self):
        try:
            self.last_screenshot = self.ocr_model.take_screenshot()
            while True:
                time.sleep(5)
                current_screenshot = self.ocr_model.take_screenshot()
                if self.ocr_model.images_are_different(self.last_screenshot, current_screenshot):
                    current_screenshot_path = self.ocr_model.save_screenshot(
                        current_screenshot)
                    self.last_screenshot = current_screenshot
                    result = self.ocr_model.process_image(
                        current_screenshot_path)
                    self.db_controller.save_to_db(
                        current_screenshot_path, str(result))
                    logging.info(
                        "Processed and saved new screenshot: %s", current_screenshot_path)
        except Exception as e:
            logging.exception("An error occurred in OCR worker: %s", e)

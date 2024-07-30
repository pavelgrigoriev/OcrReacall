from PyQt6.QtCore import QThread
import time
from multiprocessing import Queue, Process, set_start_method

set_start_method('spawn', force=True)


class OcrWorker(QThread):
    def __init__(self, ocr_model, db_controller):
        super().__init__()
        self.ocr_model = ocr_model
        self.db_controller = db_controller
        self.last_screenshot = None

    def run(self):
        self.last_screenshot = self.ocr_model.take_screenshot()
        while True:
            time.sleep(5)
            current_screenshot = self.ocr_model.take_screenshot()
            if self.ocr_model.images_are_different(self.last_screenshot, current_screenshot):
                current_screenshot_path = self.ocr_model.save_screenshot(
                    current_screenshot)
                self.last_screenshot = current_screenshot
                result_queue = Queue()
                process = Process(target=self.ocr_model.process_image, args=(
                    current_screenshot_path, result_queue))
                process.start()
                process.join()
                result = result_queue.get()
                self.db_controller.save_to_db(
                    current_screenshot_path, str(result))
                print(f"Processed screenshot: {current_screenshot_path}")

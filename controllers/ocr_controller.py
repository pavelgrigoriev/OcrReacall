from models.ocr_model import OcrModel
from workers.ocr_worker import OcrWorker


class OcrController:
    def __init__(self, settings_manager, db_controller):
        self.ocr_model = OcrModel(settings_manager.get_app_dir())
        self.db_controller = db_controller

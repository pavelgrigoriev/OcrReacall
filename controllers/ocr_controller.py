from models.ocr_model import OcrModel


class OcrController:
    def __init__(self, db_controller):
        self.ocr_model = OcrModel
        self.db_controller = db_controller

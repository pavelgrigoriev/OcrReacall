from models.db_model import DbModel


class DbController:
    def __init__(self):
        self.db_model = DbModel()

    def save_to_db(self, image_path, ocr_result):
        self.db_model.save_to_db(image_path, ocr_result)

    def search_exact_match(self, terms):
        self.db_model.search_exact_match(terms)

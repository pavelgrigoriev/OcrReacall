from models.db_model import DbModel


class DbController:
    def __init__(self, settings_manager):
        self.db_model = DbModel(settings_manager.get_app_dir())

    def save_to_db(self, image_path, ocr_result):
        self.db_model.save_to_db(image_path, ocr_result)

    def search_like(self, terms):
        results = self.db_model.search_like(terms)
        return results

import logging
import sqlite3
from logger import setup_logging

setup_logging()


class DbModel():
    def __init__(self, db_path):
        self.db_path = db_path + "/ocr_results.db"
        self.init_db()

    def init_db(self):
        """Создаем FTS5 таблицу для хранения результатов с полнотекстовым поиском."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS ocr_results_fts
                USING fts5(
                    image_path,
                    ocr_result,
                    timestamp UNINDEXED
                )
                ''')
                conn.commit()
                logging.info("Initialized database at %s", self.db_path)
        except Exception as e:
            logging.exception("Failed to initialize database: %s", e)
            raise

    def save_to_db(self, image_path, ocr_result):
        """Сохраняем результаты инференса в FTS5 таблицу."""
        try:
            ocr_result = ocr_result.lower()  # Преобразуем текст в нижний регистр
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO ocr_results_fts (image_path, ocr_result, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (image_path, ocr_result))
                conn.commit()
                logging.info("Saved OCR result for %s to database", image_path)
        except Exception as e:
            logging.exception("Failed to save OCR result to database: %s", e)

    def search_exact_match(self, terms):
        """Поиск по точному совпадению."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = ' AND '.join(['ocr_result LIKE ?' for _ in terms])
                like_terms = [f"%{term}%" for term in terms]

                cursor.execute(f'''
                    SELECT image_path, ocr_result, timestamp
                    FROM ocr_results_fts
                    WHERE {query}
                ''', like_terms)

                results = cursor.fetchall()
                logging.info("Search results for terms %s:",
                             terms)

                for result in results:
                    # Логируем путь к изображению и первые 10 символов результата
                    logging.info("Search result - Image Path: %s, OCR Result (first 10 chars): %s",
                                 result[0], result[1][:10])

                return results

        except Exception as e:
            logging.exception("Failed to search database: %s", e)
            return []

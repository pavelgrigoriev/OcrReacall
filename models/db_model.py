import logging
import sqlite3
from logger import setup_logging
import pytz

setup_logging()


class DbModel():
    def __init__(self, db_path):
        self.db_path = db_path + "/ocr_results.db"
        self.init_db()

    def init_db(self):
        """Создаем таблицу для хранения результатов."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS ocr_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT,
                    ocr_result TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                conn.commit()
                logging.info("Initialized database at %s", self.db_path)
        except Exception as e:
            logging.exception("Failed to initialize database: %s", e)
            raise

    def save_to_db(self, image_path, ocr_result):
        """Сохраняем результаты инференса в таблицу."""
        try:
            ocr_result = ocr_result.lower()  # Преобразуем текст в нижний регистр
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO ocr_results (image_path, ocr_result, timestamp)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (image_path, ocr_result))
                conn.commit()
                logging.info("Saved OCR result for %s to database", image_path)
        except Exception as e:
            logging.exception("Failed to save OCR result to database: %s", e)

    def convert_utc_to_local(self, utc_dt):
        """Преобразуем UTC время в локальное время."""
        local_tz = pytz.timezone('Europe/Moscow')
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

    def search_like(self, terms):
        terms = terms.rstrip()
        if not terms.strip():  # Проверяем, является ли строка пустой или содержит только пробелы
            return []

        """Поиск в базе данных."""
        terms = f'%{terms.lower()}%'
        results = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT image_path, ocr_result, timestamp
                    FROM ocr_results
                    WHERE ocr_result LIKE ?
                ''', (terms,))
                results = cursor.fetchall()
                logging.info("Search results for terms %s:", terms)
            return results
        except Exception as e:
            logging.exception("Failed to search database: %s", e)
            return []

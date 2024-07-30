import os
import sqlite3


class DbModel():
    def __init__(self, db_path):
        self.db_path = db_path + "/ocr_results.db"
        self.init_db()

    def init_db(self):
        """Создаем FTS5 таблицу для хранения результатов с полнотекстовым поиском."""
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

    def save_to_db(self, image_path, ocr_result):
        """Сохраняем результаты инференса в FTS5 таблицу."""
        ocr_result = ocr_result.lower()  # Преобразуем текст в нижний регистр
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ocr_results_fts (image_path, ocr_result, timestamp)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (image_path, ocr_result))
            conn.commit()

    def search_exact_match(self, terms):
        """Поиск по точному совпадению."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Создаем запрос для поиска точных совпадений
            query = ' AND '.join(['ocr_result LIKE ?' for _ in terms])
            like_terms = [f"%{term}%" for term in terms]

            cursor.execute(f'''
                SELECT image_path, ocr_result, timestamp
                FROM ocr_results_fts
                WHERE {query}
            ''', like_terms)

            results = cursor.fetchall()

            return results

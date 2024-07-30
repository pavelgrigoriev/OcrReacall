import logging
import sys
from datetime import datetime
from config.config_manager import ConfigManager


def setup_logging():
    # Получаем текущую дату и время
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Формируем имя файла с временной меткой
    log_filename = f"{ConfigManager().get_app_dir()}/app_{timestamp}.log"

    # Проверяем, есть ли уже обработчики
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s:%(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )

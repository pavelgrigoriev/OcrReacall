import logging
import os
import sys
from datetime import datetime
from config.config_manager import ConfigManager


def setup_logging():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.makedirs(ConfigManager().get_app_dir() + "/logs", exist_ok=True)
    log_filename = f"{ConfigManager().get_app_dir()
                      }/logs/app_{timestamp}.log"

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

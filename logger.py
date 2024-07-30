import logging
import sys

from config.config_manager import ConfigManager


def setup_logging():
    config_manager = ConfigManager()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(config_manager.get_app_dir() + "/app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

import logging
import sys
from PyQt6 import QtWidgets
from controllers.main_controller import MainController
from config.config_manager import ConfigManager
from logger import setup_logging


def main():
    config_manager = ConfigManager()
    setup_logging()
    logging.info("Starting application")
    app = QtWidgets.QApplication(sys.argv)

    try:
        controller = MainController(config_manager)
        controller.run()
    except Exception as e:
        logging.exception("An error occurred: %s", e)
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

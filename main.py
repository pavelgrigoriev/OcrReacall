import sys
from PyQt6 import QtWidgets
from controllers.main_controller import MainController
from config.config_manager import ConfigManager


def main():
    config_manager = ConfigManager()
    app = QtWidgets.QApplication(sys.argv)
    controller = MainController(config_manager)
    controller.run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

from PyQt6 import QtWidgets, uic


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        uic.loadUi('views/ui/mainwindow.ui', self)

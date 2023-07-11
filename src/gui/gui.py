from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow


class MainGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainGui, self).__init__(*args, **kwargs)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainGui()
    window.show()
    app.exec_()

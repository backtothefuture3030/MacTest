import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

ui = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/app.ui')[0]

class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        

    def run(self):
        keyword = self.lineEdit.text()
        print(keyword)

if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
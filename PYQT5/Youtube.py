
'''
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from YoutubeCrawling import *

form_class = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/Youtubeb.ui')[0]

class MainWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)
    def btn_clicked(self):
        self.textEdit.append("pacece")

    def run(self):
        self.YoutubeCrawling.run()

    def set_table(self, data):
        if data:
            row_idx = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_idx)

            col_idx = self.table_cols.index('Title')
            table_item = QtWidgets.QTableWidgetItem(data['title'])
            self.tableWidget.setItem(row_idx, col_idx, table_item)

            col_idx = self.table_cols.index('URL')
            table_item = QtWidgets.QTableWidgetItem(data['href'])
            self.tableWidget.setItem(row_idx, col_idx, table_item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec
'''
            


import sys 
from PyQt5.QtWidgets import * 
from PyQt5 import uic 

form_class = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/Youtubeb.ui')[0]


class MyWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.brightwing.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        self.textEdit.append("Hello World!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
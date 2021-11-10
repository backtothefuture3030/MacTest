import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from WeatherCrawling import *


ui = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/app.ui')[0]

class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.WeatherCrawling = GoogleWeather()
        self.table_cols = ['지역명', '시간', '상태']
        

    def run(self):
        keyword = self.lineEdit.text()
        self.WeatherCrawling.set_keyword(keyword + ' 날씨')
        self.WeatherCrawling.run()
        r = self.WeatherCrawling.get_result()
        self.set_table(r)
    
    def set_table(self, data):
        if data:
            row_idx = self.tableWidget.rowCount()   
            self.tableWidget.insertRow(row_idx)     # 일단 빈칸 (행) 추가
            col_idx = self.table_cols.index('지역명')      # 그칸에 추가
            table_item = QtWidgets.QTableWidgetItem(data['loc'])
            self.tableWidget.setItem(row_idx, col_idx, table_item)

            col_idx = self.table_cols.index('시간')
            table_item = QtWidgets.QTableWidgetItem(data['time'])
            self.tableWidget.setItem(row_idx, col_idx, table_item)

            col_idx = self.table_cols.index('상태')
            table_item = QtWidgets.QTableWidgetItem(data['status'])
            self.tableWidget.setItem(row_idx, col_idx, table_item)

if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()

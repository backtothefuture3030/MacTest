import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow

from YoutubeCrawling import *

ui = uic.loadUiType('/Users/sup/Desktop/Mycode/PYQT5/Youtubeb.ui')

class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
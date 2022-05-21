from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5 import QtCore

class AboutYASART(QDialog):
    def __init__(self):
        super(AboutYASART, self).__init__()
        loadUi("AboutYASART.ui", self)

class AboutPEAE(QDialog):
    def __init__(self):
        super(AboutPEAE, self).__init__()
        loadUi("AboutPEAE.ui", self)
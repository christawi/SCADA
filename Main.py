### By Christian Kibrework ;)
import sys
import sqlite3
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap
from mainWindow import Main

### Login screen on startup 
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui", self)
        self.show()
        self.LoginButton.clicked.connect(self.checkAut)
### authentication of password and username
    def checkAut(self):
        self.userName=self.UserName.text()
        self.password=self.Password.text()
        if ((self.userName=='adm') & (self.password =='adm')):
            self.userMode = 'admin'
            self.main = Main()
            self.main.show()
            self.close()
        else:
            self.userMode = 'none'
            self.LoggedInLabel.setText('Please Enter Correct Username or Password!')
            self.LoggedInLabel.setStyleSheet("color:rgb(255, 0, 0);background-color: rgba(0, 0, 0, 0);")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
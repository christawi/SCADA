import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5 import QtCore
from pymodbus.client.sync import ModbusSerialClient
import os, threading, time
from connection import Connection
from dialog import AboutYASART, AboutPEAE
### main window 
class Main(QMainWindow):
    conStatus = False
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)
### Initialization
        self.headerLabel.setText('ACTIVITY')
    
### navigation for stacked widget
        self.menuButton.clicked.connect(self.slider)
        self.activityButton.clicked.connect(lambda:(self.stackedWidget.setCurrentWidget(self.activityPage),self.headerLabel.setText('ACTIVITY')))
        self.meterButton.clicked.connect(lambda:(self.stackedWidget.setCurrentWidget(self.meterPage),self.headerLabel.setText('METER')))
        self.controlButton.clicked.connect(lambda:(self.stackedWidget.setCurrentWidget(self.controlPage),self.headerLabel.setText('CONTROL')))
        self.warningButton.clicked.connect(lambda:(self.stackedWidget.setCurrentWidget(self.warningPage),self.headerLabel.setText('WARNING')))
        self.authButton.clicked.connect(lambda:(self.stackedWidget.setCurrentWidget(self.authPage),self.headerLabel.setText('AUTH')))
        self.aboutYASARTButton.clicked.connect(self.callAboutYASART)
        self.aboutPEAEButton.clicked.connect(self.callAboutPEAE)
        self.modbusConnect.clicked.connect(self.connectOrDisconnect)
        self.dial1 = self.dial.value()
        self.connection = Connection()

### Connection button control function
    def connectOrDisconnect(self):
        if (self.conStatus == True):
            self.disconnect()
        else:
            self.connect()

### Call about* dialog page
        
    def callAboutYASART(self):
        self.main = AboutYASART()
        self.main.show()
        
    def callAboutPEAE(self):
        self.main = AboutPEAE()
        self.main.show()

### slider for menu
    def slider(self):
        width = self.slideMenu.width()
        if width == 10:
            newWidth = 200
        else:
            newWidth = 10
        self.animation = QtCore.QPropertyAnimation(self.slideMenu, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

#######################################################################################################
#######################################################################################################
### modbus comunication functions
    
    def connect(self):
        self.connectStatus.setStyleSheet("color:rgb(120, 255, 50);background-color: rgba(0, 0, 0, 0);")
        self.connectStatus.setText('Connecting through COM1')
        self.connection.start()
        time.sleep(0.1)
        if self.connection.connection_live() and self.connection.is_com_connected():
            self.modbusConnect.setText('Disconnect')
            self.connectStatus.setText('Connected')
            self.connectStatus.setStyleSheet("color:rgb(0, 255, 0);background-color: rgba(0, 0, 0, 0);")
            self.conStatus = True
        else:
            self.connectStatus.setText('Failed to connect')
            return
        self.valueUpdateThread = threading.Thread(name="valueUpdateThread",target=self.valueUpdate)
        self.valueUpdateThread.start()
        self.statusUpdateThread = threading.Thread(name="statusUpdateThread",target=self.statusUpdate)
        self.statusUpdateThread.start()
        self.senderThread = threading.Thread(name="senderThread",target=self.sender)
        self.senderThread.start()
        self.updateScreenThread = threading.Thread(name="updateScreenThread",target=self.updateScreen)
        self.updateScreenThread.start()

    def disconnect(self):
        self.connection.disconnect()
        del self.connection
        self.connection = Connection()
        self.conStatus = False

        self.modbusConnect.setText('Connect')
        self.connectStatus.setText('Disconnected')
        self.connectStatus.setStyleSheet("color:rgb(0, 255, 0);background-color: rgba(0, 0, 0, 0);")

        self.valueUpdateThread.join()
        self.statusUpdateThread.join()
        self.senderThread.join()
        self.updateScreenThread.join()


    def durring_exit():
        self.connection.disconnect()

#######################################################################################################
    def valueUpdate(self):
        update_label = False
        while (self.conStatus == True):
            self.modbusData = self.connection.data()
            
            if self.modbusData == None:
                self.connectStatus.setText("Modbus Connection Error")
                self.connectStatus.setStyleSheet("color:rgb(255, 0, 0);background-color: rgba(0, 0, 0, 0);")
                update_label = True
            else:
                print(self.modbusData.registers)
                if update_label:
                    self.connectStatus.setText('Connected')
                    self.connectStatus.setStyleSheet("color:rgb(0, 255, 0);background-color: rgba(0, 0, 0, 0);")
                    update_label = False

                self.sPump1status= self.modbusData.registers[0]
                self.sPump2status= self.modbusData.registers[1]
                self.sPump3status= self.modbusData.registers[2]
                self.sPump4status= self.modbusData.registers[3]
                self.sPump5status= self.modbusData.registers[4]
                self.sPump6status= self.modbusData.registers[5]                
                self.sPump7status= self.modbusData.registers[6]                                
                self.sPump8status= self.modbusData.registers[7]
                self.hPump1status= self.modbusData.registers[8]
                self.hPump2status= self.modbusData.registers[9]
                self.hPump3status= self.modbusData.registers[10]
                self.hPump4status= self.modbusData.registers[11]
                self.hPump5status= self.modbusData.registers[12]
                self.hPump6status= self.modbusData.registers[13]
                self.SPump1Flow= self.modbusData.registers[14]
                self.SPump1Pres= self.modbusData.registers[15]
                self.SPump2Flow= self.modbusData.registers[16]
                self.SPump2Pres= self.modbusData.registers[17]
            time.sleep(1)

### status change with the registry data
    def statusUpdate(self):
        while (self.conStatus == True):
            try:
                if (self.sPump1status == 0):
                    self.sPump1.setEnabled(False)
                else:
                    self.sPump1.setEnabled(True)
                if (self.sPump2status == 0):
                    self.sPump2.setEnabled(False)
                else:
                    self.sPump2.setEnabled(True)
                if (self.sPump3status == 0):
                    self.sPump3.setEnabled(False)
                else:
                    self.sPump3.setEnabled(True)
                if (self.sPump4status == 0):
                    self.sPump4.setEnabled(False)
                else:
                    self.sPump4.setEnabled(True)
                if (self.sPump5status == 0):
                    self.sPump5.setEnabled(False)
                else:
                    self.sPump5.setEnabled(True)
                if (self.sPump6status == 0):
                    self.sPump6.setEnabled(False)
                else:
                    self.sPump6.setEnabled(True)
                if (self.sPump7status == 0):
                    self.sPump7.setEnabled(False)
                else:
                    self.sPump7.setEnabled(True)
                if (self.sPump8status == 0):
                    self.sPump8.setEnabled(False)
                else:
                    self.sPump8.setEnabled(True)
                if (self.hPump1status == 0):
                    self.hPump1.setEnabled(False)
                else:
                    self.hPump1.setEnabled(True)
                if (self.hPump2status == 0):
                    self.hPump2.setEnabled(False)
                else:
                    self.hPump2.setEnabled(True)
                if (self.hPump3status == 0):
                    self.hPump3.setEnabled(False)
                else:
                    self.hPump3.setEnabled(True)
                if (self.hPump4status == 0):
                    self.hPump4.setEnabled(False)
                else:
                    self.hPump4.setEnabled(True)
                if (self.hPump5status == 0):
                    self.hPump5.setEnabled(False)
                else:
                    self.hPump5.setEnabled(True)
                if (self.hPump6status == 0):
                    self.hPump6.setEnabled(False)
                else:
                    self.hPump6.setEnabled(True)

            except:
                print("Coudn't update data")
            time.sleep(1)
    def sender(self):
        while (self.conStatus == True):
            try:
                self.connection.write_value(50, int(self.dial.value()), 1)
            except:
                print("couldn't send data")
            time.sleep(2)
################################################################## 
       
    def updateScreen(self):
### set pogress value of Spump 1
        while (self.conStatus == True):
            
            try:
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (120-self.SPump1Flow)/120.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump1Flow))
                self.progValue1.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.SPump1Pres))
                self.progValue2.setText(newPressureValue)
                time.sleep(.001)
### set pogress value of Spump 2
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (120-self.SPump2Flow)/120.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg2.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump2Flow))
                self.progValue3.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.SPump2Pres))
                self.progValueT.setText(newPressureValue)
                time.sleep(.002)
            except:
                print("Coudn't update screen")
            time.sleep(.5)
###################################################################################################

# progValueT
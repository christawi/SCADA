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
        time.sleep(1)
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

                self.sPump1status= self.modbusData.registers[4]
                self.sPump2status= self.modbusData.registers[5]
                self.sPump3status= self.modbusData.registers[6]
                self.sPump4status= self.modbusData.registers[7]
                self.hPump1status= self.modbusData.registers[15]
                self.hPump2status= self.modbusData.registers[16]
                self.hPump3status= self.modbusData.registers[17]
                self.hPump4status= self.modbusData.registers[18]
                self.SPump1Level= self.modbusData.registers[0]
                self.SPump2Level= self.modbusData.registers[1]
                self.SPump3Level= self.modbusData.registers[2]
                self.SPump4Level= self.modbusData.registers[3]
                self.SPump1Flow= self.modbusData.registers[11]
                self.SPump2Flow= self.modbusData.registers[12]
                self.SPump3Flow= self.modbusData.registers[13]
                self.SPump4Flow= self.modbusData.registers[14]
                self.SPump1Pres= self.modbusData.registers[19]
                self.SPump2Pres= self.modbusData.registers[20]
                self.SPump3Pres= self.modbusData.registers[21]
                self.SPump4Pres= self.modbusData.registers[22]
                self.SPump1Curr= self.modbusData.registers[27]
                self.SPump2Curr= self.modbusData.registers[28]
                self.SPump3Curr= self.modbusData.registers[29]
                self.SPump4Curr= self.modbusData.registers[30]
                self.SPump1Volt= self.modbusData.registers[35]
                self.SPump2Volt= self.modbusData.registers[36]
                self.SPump3Volt= self.modbusData.registers[37]
                self.SPump4Volt= self.modbusData.registers[38]
                self.SPump1Cond= self.modbusData.registers[43]
                self.SPump2Cond= self.modbusData.registers[44]
                self.SPump3Cond= self.modbusData.registers[45]
                self.SPump4Cond= self.modbusData.registers[46]
                self.HPump1Flow= self.modbusData.registers[51]
                self.HPump2Flow= self.modbusData.registers[52]
                self.HPump3Flow= self.modbusData.registers[53]
                self.HPump4Flow= self.modbusData.registers[54]
                self.HPump1Pres= self.modbusData.registers[57]
                self.HPump2Pres= self.modbusData.registers[58]
                self.HPump3Pres= self.modbusData.registers[59]
                self.HPump4Pres= self.modbusData.registers[60]
                self.HPump1Curr= self.modbusData.registers[63]
                self.HPump2Curr= self.modbusData.registers[64]
                self.HPump3Curr= self.modbusData.registers[65]
                self.HPump4Curr= self.modbusData.registers[66]
                self.HPump1Volt= self.modbusData.registers[69]
                self.HPump2Volt= self.modbusData.registers[70]
                self.HPump3Volt= self.modbusData.registers[71]
                self.HPump4Volt= self.modbusData.registers[72]
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
            except:
                print("Coudn't update data")
            time.sleep(1)

    def sender(self):
        while (self.conStatus == True):
            try:
                self.connection.write_value(602, int(self.dial.value()), 1)
                self.connection.write_value(603, int(self.dial2.value()), 1)
                self.connection.write_value(604, int(self.dial3.value()), 1)
                self.connection.write_value(605, int(self.dial4.value()), 1)
                self.connection.write_value(606, int(self.dial5.value()), 1)
                self.connection.write_value(607, int(self.dial6.value()), 1)
                self.connection.write_value(608, int(self.dial7.value()), 1)
                self.connection.write_value(609, int(self.dial8.value()), 1)
                self.connection.write_value(610, int(self.dial9.value()), 1)
                self.connection.write_value(611, int(self.dial10.value()), 1)
            except:
                print("couldn't send data")
            time.sleep(1)
############################################################################################################
       
    def updateScreen(self):
####### set pogress value of Spump 1
        while (self.conStatus == True):
            
            try:
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (400-self.SPump1Flow)/400.0
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
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Level: </span><span style=" font-size:11pt; font-weight:400;">{Value5}</span><span style=" font-size:11pt;">meters</span></p><p><span style=" font-size:11pt;">Conductivity: </span><span style=" font-size:11pt; font-weight:400;">{Value6}</span><span style=" font-size:11pt;">µS/cm</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump1Volt)).replace("{Value1}", str(self.SPump1Volt)).replace("{Value2}", str(self.SPump1Volt)).replace("{Value3}", str(self.SPump1Curr)).replace("{Value4}", str(self.SPump1Flow)).replace("{Value5}", str(self.SPump1Level)).replace("{Value6}", str(self.SPump1Cond)).replace("{Value7}", str(self.SPump1Pres))
                self.progressTable_1.setText(newFlowValue)
                time.sleep(.01)
############### set pogress value of Spump 2
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (400-self.SPump2Flow)/400.0
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
                self.progValue4.setText(newPressureValue)
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Level: </span><span style=" font-size:11pt; font-weight:400;">{Value5}</span><span style=" font-size:11pt;">meters</span></p><p><span style=" font-size:11pt;">Conductivity: </span><span style=" font-size:11pt; font-weight:400;">{Value6}</span><span style=" font-size:11pt;">µS/cm</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump2Volt)).replace("{Value1}", str(self.SPump2Volt)).replace("{Value2}", str(self.SPump2Volt)).replace("{Value3}", str(self.SPump2Curr)).replace("{Value4}", str(self.SPump2Flow)).replace("{Value5}", str(self.SPump2Level)).replace("{Value6}", str(self.SPump2Cond)).replace("{Value7}", str(self.SPump2Pres))
                self.progressTable_2.setText(newFlowValue)
                time.sleep(.02)
############### set pogress value of Spump 3
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (400-self.SPump3Flow)/400.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg3.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump3Flow))
                self.progValue5.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.SPump3Pres))
                self.progValue6.setText(newPressureValue)
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Level: </span><span style=" font-size:11pt; font-weight:400;">{Value5}</span><span style=" font-size:11pt;">meters</span></p><p><span style=" font-size:11pt;">Conductivity: </span><span style=" font-size:11pt; font-weight:400;">{Value6}</span><span style=" font-size:11pt;">µS/cm</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump3Volt)).replace("{Value1}", str(self.SPump3Volt)).replace("{Value2}", str(self.SPump3Volt)).replace("{Value3}", str(self.SPump3Curr)).replace("{Value4}", str(self.SPump3Flow)).replace("{Value5}", str(self.SPump3Level)).replace("{Value6}", str(self.SPump3Cond)).replace("{Value7}", str(self.SPump3Pres))
                self.progressTable_3.setText(newFlowValue)
                time.sleep(.03)
############################################
############### set pogress value of Hpump 1
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (500-self.SPump1Flow)/500.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg4.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump1Flow))
                self.progValue7.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.HPump1Pres))
                self.progValue8.setText(newPressureValue)
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump1Volt)).replace("{Value1}", str(self.HPump1Volt)).replace("{Value2}", str(self.HPump1Volt)).replace("{Value3}", str(self.HPump1Curr)).replace("{Value4}", str(self.HPump1Flow)).replace("{Value7}", str(self.HPump1Pres))
                self.progressTable_4.setText(newFlowValue)
                time.sleep(.04)
############### set pogress value of Hpump 2
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (500-self.SPump2Flow)/500.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg5.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump2Flow))
                self.progValue9.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.HPump2Pres))
                self.progValue10.setText(newPressureValue)
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump1Volt)).replace("{Value1}", str(self.HPump1Volt)).replace("{Value2}", str(self.HPump1Volt)).replace("{Value3}", str(self.HPump1Curr)).replace("{Value4}", str(self.HPump1Flow)).replace("{Value7}", str(self.HPump1Pres))
                self.progressTable_5.setText(newFlowValue)
                time.sleep(.05)
############### set pogress value of Hpump 3
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
                progress = (500-self.SPump3Flow)/500.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg3.setStyleSheet(newStlesheet)
### set flow
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump3Flow))
                self.progValue11.setText(newFlowValue)
### set pressure
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.HPump3Pres))
                self.progValue12.setText(newPressureValue)
### set all
                flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">{Value}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">{Value1}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">{Value2}</span><span style=" font-size:11pt;">V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">{Value3}</span><span style=" font-size:11pt;">A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">{Value4}</span><span style=" font-size:11pt;">m</span><span style=" font-size:11pt; vertical-align:super;">3</span><span style=" font-size:11pt;">/hr</span></p><p><span style=" font-size:11pt;">Head: </span><span style=" font-size:11pt; font-weight:400;">{Value7}</span><span style=" font-size:11pt;">Kpa</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.HPump1Volt)).replace("{Value1}", str(self.HPump1Volt)).replace("{Value2}", str(self.HPump1Volt)).replace("{Value3}", str(self.HPump1Curr)).replace("{Value4}", str(self.HPump1Flow)).replace("{Value7}", str(self.HPump1Pres))
                self.progressTable_6.setText(newFlowValue)
                time.sleep(.06)
            except:
                print("Coudn't update screen")
            time.sleep(.5)
###################################################################################################



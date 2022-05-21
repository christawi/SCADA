#from __future__ import print_function
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
        self.SPump1Value(40, 100)
        self.SPump2Value(30, 90)
        self.SPump3Value(0, 0)
        self.VPump1Value(75, 95)
        self.VPump2Value(0, 0)
        self.VPump3Value(0, 0)
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

#########################################################################################################
### circular indicators status SPump1
    def SPump1Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2.setText(newPressureValue)
### set circular pogress bar value
        progress = (40-flow)/40.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg.setStyleSheet(newStlesheet)

### circular indicators status SPump2
    def SPump2Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1_2.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2_2.setText(newPressureValue)
### set circular pogress bar value
        progress = (40-flow)/40.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg_2.setStyleSheet(newStlesheet)

### circular indicators status SPump3
    def SPump3Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1_3.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2_3.setText(newPressureValue)
### set circular pogress bar value
        progress = (40-flow)/40.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg_3.setStyleSheet(newStlesheet)

### circular indicators status VPump1
    def VPump1Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1_4.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2_4.setText(newPressureValue)
### set circular pogress bar value
        progress = (80-flow)/80.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg_4.setStyleSheet(newStlesheet)

### circular indicators status VPump2
    def VPump2Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1_5.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2_5.setText(newPressureValue)
### set circular pogress bar value
        progress = (60-flow)/60.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg_5.setStyleSheet(newStlesheet)        

### circular indicators status VPump3
    def VPump3Value(self, flow, pressure):
        styleSheet = """
            QFrame{
                border-radius: 100px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
            }
        """
### set flow meter value
        flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
        newFlowValue = flowValue.replace("{Value}", str(flow))
        self.progValue1_6.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue2_6.setText(newPressureValue)
### set circular pogress bar value
        progress = (60-flow)/60.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg_6.setStyleSheet(newStlesheet)
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
                self.vPump1status= self.modbusData.registers[3]
                self.vPump2status= self.modbusData.registers[4]
                self.vPump3status= self.modbusData.registers[5]
                self.a= self.modbusData.registers[6]
                self.b= self.modbusData.registers[7]
                self.c= self.modbusData.registers[8]
                self.d= self.modbusData.registers[9]
            time.sleep(1)

### status change with the registry data
    def statusUpdate(self):
        while (self.conStatus == True):
            try:
                if (self.sPump1status == 1):
                    self.sPump1.setEnabled(True)
                else:
                    self.sPump1.setEnabled(False)
                if (self.sPump2status == 1):
                    self.sPump2.setEnabled(True)
                else:
                    self.sPump2.setEnabled(False)
                if (self.sPump3status == 1):
                    self.sPump3.setEnabled(True)
                else:
                    self.sPump3.setEnabled(False)
                if (self.vPump1status == 1):
                    self.vPump1.setEnabled(True)
                else:
                    self.vPump1.setEnabled(False)
                if (self.vPump2status == 1):
                    self.vPump2.setEnabled(True)
                else:
                    self.vPump2.setEnabled(False)  
                if (self.vPump3status == 1):
                    self.vPump3.setEnabled(True)
                else:
                    self.vPump3.setEnabled(False)  
            except:
                print("Coudn't update data")
            time.sleep(1)

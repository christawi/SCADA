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

#########################################################################################################
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
        self.progValue5.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue6.setText(newPressureValue)
### set circular pogress bar value
        progress = (40-flow)/40.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg3.setStyleSheet(newStlesheet)

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
        self.progValue7.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue8.setText(newPressureValue)
### set circular pogress bar value
        progress = (80-flow)/80.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg4.setStyleSheet(newStlesheet)

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
        self.progValue9.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue10.setText(newPressureValue)
### set circular pogress bar value
        progress = (60-flow)/60.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg5.setStyleSheet(newStlesheet)        

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
        self.progValue11.setText(newFlowValue)
### set pressure meter value
        flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
        newPressureValue = flowValue.replace("{Value}", str(pressure))
        self.progValue12.setText(newPressureValue)
### set circular pogress bar value
        progress = (60-flow)/60.0
        Stop1 = str(progress - .001)
        Stop2 = str(progress)
        newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
        self.cirProg6.setStyleSheet(newStlesheet)
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
        self.SPump1ValueThread = threading.Thread(name="SPump1ValueThread",target=self.SPump1Value)
        self.SPump1ValueThread.start()

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
        self.SPump1ValueThread.join()


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
                self.client.write_registers(address= 39, values= 11, unit= 1)
            except:
                print(self.dial.value())
            time.sleep(1)
    ##################################################################        
    def SPump1Value(self):
        # self.SPump1Flow = 10
        # self.SPump1Pres = 10
        while (self.conStatus == True):
            try:
                styleSheet = """
                QFrame{
                    border-radius: 100px;
                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{stop1} rgba(0, 0, 8, 0), stop:{stop2} rgba(129, 0, 0, 255));
                }
                """
### set flow meter1 value 
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump1Flow))
                self.progValue1.setText(newFlowValue)
### set pressure meter1 value
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.SPump1Pres))
                self.progValue2.setText(newPressureValue)
### set pressure chart1 value
                # flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">10A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">100m</span><span style=" font-size:11pt; font-weight:400; vertical-align:super;">3</span><span style=" font-size:11pt; font-weight:400;">/hr</span></p><p><span style=" font-size:11pt;">Level: </span><span style=" font-size:11pt; font-weight:400;">50meters</span></p><p><span style=" font-size:11pt;">Conductivity: </span><span style=" font-size:11pt; font-weight:400;">200µS/cm</span></p><p><span style=" font-size:11pt;">Pressure: </span><span style=" font-size:11pt; font-weight:400;">100Kpa</span></p>"""
                # newPressureValue = flowValue.replace("{Value}", str(self.SPump1Pres))
                # self.progValue2.setText(newPressureValue)
### set circular pogress bar1 value
                progress = (40-self.SPump1Flow)/40.0
                Stop1 = str(progress - .001)
                Stop2 = str(progress)
                newStlesheet = styleSheet.replace("{stop1}", Stop1).replace("{stop2}", Stop2)
                self.cirProg.setStyleSheet(newStlesheet)
### set flow meter2 value 
                flowValue = """<p><span style=" color:#430000;">{Value}</span><span style=" color:#430000; vertical-align:super;">L/s</span></p>"""
                newFlowValue = flowValue.replace("{Value}", str(self.SPump2Flow))
                self.progValue3.setText(newFlowValue)
### set pressure meter1 value
                flowValue = """<p><span style=" font-size:24pt; color:#430000;">{Value}</span><span style=" font-size:20pt; color:#430000;">Kpa</span></p>"""
                newPressureValue = flowValue.replace("{Value}", str(self.SPump2Pres))
                self.progValue4.setText(newPressureValue)
            except:
                print("Coudn't update data")
            time.sleep(1)
########################


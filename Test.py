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

# ## set pressure chart1 value
#                 flowValue = """<p><span style=" font-size:11pt;">Voltage</span></p><p><span style=" font-size:11pt;">A-B: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">B-C: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">C-D: </span><span style=" font-size:11pt; font-weight:400;">120V</span></p><p><span style=" font-size:11pt;">Current: </span><span style=" font-size:11pt; font-weight:400;">10A</span></p><p><span style=" font-size:11pt;">Flow: </span><span style=" font-size:11pt; font-weight:400;">100m</span><span style=" font-size:11pt; font-weight:400; vertical-align:super;">3</span><span style=" font-size:11pt; font-weight:400;">/hr</span></p><p><span style=" font-size:11pt;">Level: </span><span style=" font-size:11pt; font-weight:400;">50meters</span></p><p><span style=" font-size:11pt;">Conductivity: </span><span style=" font-size:11pt; font-weight:400;">200µS/cm</span></p><p><span style=" font-size:11pt;">Pressure: </span><span style=" font-size:11pt; font-weight:400;">100Kpa</span></p>"""
#                 newPressureValue = flowValue.replace("{Value}", str(self.SPump1Pres))
#                 self.progValue2.setText(newPressureValue)
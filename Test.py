from pymodbus.client.sync import ModbusSerialClient

class MBConnect:
    def __init__(self):
        super(MBConnect, self).__init__()
        self.modbusConnect
        self.readWiteModbus
        
    def modbusConnect(self):
        self.client=ModbusSerialClient(method='rtu',port='COM8',stopbits=1,bytesize=8,parity='N',baudrate=19200)
        self.client.connect()
        print("connected!")

    def readWiteModbus(self):
        self.client.read_coils(address)


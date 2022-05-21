from pymodbus.client.sync import ModbusSerialClient
from threading import Thread, Event

class Connection:
    def __init__(self):
        self.modbusData = None
        self.client=ModbusSerialClient(method='rtu',port='COM1',stopbits=1,bytesize=8,parity='N',baudrate=9600)
        self.connection = Connection_thread(self.client)
        self.com_connected = False

    def start(self):
        if self.client.connect():
            self.connection.start()
            print('connected')
            self.com_connected = True
        
    def disconnect(self):
        self.connection.stop()
        try:
            self.client.close()
        except:
            pass
        print('connection closed')

    def data(self):
        return self.connection.update()

    def is_com_connected(self):
        return self.com_connected

    def connection_live(self):
        return self.connection.is_alive()

    def write_value(self, address, value, unit):
        self.connection.send_data(address, value, unit)
        
class Connection_thread(Thread):
    def __init__(self, client):
        self.modbus_data_value = None
        self.client = client
        Thread.__init__(self)
        self.event= Event()

    def run(self):      
        while (not self.event.is_set()):
            try:
                self.modbusData=self.client.read_holding_registers(address=512,count=10,unit=1)
                self.modbus_data_value = self.modbusData
            except:
                self.modbus_data_value = None 
    def stop(self):
        self.event.set()

    def update(self):
        return self.modbus_data_value
    
    def send_data(self, address, value, unit):
        self.client.write_register(address=address,value=value,unit=unit)
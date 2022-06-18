from pymodbus.client.sync import ModbusSerialClient
from threading import Thread, Event


class Connection:
    def __init__(self):
        self.modbusData = None
        # self.client=ModbusSerialClient(method='rtu',port='COM8',stopbits=1,bytesize=8,parity='N',baudrate=19200)
        self.client=ModbusSerialClient(method='rtu',port='COM1',stopbits=1,bytesize=8,parity='N',baudrate=19200)
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
        self.connection.send_data(self, 41, 10, 1)
        
class Connection_thread(Thread):
    def __init__(self, client):
        self.modbus_data_value = None
        self.client = client
        Thread.__init__(self)
        self.event= Event()
        

    def run(self):      
        while (not self.event.is_set()):
            try:
                self.modbusData=self.client.read_holding_registers(address=0,count=40,unit=1)
                self.modbus_data_value = self.modbusData
                # self.client.write_registers(address= 39, values= int(self.sendVal), unit= 1)
                # self.client.write_registers(address= 39, values=int(self.dial.value()), unit= 1)
                #self.client.write_coil(address=1538,value=1,unit=1)
            except:
                self.modbus_data_value = None 
    def stop(self):
        self.event.set()

    def update(self):
        return self.modbus_data_value
    
    def send_data(self, address, value, unit):
        self.client.write_coil(address=address,value=value,unit=unit)
        self.client.write_register(address=41,value=10,unit=1)
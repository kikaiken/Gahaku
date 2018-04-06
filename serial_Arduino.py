import serial
import json
import time

class serial_Arduino():
    
    def __init__(self,device):
        self.ser = serial.Serial(device,9600,timeout=1)
    def send(self,data):
        json_data = json.dumps(data)+";"
        print(json_data)
        json_bytes=bytes(json_data,'utf-8')
        self.ser.write(bytes("TESTTEST","utf-8"))
        raw_recv = str(self.ser.read(4).decode())
        print(raw_recv)
        #recv = json.loads(raw_recv)
        #time.sleep(0.005)
        #while(recv["status"] != "OK"):
        #    time.sleep(0.005)
        #    self.ser.write(json_data)
        #    recv = json.loads(str(self.ser.readline().decode()))    
        #return recv

from tkinter import *
import signal
import time
import threading
import serial
import json
class connectionThread(threading.Thread):

    def __init__(self):
        super(connectionThread, self).__init__()
        self.setDaemon(True)

    def run(self):
        while True:
            print("Servo1:"+str(Servo1.get()))
            print("Servo2:"+str(Servo2.get()))
            print("Servo3:"+str(Servo3.get()))
            print("Servo4:"+str(Servo4.get()))
            list = {'Servo1':-Servo1.get()+210,'Servo2':-Servo2.get()+220,'Servo3':Servo3.get()+27.9,'Servo4':Servo4.get()}
            json_data = json.dumps(list)+";"
            print(json_data)
            json_byte=bytes(json_data,'utf-8')
            ser.write(json_byte)
            res = str(ser.read(2).decode())
#            res = json.loads(res)
            print(res)
            while(res[0:2] != "OK"):
                time.sleep(0.005)
                ser.write(json_byte)
                res = str(ser.read(2).decode())[0:2]
 #               res = json.loads(res)
#                print(res["status"])
#            value = int(res["battery"])
#            voltage = round(value*5/1024*2,3)
#            Battery.set("Battery:"+str(voltage)+"V")
#            print (str(voltage)+"V")
            time.sleep(0.005)
ser = serial.Serial('/dev/ttyACM0',76800,timeout=1)
root = Tk()
root.title("GAHAKU")
Battery = StringVar()
Battery.set("NULL")
Servo1 = DoubleVar()
Servo2 = DoubleVar()
Servo3 = DoubleVar()
Servo4 = DoubleVar()
label_bt = Label(root,textvariable=Battery)
label_s1 = Label(root,text="Servo1")
label_s2 = Label(root,text="Servo2")
label_s3 = Label(root,text="Servo3")
label_s4 = Label(root,text="Servo4")
s1 = Scale(root,variable=Servo1,orient=HORIZONTAL,length=200,from_=30,to=210,resolution=0.1)
s2 = Scale(root,variable=Servo2,orient=HORIZONTAL,length=200,from_=40,to=220,resolution=0.1)
s3 = Scale(root,variable=Servo3,orient=HORIZONTAL,length=200,from_=0,to=90,resolution=0.1)
s4 = Scale(root,variable=Servo4,orient=HORIZONTAL,length=200,from_=0,to=180,resolution=0.1)
label_bt.pack(fill='both')
label_s1.pack(fill='both')
s1.pack(fill='both')
label_s2.pack(fill='both')
s2.pack(fill='both')
label_s3.pack(fill='both')
s3.pack(fill='both')
label_s4.pack(fill='both')
s4.pack(fill='both')
t1 = connectionThread()
t1.start()
root.mainloop()
ser.close()
print("Finished")

from tkinter import *
import signal
import time
import threading
import serial
import json
import math
from GahakuKinematics import GahakuKinematics 

class connectionThread(threading.Thread):

    def __init__(self):
        super(connectionThread, self).__init__()
        self.setDaemon(True)

    def run(self):
        while True:
            res = Kinetics.InverceKinematics(X.get(),Y.get(),Z.get())

            print("Servo1:"+str(res[3]))
            print("Servo2:"+str(res[2]))
            print("Servo3:"+str(res[1]))
            print("Servo4:"+str(res[0]))

            list = {'Servo1':-res[3]+210,'Servo2':-res[2]+220,'Servo3':res[1]+27.9,'Servo4':res[0]}
            json_data = json.dumps(list)+";"
            print(json_data)

            json_byte=bytes(json_data,'utf-8')
            ser.write(json_byte)
            res = str(ser.read(5).decode())
            print(res[0:2])

            while(res[0:2] != "OK"):
                time.sleep(0.005)
                ser.write(json_byte)
                res = str(ser.read(5).decode())
            value = int(res[2:5])
            voltage = round(value*5/1024*2,3)
            Battery.set("Battery:"+str(voltage)+"V")
            print (str(voltage)+"V")
            time.sleep(0.005)

ser = serial.Serial('/dev/ttyACM0',38400,timeout=1)
Kinetics = GahakuKinematics()
root = Tk()
root.title("GAHAKU")

Battery = StringVar()
Battery.set("NULL")
X = DoubleVar()
Y = DoubleVar()
Z = DoubleVar()

label_bt = Label(root,textvariable=Battery)
label_x = Label(root,text="X_AXSIS")
label_y = Label(root,text="Y_AXSIS")
label_z = Label(root,text="Z_AXSIS")

x = Scale(root,variable=X,orient=HORIZONTAL,length=200,from_=-150,to=150,resolution=0.1)
y = Scale(root,variable=Y,orient=HORIZONTAL,length=200,from_=150,to=400,resolution=0.1)
z = Scale(root,variable=Z,orient=HORIZONTAL,length=200,from_=0,to=100,resolution=0.1)

label_bt.pack(fill='both')
label_x.pack(fill='both')
x.pack(fill='both')
label_y.pack(fill='both')
y.pack(fill='both')
label_z.pack(fill='both')
z.pack(fill='both')

t1 = connectionThread()
t1.start()
root.mainloop()
ser.close()
print("Finished")


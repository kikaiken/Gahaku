from tkinter import *
import signal
import time
import threading
import serial
import json
import math
from GahakuKinematics import GahakuKinematics 
import numpy as np

pi = np.pi/20

class connectionThread(threading.Thread):

    def __init__(self):
        super(connectionThread, self).__init__()
        self.setDaemon(True)
        self.ser = serial.Serial("/dev/ttyACM0",9600,timeout=1)
    def run(self):
        old_X=X.get()
        old_Y=Y.get()
        old_Z=Z.get()
        while True:
            new_X = X.get()
            new_Y = Y.get()
            new_Z = Z.get()
            servo_data = deff_cordinate(old_X,old_Y,old_Z,new_X,new_Y,new_Z)
            for servo_item in servo_data:
                data = {'Servo1':int(servo_item["servo1"]),'Servo2':int(servo_item["servo2"]),'Servo3':int(servo_item["servo3"]),'Servo4':int(servo_item["servo4"])}
                json_data = json.dumps(data)+";"
                json_byte = bytes(json_data,'utf-8')
                self.ser.write(json_byte)
                recv = str(self.ser.read(2).decode())
                print(json_data)
                print(recv)
                while(recv[0:2] != "OK"):
                    recv = self.ser.write(json_byte)
                    self.ser.write(json_byte)
                    recv = str(self.ser.read(2).decode())
                time.sleep(0.005)
            old_X = new_X
            old_Y = new_Y
            old_Z = new_Z

def deff_cordinate(oldX,oldY,oldZ,newX,newY,newZ):
    res_old = GahakuKinematics().InverceKinematics(oldX,oldY,oldZ)
    res_new = GahakuKinematics().InverceKinematics(newX,newY,newZ)
    s1_old = -res_old[3]+210
    s2_old = -res_old[2]+220
    s3_old = res_old[1]+27.9
    s4_old = res_old[0]
    s1_new = -res_new[3]+210
    s2_new = -res_new[2]+220
    s3_new = res_new[1]+27.9
    s4_new = res_new[0]
    print(s4_new)
    servo_data = []
    for i in np.arange(0,20):
        tmp1 = differ(s1_old,s1_new,i)
        tmp2 = differ(s2_old,s2_new,i)
        tmp3 = differ(s3_old,s3_new,i)
        tmp4 = differ(s4_old,s4_new,i)
        servo = {"servo1":tmp1,"servo2":tmp2,"servo3":tmp3,"servo4":tmp4}
        servo_data.append(servo)
    return servo_data

def differ(old,new,t):
    diff = (new - old)/2
    return -diff * np.cos(pi*t) + old + diff
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
x = Scale(root,variable=X,orient=HORIZONTAL,length=200,from_=-70,to=70,resolution=0.1)
y = Scale(root,variable=Y,orient=HORIZONTAL,length=200,from_=150,to=350,resolution=0.1)
z = Scale(root,variable=Z,orient=HORIZONTAL,length=200,from_=0,to=100,resolution=0.1)
label_bt.pack(fill='both')
label_x.pack(fill='both')
x.pack(fill='both')
label_y.pack(fill='both')
y.pack(fill='both')
label_z.pack(fill='both')
z.pack(fill='both')
z.set(50)
t1 = connectionThread()
t1.start()
root.mainloop()
ser.close()
print("Finished")


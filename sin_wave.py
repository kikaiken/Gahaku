import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as anime
import threading
import serial
import json
import time
ser = serial.Serial('/dev/ttyACM0',38400,timeout=1)

fs = 200
f0 = 1
s1=[]
s2=[]
s3=[]
s4=[]
fig = plt.figure()
for n in range(0,int(fs/f0)):
    s_1 = 45 * np.sin(2.0 * np.pi * f0 * n / fs) + 45
    s_2 = 65 * np.cos(2.0 * np.pi * f0 * n / fs) + 115
    s_3 = -52.5 * np.sin(2.0 * np.pi * f0 * n / fs) + 72.5
    s_4 = -90 * np.cos(2.0 * np.pi * f0 * n / fs) + 90
    s1.append(s_1)
    s2.append(s_2)
    s3.append(s_3)
    s4.append(s_4)
def plot(data):
    plt.cla()
    tmp = s1.pop(0)
    s1.append(tmp)
    plt.plot(s1)
    tmp = s2.pop(0)
    s2.append(tmp)
    plt.plot(s2)
    tmp = s3.pop(0)
    s3.append(tmp)
    plt.plot(s3)
    tmp = s4.pop(0)
    s4.append(tmp)
    plt.plot(s4)
    print("Servo1:"+str(s1[-1]))
    print("Servo2:"+str(s2[-1]))
    print("Servo3:"+str(s3[-1]))
    print("Servo4:"+str(s4[-1]))
    list = {'Servo1':s1[-1],'Servo2':s2[-1],'Servo3':s3[-1],'Servo4':s4[-1]}
    json_data = json.dumps(list)+";"
    print(json_data)
    json_byte=bytes(json_data,'utf-8')
    ser.write(json_byte)
    while(str(ser.read(2).decode()) != "OK"):
        time.sleep(0.005)
        ser.write(json_byte)
ani = anime.FuncAnimation(fig,plot,interval=50)
plt.show()

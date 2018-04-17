#!/usr/bin/python3

import tkinter
import sys
import time
import threading
import serial
import json
import math
from datetime import datetime
from GahakuKinematics import GahakuKinematics 
import numpy as np
import csv
import os
import tkinter.filedialog
import tkinter.messagebox
import position
import lineSplit

fs = 10

ser = serial.Serial("/dev/ttyACM0",76800,timeout=1)

def filterForWindow(x, y, z):
    return [-int(x)/4 + 80, -int(y)/4 + 380, int(z)]

def Inverse_filterForWindow(x, y, z):
    return [-4*(int(x) - 80),-4*(int(y) - 380), int(z)]

def serial_send(x,y,z):
    print("Canvas_X:"+str(x)+"Canvas_Y:"+str(y)+"Canvas_Z:"+str(z))
    res = GahakuKinematics().InverceKinematics(int(x),int(y),int(z))
    data = {'Servo1':format(-res[3]+210,'.3f'),'Servo2':format(-res[2]+220,'.3f'),'Servo3':format(res[1]+27.9,'.3f'),'Servo4':format(res[0],'.3f')}
    json_data = json.dumps(data)+";"
    print(json_data)
    json_byte = bytes(json_data,'utf-8')
    ser.write(json_byte)
    recv = str(ser.read(2).decode())
    while(recv[0:2] != "OK"):
        ser.write(json_byte)
        recv = str(ser.read(2).decode())
        time.sleep(0.005)

class csv_logger:
    def __init__(self):
        self.init_flag = False

    def close(self):
        self.f.close()

    def open(self):
        root = tkinter.Tk()
        root.withdraw()
        fTyp = [("",".csv")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        csvdir = iDir + '/csvfiles'
        csv_name = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = csvdir)
        self.f = open(csv_name,"r")
        return csv.reader(self.f)

class my_class:
    def __init__(self):
        self.logger = None
        self.create_window()

    def create_window(self):
        window = tkinter.Tk()
        self.canvas = tkinter.Canvas(window, bg = "white", width = 640, height = 800)
 
        self.canvas.pack()
        quit_button = tkinter.Button(window, text = "終了", command = window.quit)
        quit_button.pack(side = tkinter.RIGHT)

        reset_button = tkinter.Button(window, text="Reset")
        reset_button.bind("<Button-1>",self.erase) 
        reset_button.pack(side = tkinter.LEFT)
        

        log_open_button = tkinter.Button(window, text="読み込み")
        log_open_button.bind("<Button-1>",self.log_open) 
        log_open_button.pack(side = tkinter.LEFT)

        COLORS = ["red", "green", "blue", "black"]
        self.color = tkinter.StringVar()
        self.color.set(COLORS[1])
        b = tkinter.OptionMenu(window, self.color, *COLORS)
        b.pack()
        window.mainloop()
        self.th._stop()

    def erase(self, event):
        self.canvas.delete("line")
    
    def log_open(self,event):
        self.logger = csv_logger()
        data_list = self.logger.open()
        self.th = threading.Thread(target=draw_canvas2, name="draw_thread", args=(self.canvas, self.color.get(), data_list,))
        self.th.setDaemon(True)
        self.th.start()

def draw_canvas(canvas,color,data):
    pri_x = 0
    pri_y = 0
    for item in data:
        if int(item[2]) == 0:
            if pri_x == 0 and pri_y == 0:
                canvas.create_oval(item[0], item[1], item[0], item[1], outline=color, width=5, tag="line")
            else:
                canvas.create_line(pri_x, pri_y, item[0], item[1], fill=color, width=3, tag="line")
        serial_send(-int(item[0])/4+80,380-int(item[1])/4,item[2])
        pri_x = item[0]
        pri_y = item[1]
        time.sleep(0.05)
    
def draw_canvas2(canvas, color, data):
    pre_state = position.Point()
    cur_state = position.Point()

    for item in data:
        if pre_state.Windowpoint == [0, 0, 0]:
            cur_state.Windowpoint = item
            cur_state.point = filterForWindow(*cur_state.Windowpoint)
            if float(cur_state.point[2]) <= 2:
                canvas.create_oval(cur_state.Windowpoint[0], cur_state.Windowpoint[1], cur_state.Windowpoint[0], cur_state.Windowpoint[1], outline=color, width=3, tag="line")

            pre_state.Windowpoint = cur_state.Windowpoint
            pre_state.point = cur_state.point
            
        else:
            cur_state.Windowpoint = item
            cur_state.point = filterForWindow(*cur_state.Windowpoint)
            
            point_buff = lineSplit.lineSplit_sin(pre_state.point, cur_state.point)

            for n in range(fs):
                cur_state.point = point_buff[n]
                cur_state.Windowpoint = Inverse_filterForWindow(*cur_state.point)
                if float(cur_state.Windowpoint[2]) < -1:
                    canvas.create_line(pre_state.Windowpoint[0], pre_state.Windowpoint[1], cur_state.Windowpoint[0], cur_state.Windowpoint[1], fill=color, width=5, tag="line")
                if - 1 <= float(cur_state.Windowpoint[2]) <= 2:
                    canvas.create_line(pre_state.Windowpoint[0], pre_state.Windowpoint[1], cur_state.Windowpoint[0], cur_state.Windowpoint[1], fill=color, width=3, tag="line")
                if 2 <= float(cur_state.Windowpoint[2]) <= 5:
                    canvas.create_line(pre_state.Windowpoint[0], pre_state.Windowpoint[1], cur_state.Windowpoint[0], cur_state.Windowpoint[1], fill=color, width=1, tag="line")
                
                serial_send(*cur_state.point)

                pre_state.Windowpoint = cur_state.Windowpoint
                pre_state.point = cur_state.point
                time.sleep(0.02)
            
            pre_state.Windowpoint = cur_state.Windowpoint
            pre_state.point = cur_state.point
            
serial_send(0,250,20)
root = my_class()
ser.close()
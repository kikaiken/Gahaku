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

ser = serial.Serial("/dev/ttyACM0",76800,timeout=1)

def serial_send(x,y,z):
    print("Canvas_X:"+str(x)+"Canvas_Y:"+str(y)+"Canvas_Z:"+str(z))
    res = GahakuKinematics().InverceKinematics(x,y,z)
    data = {'Servo1':format(-res[3]+210,'.3f'),'Servo2':format(-res[2]+220,'.3f'),'Servo3':format(res[1]+27.9,'.3f'),'Servo4':format(res[0], '.3f')}
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

    def write(self,x,y,z):
        if self.init_flag != True:
            now_time = datetime.now()
            csv_name = now_time.isoformat()+".csv"
            self.f = open(csv_name,"w")
            self.writer = csv.writer(self.f, lineterminator='\n') 
            self.init_flag = True
        tmp_data = [x,y,z]
        self.writer.writerow(tmp_data)
    
    def close(self):
        self.f.close()

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
        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        
        COLORS = ["red", "green", "blue", "#FF00FF", "black"]

        reset_button = tkinter.Button(window, text="Reset")
        reset_button.bind("<Button-1>",self.erase) 
        reset_button.pack(side = tkinter.LEFT)
        
        log_start_button = tkinter.Button(window, text="記録開始")
        log_start_button.bind("<Button-1>",self.log_start) 
        log_start_button.pack(side = tkinter.LEFT)
        
        log_stop_button = tkinter.Button(window, text="記録停止")
        log_stop_button.bind("<Button-1>",self.log_stop) 
        log_stop_button.pack(side = tkinter.LEFT)
        
        self.log_status_text = tkinter.StringVar()
        self.log_status_text.set("記録停止中...")
        log_status_label = tkinter.Label(window,textvariabl=self.log_status_text)
        log_status_label.pack(side = tkinter.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_pressed)
        self.canvas.bind("<B1-Motion>", self.on_dragged)
        self.canvas.bind("<Motion>",self.on_move)   
        COLORS = ["red", "green", "blue", "black"]
        self.color = tkinter.StringVar()
        self.color.set(COLORS[1])
        b = tkinter.OptionMenu(window, self.color, *COLORS)
        b.pack()
        window.mainloop()

    def on_pressed(self, event):
        self.sx = event.x
        self.sy = event.y
        self.canvas.create_oval(self.sx, self.sy, event.x, event.y, outline=self.color.get(), width=5, tag="line")
        if self.sx >= 0 and self.sx <= 640 and self.sy >= 0 and self.sy <= 800:
            serial_send(-self.sx/4+80,380-self.sy/4,0)
            if self.logger != None:
                self.logger.write(self.sx,self.sy,0)

    def on_dragged(self, event):
        self.canvas.create_line(self.sx, self.sy, event.x, event.y, fill=self.color.get(), width=3, tag="line")
        self.sx = event.x
        self.sy = event.y
        if self.sx >= 0 and self.sx <= 640 and self.sy >= 0 and self.sy <= 800:
            serial_send(-self.sx/4+80,380-self.sy/4,0)
            if self.logger != None:
                self.logger.write(self.sx,self.sy,0)

    def on_move(self,event):
        self.sx = event.x
        self.sy = event.y
        if self.sx >= 0 and self.sx <= 640 and self.sy >= 0 and self.sy <= 800:
            serial_send(-self.sx/4+80,380-self.sy/4,20)
            if self.logger != None:
                self.logger.write(self.sx,self.sy,20)

    def erase(self, event):
        self.canvas.delete("line")

    def log_start(self,event):
        self.logger = csv_logger()    
        self.log_status_text.set("記録中...")
    def log_stop(self,event):
        self.logger.close()
        self.logger = None
        self.log_status_text.set("記録停止中...")
    
serial_send(0,250,20)
root = my_class()
ser.close()

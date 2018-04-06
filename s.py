import serial
import json
import time

def main():
    ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
    list = {'servo1':100,'servo2':100,'servo3':100,'servo4':100}
    json_data = json.dumps(list)+";"
    print(json_data)
    flag=bytes(json_data,'utf-8')
    ser.write(flag)
    cnt = 0
    while(str(ser.read(2).decode()) != "OK"):
        time.sleep(0.1)
        ser.write(flag)
        cnt = cnt + 1
        print(cnt)
    cnt=0
    print("OK")
    if(flag==bytes('a','utf-8')):
        break;
    time.sleep(0.01)
    ser.close()
if __name__ == "__main__":
    main()

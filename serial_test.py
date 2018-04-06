from serial_Arduino import serial_Arduino as seArd

ser = seArd("/dev/ttyUSB0")
data = {"status":"Failed"}
recv = ser.send(data)
print(recv)

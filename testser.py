import os, sys
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout = 5)

while True:
    line = ser.readline()
    if len(line) == 0:
        print("time Out! Exit.\n")
        sys.exit()
    print(line)

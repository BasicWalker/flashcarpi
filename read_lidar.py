import serial

def readLidar():
    global distance, velocity
    try:
        data_raw = ser.readline()
        distance, velocity = ser.readline().decode("utf-8").strip().split("|")
        return distance, velocity
    except:
        pass

if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyUSB0", timeout=None, baudrate=115200, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()

    while True:
        distance, velocity = readLidar()
        print("distance", distance)
        print("velocity", velocity)
    


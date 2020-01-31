import serial

ser = serial.Serial("com4", timeout=None, baudrate=115200, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()

def readLidar():
    data_raw = ser.readline()
    try:
        distance, velocity = ser.readline().decode("utf-8").strip().split("|")
        return distance, velocity
    except:
        pass

if __name__ == "__main__":
    while True:
        distance, velocity = readLidar()
        print("distance", distance)
        print("velocity", velocity)
    


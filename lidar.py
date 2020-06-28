import serial
import serial.tools.list_ports
import time


def read():
    global distance, velocity
    try:
        data_raw = ser.readline()
        distance, velocity = ser.readline().decode("utf-8").strip().split("|")
        return distance, velocity
    except:
        pass

def check(correct_port="ttyUSB0", interval=1):
    global serial_ports, arduino_port, lidar_status
    serial_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    while True:
        serial_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if correct_port not in serial_ports:
            return 0
            break
        elif ser.readline() == "Read fail":
            return 2
        else:
            return 1
        time.sleep(interval)

def connect(port="ttyUSB0"):
    global ser, lidar_status
    ser = serial.Serial(f"/dev/{port}", timeout=None, baudrate=115200, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()


class NoSerialConnection(Exception):
    def __init__(self, port):
        self.port = port
        self.message = f'Arduino port {port} not found in serial ports'
        super().__init__(self.message)
    pass

class FailedRead(Exception):
    def __init__(self,message="Lidar read failed"):
        self.message = message
        super().__init__(self.message)
    pass
    


if __name__ == "__main__":
    import threading

    def start():
        lidar_status = 0
        while True:
            if lidar_status == 0:
                print("no serial connection")
                time.sleep(0.1)
                connect()
            elif lidar_status == 2:
                print("read failure")
            else:
                distance, velocity = read()
                print(f'distance: {distance}, velocity: {velocity}')


            
    lidar_thread = threading.Thread(target=lidar)
    port_controller = threading.Thread(target=check, args=("ttyUSB0", 0.1))
    lidar_thread.start()
    port_controller.start()




    


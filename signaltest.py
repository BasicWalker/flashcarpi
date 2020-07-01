import time
import traceback, sys
import serial
import serial.tools.list_ports
from pathlib import Path
import random


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap  
from PyQt5.Qt import Qt
import obd

from Ui_MainWindow import Ui_MainWindow

class obdWorker(QRunnable):
    '''
    OBD Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''

    def __init__(self, fn):
        super(obdWorker, self).__init__()
        self.obd_try_counter = 0
        self.obd_status = 1
        print("init obd thread")   

    @pyqtSlot()
    def run(self):
        while True:
            print("running")
            if self.obd_status == 0:
                print("not connected")
                try:
                    print("attempting to connect to obd")
                    # self.connection = obd.Async(fast=False, timeout=30)
                    # self.connection.watch(obd.commands.SPEED)
                    # self.connection.watch(obd.commands.RPM)
                    # self.connection.start()
                    self.connection = obd.OBD(fast=False, timeout=30)
                except Exception as e:
                    print(e)
                    self.obd_try_counter += 1
                    if self.obd_try_counter >= 5:
                        print("reached max (5) attempts to connect, stopping attempts")
                        break
                    else:
                        print("obd connection attempt {} of 5 failed, trying again".format(self.obd_try_counter))
                        time.sleep(1)
                        pass
                else:
                    print("connected succesfully")
                    self.obd_status = 1
                    self.obd_try_counter = 0
                    while self.connection.is_connected():
                        print("reading obd")
                        self.read()
                        time.sleep(0.5)
                    else:
                        print("connection broken")
                        self.signal.obd_status = 0
                        break
            else:
                print("connected succesfully")
                self.obd_status = 1
                self.obd_try_counter = 0
                while True:
                    print("reading lidar")
                    self.read()
                    time.sleep(0.5)
                else:
                    print("connection broken")
                    self.obd_status = 0
                    break
    def read(self):
        speed = random.randint(0,100)
        rpm1 = random.randint(0,100)
        print("setting obd reading")
        self.obd_speed = speed
        self.obd_rpm1 = rpm1
        print(self.obd_speed, self.obd_speed)

class lidarWorker(QRunnable):
    '''
    Lidar Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''

    def __init__(self, fn):
        super(lidarWorker, self).__init__() 
        self.lidar_try_counter = 0
        self.lidar_status = 1
        self.serial_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        print("init lidar thread")   

    @pyqtSlot()
    def run(self):
        while True:
            print("running")
            if self.lidar_status == 0:
                print("not connected")
                try:
                    print("attempting to connect to lidar")
                    self.ser = serial.Serial("/dev/ttyUSB0", baudrate=115200)
                except Exception as e:
                    print(e)
                    self.lidar_try_counter += 1
                    if self.lidar_try_counter >= 5:
                        print("reached max (5) attempts to connect, stopping attempts")
                        break
                    else:
                        print("obd connection attempt {} of 5 failed, trying again".format(self.lidar_try_counter))
                        time.sleep(5)
                        pass
                else:
                    print("connected succesfully")
                    self.lidar_status = 1
                    self.obd_try_counter = 0
                    while self.check:
                        self.read()
                        time.sleep(0.5)
                    else:
                        print("connection broken")
                        self.lidar_status = 0
                        break
            else:
                print("connected succesfully")
                self.lidar_status = 1
                self.obd_try_counter = 0
                while True:
                    self.read()
                    time.sleep(0.5)
                else:
                    print("connection broken")
                    self.lidar_status = 0
                    break

    def read(self):
        try:
            distance = random.randint(0,100)
            velocity = random.randint(0,100)
            print("setting lidar reading")
            self.lidar_velocity = velocity
            self.lidar_distance = distance
            print(self.lidar_distance, self.lidar_velocity)
        except Exception as e: print(e)

    def check(self):
        return 1


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        self.asset_path = Path('assets/')
        self.obd_status = int()
        self.obd_speed = int()
        self.obd_rpm1 = int()
        self.lidar_status = int()
        self.lidar_velocity = int()
        self.lidar_distance = int()

        self.show()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.obd_thread()
        self.lidar_thread()

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        print("updating car")
        self.update_car()
        print("updating carfront")
        self.update_carfront()

    def dist_meter_path(self, distance):
        nearest_dist = 2.5 * round(distance/2.5)
        bar_measure_dist = str(nearest_dist).replace(".0", "")
        bar_measure_dist = bar_measure_dist.replace(".", "_")
        png_path = self.asset_path / (bar_measure_dist + 'dist.png')
        return str(png_path)

    def rpm_meter_path(self, rpm):
        nearest_rpm = 500 * round(rpm/500)
        bar_measure_rpm = str(nearest_rpm).replace(".0", "")
        png_path = self.asset_path / (bar_measure_rpm + 'rpm.png')
        return str(png_path)

    def update_carfront(self):
        try:
            distance = self.lidar_distance
            velocity = self.lidar_velocity
            speed = self.obd_speed
            print("setting distance property")
            self.distance.setProperty("value", int(distance))
            print("setting distance frontspeed property")
            self.frontspeed.setProperty("value", int(velocity + speed ))
            print("setting distance frontspeed property")
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
            print("setting distance bars")
        except Exception as e:
            print(e)
            self.distance.setProperty("value", 999)
            self.frontspeed.setProperty("value", 999)
            print("Lidar update failed")

    def update_car(self):
        try:
            speed = self.obd_speed
            rpm1 = self.obd_rpm1
            self.carspeed.setProperty("value", int(speed))
            self.rpm.setProperty("value", int(rpm1))
            self.rpm_meter.setPixmap(QtGui.QPixmap(self.rpm_meter_path(rpm1)))
        except Exception as e:
            print(e)
            self.carspeed.setProperty("value", 999)
            self.rpm.setProperty("value", 999)
            print("obd update failed")

    def obd_function(self):
        print("Starting obd thread")

    def lidar_function(self):
        print("Starting lidar thread")
 
    def obd_thread(self):
        # Pass the function to execute
        obd_worker = obdWorker(self.obd_function)
        
        # Execute
        self.threadpool.start(obd_worker)

    def lidar_thread(self):
        # Pass the function to execute
        lidar_worker = lidarWorker(self.lidar_function)
        
        # Execute
        self.threadpool.start(lidar_worker)



if __name__ == "__main__": 
    # app = QApplication([])
    # window = MainWindow()
    # app.exec_()

    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_()) 
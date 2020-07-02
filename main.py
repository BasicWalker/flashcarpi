import time
import traceback, sys
import serial
import serial.tools.list_ports
from pathlib import Path


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


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:
    
    obd_status
        `int` indicating stats 0 = off, 1 = on

    obd_reading
        `tuple` (speed, rpm)

    lidar_status
        `int` indicating stats 0 = off, 1 = on

    lidar_reading
        `tuple` (speed, rpm)

    '''

    obd_reading = pyqtSignal(tuple)
    lidar_reading = pyqtSignal(tuple)

class obdWorker(QRunnable):
    '''
    OBD Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''

    def __init__(self, fn, *args, **kwargs):
        super(obdWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.obd_try_counter = 0
        self.obd_status = 0
        print("init obd thread")   

    @pyqtSlot()
    def run(self):
        while True:
            print("obd running")
            if self.obd_status == 0:
                print("obd not connected")
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
                        print("reached max (5) attempts to connect to obd, stopping attempts")
                        break
                    else:
                        print("obd connection attempt {} of 5 failed, trying again".format(self.obd_try_counter))
                        time.sleep(1)
                        pass
                else:
                    print("obd connected succesfully")
                    self.obd_status = 1
                    self.obd_try_counter = 0
                    while self.connection.is_connected():
                        self.read()
                    else:
                        print("obd connection broken")
                        self.obd_status = 0
                        break
            else:
                print("obd connected succesfully")
                self.obd_status = 1
                self.obd_try_counter = 0
                while self.connection.is_connected():
                    self.read()
                else:
                    print("obd connection broken")
                    self.obd_status = 0
                    break
    def read(self):
        self.speed = self.connection.query(obd.commands.SPEED).value.to("mph").magnitude
        self.rpm1 = self.connection.query(obd.commands.RPM).value.magnitude
        self.signals.obd_reading.emit((speed, rpm1))
        print("obd reading emitted")

class lidarWorker(QRunnable):
    '''
    Lidar Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    '''

    def __init__(self, fn, *args, **kwargs):
        super(lidarWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        self.lidar_try_counter = 0
        self.lidar_status = 0
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
                        self.read
                    else:
                        print("connection broken")
                        self.lidar_status = 0
                        break
            else:
                print("connected succesfully")
                self.lidar_status = 1
                self.obd_try_counter = 0
                while self.check:
                    self.read
                else:
                    print("connection broken")
                    self.lidar_status = 0
                    break

    def read(self):
        try:
            self.distance, self.velocity = self.ser.readline().decode("utf-8").strip().split("|")
            self.signals.lidar_reading.emit((self.distance, self.velocity))
            print("lidar readings emitted")
        except Exception as e: print(e)

    def check(self, correct_port="ttyUSB0"):
            if correct_port not in serial_ports:
                return 0
            else:
                return 1


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        self.signals = WorkerSignals() 
        self.asset_path = Path('assets/')
        self.speed = 0

        self.show()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.obd_thread()
        self.lidar_thread()

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
            distance, velocity = self.signals.lidar_reading
            self.distance.setProperty("value", int(distance))
            self.frontspeed.setProperty("value", int(velocity + self.speed ))
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
        except:
            self.distance.setProperty("value", 999)
            self.frontspeed.setProperty("Value", 999)
            print("Lidar update failed")

    def update_car(self):
        try:
            speed, rpm1 = self.signals.obd_reading
            self.carspeed.setProperty("value", int(speed))
            self.rpm.setProperty("value", int(rpm1))
            self.rpm_meter.setPixmap(QtGui.QPixmap(self.rpm_meter_path(rpm1)))
        except:
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
        obd_worker.signals.obd_reading.connect(self.update_car)
        
        # Execute
        self.threadpool.start(obd_worker)

    def lidar_thread(self):
        # Pass the function to execute
        lidar_worker = lidarWorker(self.lidar_function)
        lidar_worker.signals.lidar_reading.connect(self.update_carfront)
        
        # Execute
        self.threadpool.start(lidar_worker)



if __name__ == "__main__": 
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec_()) 
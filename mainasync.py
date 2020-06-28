#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from myappasync import MainWindow
import sys
import obd
import time
import threading
import lidar


import sys
import lidar
import obd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap  
from PyQt5.Qt import Qt
from pathlib import Path
from Ui_MainWindow import Ui_MainWindow

# move my app into here

# def get_speed(s):
#    global speed
#    if not s.is_null():
#        speed = int(s.value.to("mph").magnitude)  # MPH conversion

# def get_rpm(r):
#    global rpm1
#    if not r.is_null():
#        rpm1 = int(r.value.magnitude)

def check_obd(interval=1):
    global obd_status
    while True:
        if connection.is_connected():
            obd_status = 1
        else:
            lidar_status = 0
            break
        time.sleep(interval)



def start_obd():
    global connection, obd_status
    obd_status=0
    obd_try_counter=0
    while True:
        if obd_status == 0:
            try:
                # connection = obd.Async(fast=False, timeout=30)
                # connection.watch(obd.commands.SPEED, callback=get_speed)
                # connection.watch(obd.commands.RPM, callback=get_rpm)
                # connection.start()
                print("attempting to connect to obd")
                self.connection = obd.OBD(fast=False, timeout=30)
            except Exception as e:
                print(e)
                obd_try_counter += 1
                if obd_try_counter >= 5:
                    print("reached max (5) attempts to connect, stopping attempts")
                    break
                else:
                    print(f"obd connection attempt {obd_try_counter} failed, trying again")
                    time.sleep(5)
                    pass
            else:
                obd_status = 1
                obd_try_counter=0
                print("starting obd checker")
                thread_obd_checker.start()
                thread_obd_checker.join()
                print("obd connection disrupted")
        else:
            pass


def start_lidar():
    global lidar_status, ser
    lidar_status = 0
    lidar_try_counter = 0
    while True:
        if lidar_status == 0:
            try:
                print("attempting to connect to lidar")
                lidar.connect()
            except Exception as e:
                print(e)
                lidar_try_counter += 1
                if lidar_try_counter >= 5:
                    print("reached max (5) attempts to connect, stopping attempts")
                    break
                else: 
                    print(f"lidar connection attempt {lidar_try_counter} failed, trying again")
                    time.sleep(5)
                    pass
            else:
                lidar_status = 1
                lidar_try_counter = 0
                print("starting lidar checker")
                thread_lidar_checker.start()
                thread_lidar_checker.join()
                print("lidar connection disrupted")
        else:
            pass

def start_gui(timer_clock=20):
    global app, ui, timer
    app = QApplication(sys.argv)
    ui = MainWindow()
    print("showing GUI")
    ui.show()

    print("setting timer")
    timer = QTimer()
    print("connecting timer")
    timer.timeout.connect(ui.update)
    print("starting timer")
    timer.start(timer_clock)  # 20ms default
    sys.exit(app.exec_()) 


if __name__ == "__main__":
    print(sys.version_info)
    print("starting app")
    

    # defining threads
    thread_obd = threading.Thread(target=start_obd)
    thread_lidar = threading.Thread(target=start_lidar)
    thread_gui = threading.Thread(target=start_gui, args=(20,)) 

    thread_lidar_checker = threading.Thread(target=lidar.check, args=("ttyUSB0", 1))
    thread_obd_checker = threading.Thread(target=check_obd, args=(1,))
    

    # starting threads
    thread_obd.start()
    thread_lidar.start()
    time.sleep(0.2)
    thread_gui.start()

    thread_obd.join()
    print("obd thread killed")
    thread_lidar.join()
    print("lidar thread killed")
    thread_gui.join()
    print("gui thread killed")

    # app = QApplication(sys.argv)
    # ui = MainWindow()
    # print("showing GUI")
    # ui.show()

    # print("setting timer")
    # timer = QTimer()
    # print("connecting timer")
    # timer.timeout.connect(ui.update)
    # print("starting timer")
    # timer.start(20)  # 20ms default
    # thread_obd.start()
    # thread_lidar.start()
    # thread_obd.join()
    # print("obd thread killed")
    # thread_lidar.join()
    # print("lidar thread killed")

    # sys.exit(app.exec_())





    
    
    

    



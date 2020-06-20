#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys
import obd
from signal import pause
import time


from myapp import MainWindow

##def get_speed(s):
##    global speed
##    if not s.is_null():
##        speed = int(s.value.to("mph").magnitude)  # MPH conversion
##
##def get_rpm(r):
##    global rpm1
##    if not r.is_null():
##        rpm1 = int(r.value.magnitude)


if __name__ == "__main__":
    global connection
    print(sys.version_info)
    print("starting app")
##    connection = obd.Async(fast=False, timeout=30)
##    connection.watch(obd.commands.SPEED, callback=get_speed)
##    connection.watch(obd.commands.RPM, callback=get_rpm)
##    connection.start()
    
    app = QApplication(sys.argv)
    ui = MainWindow()
    print("showing GUI")
    ui.show()

    
    
    print("setting timer")
    timer = QTimer()
    print("connecting timer")
    timer.timeout.connect(ui.update)
    print("starting timer")
    timer.start(20)
    sys.exit(app.exec_()) 



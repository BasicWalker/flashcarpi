#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys


from myapp import MainWindow


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

##    connection = obd.Async(fast=False, timeout=30)
##    connection.watch(obd.commands.SPEED, callback=get_speed)
##    connection.watch(obd.commands.RPM, callback=get_rpm)
##    connection.start()
    

    timer = QTimer()
    timer.timeout.connect(ui.update)
    timer.start(20)
    sys.exit(app.exec_()) 


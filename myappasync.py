#!/usr/bin/python3
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


asset_path = Path('assets/')

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        self.update()
        self.obd_status = 0
        self.lidar_status = 0

    def update(self):
        self.update_car()
        self.update_carfront()

    def dist_meter_path(self, distance):
        nearest_dist = 2.5 * round(distance/2.5)
        bar_measure_dist = str(nearest_dist).replace(".0", "")
        bar_measure_dist = bar_measure_dist.replace(".", "_")
        png_path = asset_path / (bar_measure_dist + 'dist.png')
        return str(png_path)

    def rpm_meter_path(self, rpm):
        nearest_rpm = 500 * round(rpm/500)
        bar_measure_rpm = str(nearest_rpm).replace(".0", "")
        png_path = asset_path / (bar_measure_rpm + 'rpm.png')
        return str(png_path)

    def update_carfront(self):
        global distance, velocity
        try:
            distance, velocity = lidar.read()
            self.distance.setProperty("intvalue", int(distance))
            self.frontspeed.setProperty("intValue", int(velocity + speed ))
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
        except:
            self.distance.setProperty("value", 999)
            self.frontspeed.setProperty("Value", 999)
            # print("Lidar update failed")

    def update_car(self):
        global speed, rpm1
        try:
            speed = self.connection.query(obd.commands.SPEED).value.to("mph").magnitude
            rpm1 = self.connection.query(obd.commands.RPM).value.magnitude
            self.carspeed.setProperty("value", int(speed))
            self.rpm.setProperty("value", int(rpm1))
            self.rpm_meter.setPixmap(QtGui.QPixmap(self.rpm_meter_path(rpm1)))
        except:
            self.carspeed.setProperty("value", 999)
            self.rpm.setProperty("value", 999)
            # print("obd update failed")

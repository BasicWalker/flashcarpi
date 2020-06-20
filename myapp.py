#!/usr/bin/python3
import sys
import obd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap  
from PyQt5.Qt import Qt
from pathlib import Path



from Ui_MainWindow import Ui_MainWindow
from read_lidar import readLidar
##from obd_read import get_rpm, get_speed

asset_path = Path('assets/')

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        global speed, rpm, distance, frontspeedreading
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        # self.createGraphicView()
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
##        self.connection = obd.Async(fast=False, timeout=30)
        self.connection = obd.OBD(fast=False, timeout=30)
##        self.connection.watch(obd.commands.SPEED, callback=self.get_speed)
##        self.connection.watch(obd.commands.RPM, callback=self.get_rpm)
##        self.connection.start()
##        self.speed = 42
##        self.rpm1 = 0
        self.update()

    # def createGraphicView(self):
    #     self.scene = QGraphicsScene()
    #     self.graphicView = QGraphicsView(self.scene, self)
    #     self.graphicView.setGeometry(0,-80,800,640)
    #     self.graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     self.graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     self.graphicView.setStyleSheet("background-color: transparent;")
    #     self.gaugeline = self.scene.addPixmap(QtGui.QPixmap(str(asset_path / 'gaugehand.png')))
    #     self.gaugeline.setTransformOriginPoint(399, 196)

    def update(self):
        # pass
        self.update_car()
        self.update_carfront()
        # self.gaugeline.setRotation(self.speed_diff(carspeedreading, frontspeedreading))
##        if int(frontspeedreading) == int(carspeedreading):
##            self.okaystat.setPixmap(QtGui.QPixmap(str(asset_path / 'ok.png')))
##        else:
##            self.okaystat.setPixmap(QtGui.QPixmap(''))
                

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

    def speed_diff(self, carspeed, frontcarspeed):
        speed_diff = int(((carspeed - int(frontcarspeed))/ 2 ))
        speed_diff1 = frontcarspeed
        return float(speed_diff)

    def update_carfront(self):
        try:
            distance, frontspeedreading = readLidar()
            self.distance.setProperty("value", distance)
            self.frontspeed.setProperty("intValue", frontspeedreading)
##            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
##            self.frontcar.setGeometry(0, (10 - (int(distance) * 90 / 40)), 800, 640)
        except TypeError:
            self.distance.setProperty("intvalue", 999)
            self.frontspeed.setProperty("intValue", 999)
##            self.dist_meter.setPixmap(QtGui.QPixmap(''))
##            self.frontcar.setPixmap(QtGui.QPixmap(''))
##            self.okaystat.setPixmap(QtGui.QPixmap(Path(str(asset_path / 'error.png'))))
##            self.gaugeline.setRotation(0)
            print("ouch")

    def update_car(self):
        try:
            speed = self.connection.query(obd.commands.SPEED).value.to("mph").magnitude
            rpm1 = self.connection.query(obd.commands.RPM).value.magnitude
            self.carspeed.setProperty("value", int(speed))
            self.rpm.setProperty("value", (rpm1))
            self.rpm_meter.setPixmap(QtGui.QPixmap(self.rpm_meter_path(rpm1)))
        
        except:
            self.carspeed.setProperty("intvalue", 999)
            self.rpm.setProperty("intvalue", 999)
            print("obd update failed")

##    def get_speed(self, s):
##        if not s.is_null():
##            self.speed = int(s.value.to("mph").magnitude)  # MPH conversion
##
##    def get_rpm(self, r):
##        if not r.is_null():
##            self.rpm1 = int(r.value.magnitude)


import sys
import obd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap
from PyQt5.QtCore import  Qt
from PyQt5.Qt import Qt
from pathlib import Path
from signal import pause
from threading import Thread



from Ui_MainWindow import Ui_MainWindow
##from serial_test import readLidar
##from obd_read import get_rpm, get_speed

asset_path = Path('assets/')



class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        global speed, rpm1
        super(MainWindow, self).__init__(parent)
        print("setting up UI")
        self.setupUi(self)
        # self.createGraphicView()
##        self.showFullScreen()
##        print("setting up OBD II connection")
##        self.connection = obd.Async(fast=False, timeout=30)
##        pause()
##
##        self.connection = obd.OBD(fast=False, timeout=30)
##        print("watching for connection")
##        self.connection.watch(obd.commands.SPEED, callback=self.get_speed)
##        self.connection.watch(obd.commands.RPM, callback=self.get_rpm)
##        print("starting OBD connection")
##        self.connection.start()
        self.connect()
        
        
        self.speed = 42
        self.rpm1 = 0
        self.update()
        print("initial update")
        
    # def createGraphicView(self):
    #     self.scene = QGraphicsScene()
    #     self.graphicView = QGraphicsView(self.scene, self)
    #     self.graphicView.setGeometry(0,-80,800,640)
    #     self.graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     self.graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     self.graphicView.setStyleSheet("background-color: transparent;")
    #     self.gaugeline = self.scene.addPixmap(QtGui.QPixmap(str(asset_path / 'gaugehand.png')))
    #     self.gaugeline.setTransformOriginPoint(399, 196)

    def obd_connect(self):
        self.connection = obd.OBD(fast=False, timeout=30)


    def connect(self):
        self.t = Thread(target=self.obd_connect)
        self.t.start()
        


    def update(self):
        self.update_car()
##        self.update_carfront()
        # self.gaugeline.setRotation(self.speed_diff(carspeedreading, frontspeedreading))
##        if int(frontspeedreading) == int(carspeedreading):
##            self.okaystat.setPixmap(QtGui.QPixmap(str(asset_path / 'ok.png')))
##        else:
##            self.okaystat.setPixmap(QtGui.QPixmap(''))
                

    def dist_meter_path(self, distance):
        nearest_dist = 2.5 * round(distance/2.5)
        bar_measure = str(nearest_dist).replace(".0", "")
        bar_measure = bar_measure.replace(".", "_")
        png_path = asset_path / (bar_measure + 'dist.png')
        return str(png_path)

    def speed_diff(self, carspeed, frontcarspeed):
        speed_diff = int(((carspeed - int(frontcarspeed))/ 2 ))
        speed_diff1 = frontcarspeed
        return float(speed_diff)

    def update_carfront(self):
        global distance, frontspeedreading
        try:
            distance, frontspeedreading = readLidar()
            self.distance.setProperty("value", distance)
            self.frontspeed.setProperty("intValue", frontspeedreading)
##            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
            self.frontcar.setGeometry(0, (10 - (int(distance) * 90 / 40)), 800, 640)
        except TypeError:
            self.distance.setProperty("intvalue", 999)
            self.frontspeed.setProperty("intValue", 999)
            self.dist_meter.setPixmap(QtGui.QPixmap(''))
            self.frontcar.setPixmap(QtGui.QPixmap(''))
            self.okaystat.setPixmap(QtGui.QPixmap(Path(str(asset_path / 'error.png'))))
            self.gaugeline.setRotation(0)
            print("ouch")

    def update_car(self):
        global speed, rpm1, connection
        speed = self.connection.query(obd.commands.SPEED).value.to("mph").magnitude
        rpm1 = self.connection.query(obd.commands.RPM).value.magnitude
        self.carspeed.setProperty("value", self.speed)
        self.rpm.setProperty("value", self.rpm1)
        
        # except:
        #     self.carspeed.setProperty("intvalue", 999)
        #     self.rpm.setProperty("intvalue", 999)
        #     print("obd update failed")

    def get_speed(self, s):
        if not s.is_null():
            self.speed = int(s.value.to("mph").magnitude)  # MPH conversion

    def get_rpm(self, r):
        if not r.is_null():
            self.rpm1 = int(r.value.magnitude)

        

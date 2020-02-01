import sys
import obd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap
from PyQt5.QtCore import  Qt
from PyQt5.Qt import Qt
from pathlib import Path



from Ui_MainWindow import Ui_MainWindow
from serial_test import readLidar
from obd_read import get_rpm, get_speed

asset_path = Path('assets/')

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.createGraphicView()
        # self.showFullScreen() 
        self.connection = obd.Async(fast=False, timeout=30)
        self.connection.start()
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
        global speed
        speed = 10  # for testing
        self.update_car()
        self.update_carfront()
        
        
        # carspeedreading = -30  # for testing 
        # self.gaugeline.setRotation(self.speed_diff(carspeedreading, frontspeedreading))
        # if int(frontspeedreading) == int(carspeedreading):
        #         self.okaystat.setPixmap(QtGui.QPixmap(str(asset_path / 'ok.png')))
        # else:
        #     self.okaystat.setPixmap(QtGui.QPixmap(''))
                

    def dist_meter_path(self, distance):
        png_path = asset_path / (str(distance) + 'dist.png')
        return str(png_path)

    def speed_diff(self, carspeed, frontcarspeed):
        speed_diff = int(((carspeed - int(frontcarspeed))/ 2 ))
        speed_diff1 = frontcarspeed
        print(speed_diff1)
        print(speed_diff)



        return float(speed_diff)

    def update_carfront(self):
        global distance, frontspeedreading, speed
        try:
            distance, frontspeedreading = readLidar()
            frontspeedreading += speed
            self.distance.setProperty("value", distance)
            self.frontspeed.setProperty("intValue", frontspeedreading)
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
            self.frontcar.setGeometry(0, (10 - (int(distance) * 90 / 40)), 800, 640)
        except TypeError:
            self.distance.setProperty("intvalue", 999)
            self.frontspeed.setProperty("intValue", 999)
            self.dist_meter.setPixmap(QtGui.QPixmap(Path(str(asset_path / '0dist.png'))))
            self.frontcar.setPixmap(QtGui.QPixmap(''))
            self.okaystat.setPixmap(QtGui.QPixmap(Path(str(asset_path / 'error.png'))))
            self.gaugeline.setRotation(0)
            print("ouch")

    def update_car(self):
        global speed
        self.connection.watch(obd.commands.SPEED, callback=get_speed)
        self.connection.watch(obd.commands.RPM, callback=get_rpm)
        self.carspeed.setProperty("intvalue", int(speed))
        self.rpm.setProperty("intvalue", int(rpm))
        # except:
        #     self.carspeed.setProperty("intvalue", 999)
        #     self.rpm.setProperty("intvalue", 999)
        #     print("obd update failed")

        

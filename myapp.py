import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap
from PyQt5.QtCore import  Qt
from PyQt5.Qt import Qt
from pathlib import Path


from Ui_MainWindow import Ui_MainWindow
from serial_test import readLidar

asset_path = Path('assets/')

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.createGraphicView()
        # self.showFullScreen() 
        self.update_lcd()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.graphicView = QGraphicsView(self.scene, self)
        self.graphicView.setGeometry(0,-80,800,640)
        self.graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicView.setStyleSheet("background-color: transparent;")
        self.gaugeline = self.scene.addPixmap(QtGui.QPixmap(str(asset_path / 'gaugehand.png')))
        self.gaugeline.setTransformOriginPoint(399, 196)

    def dist_meter_path(self, distance):
        png_path = asset_path / (str(distance) + 'dist.png')
        return str(png_path)

    def speed_diff(self, carspeed, frontcarspeed):
        speed_diff = float((carspeed - int(frontcarspeed) * 90/20)) 
        return speed_diff 

    def update_lcd(self):
        try:
            distance, frontspeedreading = readLidar()
            carspeedreading = 10    
            self.distance.setProperty("value", distance)
            self.frontspeed.setProperty("intValue", frontspeedreading)
            
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
            self.gaugeline.setRotation(self.speed_diff(carspeedreading, frontspeedreading))
            self.graphicView.setGeometry(0,-80,800,640)
            self.frontcar.setGeometry(0, (10 - (int(distance) * 90 / 40)), 800, 640)
            if int(frontspeedreading) == int(10):
                self.okaystat.setPixmap(QtGui.QPixmap(str(asset_path / 'ok.png')))
            else:
                self.okaystat.setPixmap(QtGui.QPixmap(''))

        except TypeError:
            self.distance.setProperty("intvalue", 999)
            self.frontspeed.setProperty("intValue", 999)
            self.dist_meter.setPixmap(QtGui.QPixmap(Path(str(asset_path / '0dist.png'))))
            self.frontcar.setPixmap(QtGui.QPixmap(''))
            self.okaystat.setPixmap(QtGui.QPixmap(Path(str(asset_path / 'error.png'))))
            self.gaugeline.setRotation(0)
            print("ouch")

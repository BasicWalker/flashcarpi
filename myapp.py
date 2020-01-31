import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPen,  QPixmap
from PyQt5.QtCore import  Qt
from PyQt5.Qt import Qt


from Ui_MainWindow import Ui_MainWindow
from serial_test import readLidar

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.createGraphicView()
        # self.showFullScreen()
        self.update_lcd()

    def createGraphicView(self):
        self.scene = QGraphicsScene()
        self.pen = QPen(Qt.red)
        self.pen.setWidth(3)
        self.pen.setCapStyle(Qt.RoundCap)
        graphicView = QGraphicsView(self.scene, self)
        graphicView.setGeometry(0,-80,800,640)
        graphicView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        graphicView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        graphicView.setStyleSheet("background-color: transparent;")
        self.gaugeline = self.scene.addPixmap(QtGui.QPixmap('FlashCarPi/assets/gaugehand.png'))
        self.gaugeline.setTransformOriginPoint(399, 196)

    def dist_meter_path(self, distance):
        png_path = 'FlashCarPi/assets/' + distance + 'dist.png'
        return png_path

    def update_lcd(self):
        try:
            distance, velocity = readLidar()
            self.distance.setProperty("value", distance)
            self.frontspeed.setProperty("intValue", velocity)
            self.dist_meter.setPixmap(QtGui.QPixmap(self.dist_meter_path(distance)))
            self.gaugeline.setRotation(float(velocity))
            self.frontcar.setGeometry(0, (-80 + int(distance)), 800, 640)
            # if int(velocity) == int(self.carspeed.value):
            #     self.okaystat.setPixmap(QtGui.QPixmap('FlashCarPi/assets/ok.png'))
            # else:
            #     self.okaystat.setText("")
        except TypeError:
            self.distance.setProperty("intvalue", 9999)
            self.frontspeed.setProperty("intValue", 9999)
            self.dist_meter.setPixmap(QtGui.QPixmap('FlashCarPi/assets/0dist.png'))
            self.gaugeline.setRotation(0)

        
 


# 'FlashCarPi/assets/frontcar.png'
# 'FlashCarPi/assets/gaugehand.png'
# 'FlashCarPi/assets/ok.png'
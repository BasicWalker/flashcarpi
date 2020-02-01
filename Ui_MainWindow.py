#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path

asset_path = Path('assets/')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.frontspeed = QtWidgets.QLCDNumber(self.centralwidget)
        self.frontspeed.setGeometry(QtCore.QRect(330, 40, 291, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frontspeed.sizePolicy().hasHeightForWidth())
        self.frontspeed.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        # palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        # palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 108, 17, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        # palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.frontspeed.setPalette(palette)
        self.frontspeed.setStyleSheet("QLCDNumber{\n"
"    color: rgb(255,108,17) ;\n"
"}")
        self.frontspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frontspeed.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.frontspeed.setProperty("intValue", 45)
        self.frontspeed.setObjectName("frontspeed")
        self.carspeed = QtWidgets.QLCDNumber(self.centralwidget)
        self.carspeed.setGeometry(QtCore.QRect(50, 40, 291, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.carspeed.sizePolicy().hasHeightForWidth())
        self.carspeed.setSizePolicy(sizePolicy)
        self.carspeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.carspeed.setStyleSheet("QLCDNumber{\n"
"    color: rgb(255,108,17) ;\n"
"}")
        self.carspeed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.carspeed.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.carspeed.setProperty("intValue", 10)
        self.carspeed.setObjectName("carspeed")
        self.Background = QtWidgets.QLabel(self.centralwidget)
        self.Background.setGeometry(QtCore.QRect(0, -80, 800, 640))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Background.sizePolicy().hasHeightForWidth())
        self.Background.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.Background.setFont(font)
        self.Background.setStyleSheet("color: rgb(45, 226, 230);")
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap(str(asset_path / "flashretrobackground.jpg")))
        self.Background.setAlignment(QtCore.Qt.AlignCenter)
        self.Background.setObjectName("Background")
        self.rpm = QtWidgets.QLCDNumber(self.centralwidget)
        self.rpm.setGeometry(QtCore.QRect(120, 370, 111, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.rpm.sizePolicy().hasHeightForWidth())
        self.rpm.setSizePolicy(sizePolicy)
        self.rpm.setStyleSheet("QLCDNumber{\n"
"    color: rgb(255,108,17) ;\n"
"}")
        self.rpm.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.rpm.setDigitCount(4)
        self.rpm.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rpm.setProperty("intValue", 2456)
        self.rpm.setObjectName("rpm")
        self.distance = QtWidgets.QLCDNumber(self.centralwidget)
        self.distance.setGeometry(QtCore.QRect(550, 370, 121, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.distance.sizePolicy().hasHeightForWidth())
        self.distance.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.distance.setFont(font)
        self.distance.setStyleSheet("QLCDNumber{\n"
"    color: rgb(255,108,17) ;\n"
"}")
        self.distance.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.distance.setSmallDecimalPoint(True)
        self.distance.setDigitCount(5)
        self.distance.setMode(QtWidgets.QLCDNumber.Dec)
        self.distance.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.distance.setProperty("value", 23.0)
        self.distance.setProperty("intValue", 23)
        self.distance.setObjectName("distance")
        self.rpm_meter = QtWidgets.QLabel(self.centralwidget)
        self.rpm_meter.setGeometry(QtCore.QRect(0, -80, 800, 640))
        self.rpm_meter.setAutoFillBackground(False)
        self.rpm_meter.setStyleSheet("")
        self.rpm_meter.setText("")
        self.rpm_meter.setTextFormat(QtCore.Qt.RichText)
        self.rpm_meter.setPixmap(QtGui.QPixmap(""))
        self.rpm_meter.setScaledContents(False)
        self.rpm_meter.setOpenExternalLinks(False)
        self.rpm_meter.setObjectName("rpm_meter")
        self.dist_meter = QtWidgets.QLabel(self.centralwidget)
        self.dist_meter.setGeometry(QtCore.QRect(0, -80, 800, 640))
        self.dist_meter.setAutoFillBackground(False)
        self.dist_meter.setStyleSheet("")
        self.dist_meter.setText("")
        self.dist_meter.setTextFormat(QtCore.Qt.RichText)
        self.dist_meter.setPixmap(QtGui.QPixmap(""))
        self.dist_meter.setScaledContents(False)
        self.dist_meter.setOpenExternalLinks(False)
        self.dist_meter.setObjectName("dist_meter")
        self.frontcar = QtWidgets.QLabel(self.centralwidget)
        self.frontcar.setGeometry(QtCore.QRect(0, -80, 800, 640))
        self.frontcar.setText("")
        self.frontcar.setPixmap(QtGui.QPixmap(str(asset_path / "frontcar.png")))
        self.frontcar.setObjectName("frontcar")
        self.okaystat = QtWidgets.QLabel(self.centralwidget)
        self.okaystat.setGeometry(QtCore.QRect(0, -80, 800, 640))
        self.okaystat.setText("")
        self.okaystat.setPixmap(QtGui.QPixmap(str(asset_path / "ok.png")))
        self.okaystat.setObjectName("okaystat")
        self.Background.raise_()
        self.dist_meter.raise_()
        self.rpm_meter.raise_()
        self.frontspeed.raise_()
        self.rpm.raise_()
        self.distance.raise_()
        self.carspeed.raise_()
        self.frontcar.raise_()
        self.okaystat.raise_()
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 0, 25, 25))
        font = QtGui.QFont()
        font.setStrikeOut(True)
        font.setKerning(True)
        self.pushButton.setFont(font)
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(asset_path / "exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setShortcut("")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

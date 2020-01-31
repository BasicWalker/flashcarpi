from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from myapp import MainWindow
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    timer = QTimer()
    timer.timeout.connect(ui.update_lcd)
    timer.start(20)
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys


from myapp import MainWindow




if __name__ == "__main__":
    global connection

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    

    timer = QTimer()
    timer.timeout.connect(ui.update)
    timer.start(20)
    sys.exit(app.exec_()) 


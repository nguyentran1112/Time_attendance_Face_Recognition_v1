import sys
# pip install pyqt5
from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTime, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_MainWindow
from formview import Ui_WindowCheck
import cv2
from time import time
# from test import capture_video
from be import capture_video


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.pushButton.clicked.connect(self.show_main)
        self.thread = {}


    def closeEvent(self, event):
        self.stop_capture_video()

    def stop_capture_video(self):
        self.thread[1].stop()

    def start_capture_video(self):
        self.thread[1] = capture_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)
        self.uic.textStatus.setText('Connected')

    def show_wedcam(self, img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(img)
        self.uic.view.setPixmap(qt_img)

    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 800, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def show_main(self):
        self.uic = Ui_WindowCheck()
        self.uic.setupUi(self)
        self.uic.checkin.clicked.connect(self.start_capture_video)
        now = datetime.now()
        _date = now.strftime("%d-%m")
        _time = now.strftime("%H:%M")
        self.uic.lcdNumber.display(_time)
        self.uic.lcdNumber_2.display(_date)
        self.uic.textStatus.setText('Not Connected!!!!!!')







if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

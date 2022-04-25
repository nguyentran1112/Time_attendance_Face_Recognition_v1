import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from formview import Ui_WindowCheck
import os
from asyncio.windows_events import NULL
from dis import dis
from tempfile import tempdir
from time import time
from webbrowser import get
import cv2
import numpy as np
from simple_facerec import SimpleFacerec
import pickle
import sqlite3
import csv
from datetime import date, datetime

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(capture_video, self).__init__()


    def run(self):
        # Encode faces from a forder
        sfr = SimpleFacerec()
        sfr.load_encoding_images("DataSet/")
        # Load Camera
        cap = cv2.VideoCapture(0)
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 0.5
        fontcolor = (0, 255, 0)
        fontcolor1 = (0, 0, 255)

        def getProfile_peple(id):
            conn = sqlite3.connect("FaceBaseNew.db")
            cursor = conn.execute("SELECT * FROM People WHERE ID=" + str(id))
            profile = None
            for row in cursor:
                profile = row
            conn.close()
            return profile

        # Hàm lấy thời gian
        def getTime():
            now = datetime.now()
            _date = now.strftime("%d/%m/%Y")
            _time = now.strftime("%H:%M:%S")
            #print("Ngay va gio hien tai =", _date, _time)
            return _date, _time

        # Hàm cập nhật thời gian vào database
        def insertOrUpdate_time(id, date_, time_in):
            conn = sqlite3.connect("FaceBaseNew.db")
            cursor = conn.execute(
                "SELECT * FROM Time_table WHERE (ID=' " + str(id) + " ' AND _Date=' " + str(date_) + " ' )")
            isRecordExist = 0
            for row in cursor:
                isRecordExist = 1
                break
            if isRecordExist == 1:
                cmd = "UPDATE Time_table SET Time_in=' " + str(time_in) + " ' WHERE (ID=' " + str(
                    id) + " ' AND _Date=' " + str(date_) + " ' )"
            else:
                cmd = "INSERT INTO Time_table(ID,_Date,Time_in) Values(" + str(id) + ",' " + str(date_) + " ',' " + str(
                    time_in) + " ' )"
            conn.execute(cmd)
            conn.commit()
            conn.close()

        def csvAdd(num_row):
            temp = 1
            if num_row == 0:
                print("Not exist profile")
            else:
                conn = sqlite3.connect("FaceBaseNew.db")
                cursor = conn.execute("SELECT * FROM Time_table")
                profile = None
                keys = ['STT', 'ID', 'Name', 'Date', 'Time_in', 'Time_out']
                with open('myfile.csv', mode='w') as f:
                    writer = csv.writer(f)
                    writer.writerow(keys)
                    for row in cursor:
                        profile = row
                        if profile == None:
                            break
                        name = getProfile_peple(profile[0])[2]
                        writer.writerow([temp, profile[0], name, profile[1], profile[2], profile[3]])
                        temp += 1
                conn.close()

        def getCount_row():
            conn = sqlite3.connect("FaceBaseNew.db")
            # cursor=conn.execute("SELECT * FROM Time_table WHERE stt = (SELECT MAX(STT) FROM Time_table)")
            cursor = conn.execute("SELECT count(*) FROM Time_table")
            profile = None
            for row in cursor:
                profile = row
            conn.close()

            if profile == None:
                return 0
            return profile[0]
        # chuong trinh chính
        id = 0
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                id = name[5:]
                y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                if name != "Unknown":
                    print("\n")
                    print("User name: ", name)
                    print("Face location: ", face_loc)
                    profile = None
                    profile = getProfile_peple(id)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                    cv2.putText(frame, str(profile[2]), (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    _date, _time = getTime()
                    insertOrUpdate_time(id, _date, _time)
                    cv2.putText(frame, "Date: {}{}".format(_date, _time), (15, 55), fontface, fontscale, fontcolor, 1)
                    num_row = getCount_row()
                    csvAdd(num_row)
                else:
                    print("\n")
                    print("Face location: ", face_loc)
                    print("Unknow")

                if ret:
                    self.signal.emit(frame)
            if cv2.waitKey(1) == 27:
                print("Đã nhấn nút")
                num_row = getCount_row()
                csvAdd(num_row)
                break
        cap.release()
        cv2.destroyAllWindows()
        if ret:
            self.signal.emit(frame)
    def stop(self):
        print("stop threading", self.index)
        self.terminate()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_win = MainWindow1()
#     main_win.show()
#     sys.exit(app.exec())
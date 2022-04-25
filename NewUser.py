
import cv2
import sqlite3
import numpy as np
from cv2 import blur
from PIL import Image
from PIL import ImageEnhance

path = 'video/hiep.mp4'

cam = cv2.VideoCapture(path)

if (cam.isOpened() == False):
    print("Error opening the video file")

# Hàm cập nhật tên và ID vào CSDL
def insertOrUpdate(stt, id, name):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute('SELECT * FROM People WHERE ID='+str(id))
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist==1:
        cmd="UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(id)
        cmd="UPDATE people SET STT= "+str(stt)+" WHERE ID="+str(id)
    else:
        cmd="INSERT INTO people(ID,Name,STT) Values("+str(id)+",' "+str(name)+" ',"+str(stt)+")"

    conn.execute(cmd)
    conn.commit()
    conn.close()
    
id=input('Nhập mã nhân viên: ')
name=input('Nhập tên nhân viên: ')
stt=input('Nhập stt nhân viên: ')
print("Bắt đầu chụp ảnh nhân viên, nhấn q để thoát!")

insertOrUpdate(stt,id,name)

sampleNum=0

while(True):

    ret, img = cam.read()

    # Lật ảnh cho đỡ bị ngược
    #img = cv2.flip(img,1)

    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
    # centerH = img.shape[0] // 2;
    # centerW = img.shape[1] // 2;
    # sizeboxW = 300;
    # sizeboxH = 400;
    # cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
    #               (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)
    
    #img_new = change_brightness(img, 1.2, 35)
    
    #cv2.imshow("map", img_new)
    # Đưa ảnh về ảnh xám
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #blur = cv2.bilateralFilter(gray, 1, 75,75)
    #cv2.imshow("est", blur)
    
    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # filter = cv2.filter2D(blur, -1, kernel)
    
    # equalized_img = cv2.equalizeHist(filter)
    # cv2.imshow("map", equalized_img)
    #equalized_img = blur
    # Nhận diện khuôn mặt
    #faces = detector.detectMultiScale(equalized_img, 1.3, 5)
    #for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
    #    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    sampleNum = sampleNum + 1
        # Ghi dữ liệu khuôn mặt vào thư mục dataSet
    cv2.imwrite("DataSet/User." + id + ".jpg", img)

    cv2.imshow('frame', img)
    # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif sampleNum>1:
         break

cam.release()
cv2.destroyAllWindows()

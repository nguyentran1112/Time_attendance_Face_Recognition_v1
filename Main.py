import cv2
from simple_facerec import SimpleFacerec
import csv
import sqlite3
from datetime import date, datetime
import numpy as np

# Encode faces from a forder
sfr = SimpleFacerec()
sfr.load_encoding_images("DataSet/")

#Load Camera
cap = cv2.VideoCapture(0)

fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 0.5
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)

def getProfile_peple(id):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute("SELECT * FROM People WHERE ID="+str(id))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

# Hàm lấy thời gian
def getTime():
    now = datetime.now()
    
    _date = now.strftime("%d/%m/%Y")
    _time = now.strftime("%H:%M:%S")
    
    print("Ngay va gio hien tai =", _date, _time)
    return _date, _time

# Hàm cập nhật thời gian vào database
def insertOrUpdate_time(id, date_, time_in):
  
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute("SELECT * FROM Time_table WHERE (ID=' "+str(id)+" ' AND _Date=' "+str(date_)+" ' )")
    
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist==1:
        cmd="UPDATE Time_table SET Time_in=' "+str(time_in)+" ' WHERE (ID=' "+str(id)+" ' AND _Date=' "+str(date_)+" ' )"
    else:
        cmd="INSERT INTO Time_table(ID,_Date,Time_in) Values("+str(id)+",' "+str(date_)+" ',' "+str(time_in)+" ' )"
        
    conn.execute(cmd)
    conn.commit()
    conn.close()

    
def csvAdd(num_row):
    temp=1
    if num_row==0:
        print("Not exist profile")
    else:
        conn=sqlite3.connect("FaceBaseNew.db")
        cursor=conn.execute("SELECT * FROM Time_table")
        
        profile=None
        keys = ['STT','ID', 'Name', 'Date', 'Time_in','Time_out']
        with open('myfile.csv', mode='a') as f:
                writer = csv.writer(f)
                writer.writerow(keys)
                for row in cursor:
                    profile=row
                    if profile==None:
                        break
                    name=getProfile_peple(profile[0])[2]
                    writer.writerow([temp, profile[0], name, profile[1], profile[2], profile[3]])
                    temp+=1
        conn.close()

def getCount_row():
    conn=sqlite3.connect("FaceBaseNew.db")
    #cursor=conn.execute("SELECT * FROM Time_table WHERE stt = (SELECT MAX(STT) FROM Time_table)")
    cursor=conn.execute("SELECT count(*) FROM Time_table")
    
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    
    if profile==None:
        return 0
    return profile[0]



#chuong trinh chính
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
            
            profile=None
            profile=getProfile_peple(id)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0 ,255), 4)
            cv2.putText(frame, str(profile[2]), (15, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            _date, _time = getTime()
            
            insertOrUpdate_time(id, _date, _time)
            
            cv2.putText(frame, "Date: {}{}".format(_date,_time), (15,30), fontface, fontscale, fontcolor ,1)
            
        else:
            print("\n")
            print("Face location: ", face_loc)
            print("Unknow")

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)

    if key == 27:
        num_row=getCount_row()
        csvAdd(num_row)
        break

# cap.release()
cv2.destroyAllWindows()
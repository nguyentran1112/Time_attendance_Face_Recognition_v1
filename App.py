from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from simple_facerec import SimpleFacerec
import smtplib
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
from time import sleep
from threading import Thread
import csv
import sqlite3
from datetime import date, datetime
import numpy as np
import time

window = tkinter.Tk()
window.title("Tkinter OpenCV")
video = cv2.VideoCapture(0)
canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2
canvas = tkinter.Canvas(window, width=canvas_w*2, height=canvas_h*2)
canvas.pack(fill=tkinter.BOTH, expand=True, padx = 50, pady = 20)
bw = 0
check_status_active = 0
sfr = SimpleFacerec()
sfr.load_encoding_images("DataSet/")
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 0.5
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)
photo = None
count = 0

def handleCSV():
    num_row=getCount_row()
    csvAdd(num_row)

def getProfile_peple(id):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute("SELECT * FROM People WHERE ID="+str(id))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def handleBW():
    global bw
    bw = 1 - bw

def send_to_lable():
    global lbl_id
    ret, frame = video.read()
    _, _, id, name= Recognition(ret, frame, check_status_active)
    lbl_id.configure(text=str(id + " " + name))
    return

def getTime():
    now = datetime.now()
    _date = now.strftime("%d/%m/%Y")
    _time = now.strftime("%H:%M:%S")
    return _date, _time

def insertOrUpdateTime_In(id, date_, time_in):
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

def insertOrUpdateTime_Out(id, date_, time_out):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute("SELECT * FROM Time_table WHERE (ID=' "+str(id)+" ' AND _Date=' "+str(date_)+" ' )")
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break
    if isRecordExist==1:
        cmd="UPDATE Time_table SET Time_out=' "+str(time_out)+" ' WHERE (ID=' "+str(id)+" ' AND _Date=' "+str(date_)+" ' )"
    else:
        cmd="INSERT INTO Time_table(ID,_Date,Time_out) Values("+str(id)+",' "+str(date_)+" ',' "+str(time_out)+" ' )"
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
        with open('myfile.csv', mode='w') as f:
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
    cursor=conn.execute("SELECT count(*) FROM Time_table")
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    if profile==None:
        return 0
    return profile[0]

def Recognition(ret, frame, status):
    id = []
    User_name = []
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        id = name[5:]
        y1, x1, y2, x2 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        if (name != "Unknown"):
            profile = None
            profile = getProfile_peple(id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), fontcolor1, 4)
            cv2.putText(frame, str(
                profile[2]).strip(), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, fontscale, fontcolor1, 1)
            _date, _time = getTime()
            if status == 1:
                insertOrUpdateTime_In(id, _date, _time)
                cv2.putText(frame, "Check In", (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, fontscale, fontcolor, 1)
            elif status == -1:
                insertOrUpdateTime_Out(id, _date, _time)
                cv2.putText(frame, "Check Out", (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, fontscale, fontcolor1, 1)
            User_name = profile[2].strip()
            cv2.putText(frame, "Date: {}  {}".format(_date, _time),
                        (20, 40), fontface, fontscale, fontcolor1, 1)
        else:
            print("\n")
            print("Unknow user")

    return (ret, frame, id, User_name)

lbl_id = tkinter.Label(window, text="ID", width=30, font=("Arial", 12))
lbl_id.pack(side=tkinter.LEFT, padx=20, pady=5)

checkInButton = tkinter.Button(window, text="Check", width=10, fg="white",bg='green',font=("Arial", 12), activeforeground ='black', command=handleBW)
checkInButton.pack(side=tkinter.LEFT, expand=True, pady=5)
        
button = tkinter.Button(window, text="CSV",  width=10, fg="white",bg='red',font=("Arial", 12), activeforeground ='black', command=handleCSV)
button.pack(side=tkinter.RIGHT, expand=True, pady=5)

def update_frame():
    global canvas, photo, bw, count, check_status_active, checkInButton, checkMail
    if(bw==0):
        check_status_active = 1
        checkInButton.configure(text="Check IN", bg='green')
    else:
        check_status_active = -1
        checkInButton.configure(text="Check OUT", bg='blue')
    ret, frame = video.read()
    frame = cv2.resize(frame, dsize=None, fx=1, fy=1)
    ret,frame,_,_= Recognition(ret, frame, check_status_active)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    count = count + 1
    if count % 1 == 0:
        thread = Thread(target=send_to_lable)
        thread.start()
    window.after(15, update_frame)

update_frame()

window.mainloop()

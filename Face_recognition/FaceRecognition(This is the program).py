import cv2
import numpy as np
import os
from PIL import Image
from Tkinter import *
import trainner
import sqlite3
import pickle
import tkMessageBox
import time
import sys
face_csc = cv2.CascadeClassifier('.//Haarcascade//haarcascade_frontalface_default.xml')
rec = cv2.createLBPHFaceRecognizer()
root4 = Tk()
root4.title("Face Recognition")
fr1=Frame(root4)
fr1.pack()
fr2=Frame(root4)
fr2.pack()
fr3=Frame(root4)
fr3.pack()
stvar=StringVar()
lab1=Label(fr1, text="What kind of Camera will you use ")
lab1.pack()
rad1=Radiobutton(fr2,text="Internal Camera")
rad1.grid(row=0, column=0)
rad2=Radiobutton(fr2,text="External Camera")
rad2.grid(row=0, column=1)
rad1.config(variable=stvar,value="Internal Camera")
rad2.config(variable=stvar, value="External Camera")
but1=Button(fr3, text="Start")
but1.pack()
but1.config(command=lambda : close())
def close():
    if stvar.get() == "Internal Camera":
        try:
            Prop=0
            cam = cv2.VideoCapture(0)
            while Prop < 2 :
                ret, frame = cam.read()
                Prop=Prop+1
            if ret == True:
                root4.destroy()
            elif  ret == False:
                print ret
                tkMessageBox.showerror("No Camera", "There isn't Internal Camera")
            cam.release()
        except :
            tkMessageBox.showerror("No Camera", "There isn't Internal Camera")
    elif stvar.get() == "External Camera":
        try:
            cam = cv2.VideoCapture(1)
            tf, FR = cam.read()
            cam.release()
            if tf == False:
                tkMessageBox.showerror("No Camera", "There isn't External Camera")
            else:
                root4.destroy()
        except:
            tkMessageBox.showerror("No Camera", "There isn't External Camera")
    elif stvar.get() == "":
        tkMessageBox.showerror("You didn't Choose", "Please choose The kind of Camera")


root4.mainloop()

if stvar.get() == "Internal Camera":
    cam = cv2.VideoCapture(0)
elif stvar.get() == "External Camera":
    cam = cv2.VideoCapture(1)


def InsertInform(iD, Name, Name2, Job, Age):
    conn = sqlite3.connect('FaceDataBase.db')
    cursor = conn.execute("SELECT * FROM face WHERE ID=" + str(iD))
    record = 0
    for row in cursor:
        record = 1
    if record == 1:
        tkMessageBox.showerror(title="ID is excisted", message="ID is excisted: Please select another ID")
        insertID()
    else:
        parm = (str(iD), str(Name), str(Name2), str(Job), str(Age))
        conn.execute("INSERT INTO face VALUES(?, ?, ?, ?, ?)", parm)
        conn.commit()
    conn.close()


def insertID():
    sample = 0
    root = Tk()
    root.title("Registertion ")
    l1 = Label(root, text="Insert an ID (Start with 1 after that 2 then 3 and so on):")
    l1.pack()
    entry = Entry(root)
    entry.pack()
    l2 = Label(root, text="First Name :")
    l2.pack()
    entry2 = Entry(root)
    entry2.pack()
    l3 = Label(root, text="Last Name :")
    l3.pack()
    entry3 = Entry(root)
    entry3.pack()
    l4 = Label(root, text="Your Job :")
    l4.pack()
    entry4 = Entry(root)
    entry4.pack()
    l5 = Label(root, text="Age :")
    l5.pack()
    entry5 = Entry(root)
    entry5.pack()
    bu1 = Button(root, text="Register")
    bu1.pack()
    bu1.config(command=lambda: buclick())
    def buclick():
        eID=entry.get()
        conn = sqlite3.connect('FaceDataBase.db')
        cursor = conn.execute("SELECT * FROM face WHERE ID=" + str(entry.get()))
        record = 0
        for row in cursor:
            record = 1
        if record == 1:
            tkMessageBox.showerror(title="ID is excisted", message="ID is excisted: Please select another ID")
            conn.close()
        else:
            parm = (str(entry.get()), str(entry2.get()), str( entry3.get()), str(entry4.get()), str( entry5.get()))
            conn.execute("INSERT INTO face VALUES(?, ?, ?, ?, ?)", parm)
            conn.commit()
            conn.close()
            root.destroy()
            root1 = Tk()
            root1.title("Face Recognition")
            l7 = Label(root1, text="Notice: Stop in front of camera for 2 seconds \n When you are ready Click the button ")
            l7.pack()
            b9 = Button(root1, text="Ready!")
            b9.pack()
            b9.config(command=lambda: bc())
            def bc():
                root1.destroy()
                sample = 0
                while (True):
                    ret, frame = cam.read()
                    if ret == True:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_csc.detectMultiScale(gray, 1.3, 5)
                        for (x, y, w, h) in faces:
                            sample = sample+1
                            cv2.imwrite(".//Recognizer//sample" + str(sample) + "." + str(eID) + ".jpg", gray[y: y + h, x: x + w])
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.waitKey(10)
                        cv2.imshow('Face Recognition', frame)
                        if sample == 12:
                            break
                trainner.recognize()
                cam.release()
                cv2.destroyAllWindows()
                end2 = cv2.imread('end2.png')
                cv2.imshow("Face Recognition", end2)
                cv2.waitKey(10)
                time.sleep(3)
                cv2.destroyAllWindows()
                sys.exit()
            root1.mainloop()
    root.mainloop()
try:
    rec.load('.//result//trainning_result.yml')

except:
    insertID()
    rec.load('.//result//trainning_result.yml')
font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL, 5, 1, 0, 1)
g = 0
iD = 0
sample = 0


def ShowInform(id):
    root = Tk()
    root.title("Information")
    f1 = Frame(root)
    f1.pack()
    f2 = Frame(root)
    f2.pack()
    l1 = Label(f1,text="First Name : " + profile[1])
    l1.pack()
    l2 = Label(f1, text="Last Name : " + profile[2])
    l2.pack()
    l3 = Label(f1, text="Job : " + profile[3])
    l3.pack()
    l4 = Label(f1, text="Age : " + str(profile[4]))
    l4.pack()
    bu = Button(f2,text= "close")
    bu.grid(row=0,column=0)
    bu2 = Button(f2, text="Update\nInfo")
    bu2.grid(row=0, column=2)
    bu3=Button(f2,text="Update Face\n(For hard identifing)")
    bu3.grid(row=0,column=1)
    bu3.config(command=lambda : UF())
    bu.config(command=lambda: close())
    bu2.config(command=lambda: update())
    def UF():
        root.destroy()
        root1 = Tk()
        root1.title("Face Recognition")
        l7 = Label(root1, text="Notice: Stop in front of camera for 2 seconds \n When you are ready Click the button ")
        l7.pack()
        b9 = Button(root1, text="Ready!")
        b9.pack()
        b9.config(command=lambda: bc())

        def bc():
            root1.destroy()
            sample = 0
            while (True):
                ret, frame = cam.read()
                if ret == True:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_csc.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        sample = sample+1
                        cv2.imwrite(".//Recognizer//sample" + str(sample) + "." + str(id) + ".jpg", gray[y: y + h, x: x + w])
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.waitKey(20)
                    cv2.imshow('Face Recognition', frame)
                    if sample == 12:
                        cv2.destroyAllWindows()
                        break
            trainner.recognize()
            cam.release()
            cv2.destroyAllWindows()
            end2 = cv2.imread('end2.png')
            cv2.imshow("Face Recognition", end2)
            cv2.waitKey(10)
            time.sleep(3)
            cv2.destroyAllWindows()
            sys.exit()
    def close():
        root.destroy()
    def update():
        root.destroy()
        root2 = Tk()
        root2.title("Updating Info")
        f1 = Frame(root2)
        f1.pack()
        f2 = Frame(root2)
        f2.pack()
        fE1 = Frame(root2)
        fE1.pack()
        f3 = Frame(root2)
        f3.pack()
        f4 = Frame(root2)
        f4.pack()
        fE2 = Frame(root2)
        fE2.pack()
        f5 = Frame(root2)
        f5.pack()
        f6 = Frame(root2)
        f6.pack()
        fE3 = Frame(root2)
        fE3.pack()
        f7 = Frame(root2)
        f7.pack()
        f8 = Frame(root2)
        f8.pack()
        fE4 = Frame(root2)
        fE4.pack()
        Fb = Frame(root2)
        Fb.pack()
        var = StringVar()
        var2 = StringVar()
        var3 = StringVar()
        var4 = StringVar()
        la1 = Label(f1, text="First Name :")
        la1.pack()
        ra1 = Radiobutton(f2, text="Change")
        ra1.grid(row=0, column=0)
        ra1.config(variable=var, value="Change")
        ra2 = Radiobutton(f2, text="Not change")
        ra2.grid(row=0, column=1)
        ra2.config(variable=var, value="Not change")
        e1 = Entry(fE1)
        e1.pack()
        la2 = Label(f3, text="Last Name :")
        la2.pack()
        rb1 = Radiobutton(f4, text="Change")
        rb1.grid(row=0, column=0)
        rb1.config(variable=var2, value="Change")
        rb2 = Radiobutton(f4, text="Not change")
        rb2.grid(row=0, column=1)
        rb2.config(variable=var2, value="Not change")
        e2 = Entry(fE2)
        e2.pack()
        la3 = Label(f5, text="Job :")
        la3.pack()
        rc1 = Radiobutton(f6, text="Change")
        rc1.grid(row=0, column=0)
        rc1.config(variable=var3, value="Change")
        rc2 = Radiobutton(f6, text="Not change")
        rc2.grid(row=0, column=1)
        rc2.config(variable=var3, value="Not change")
        e3 = Entry(fE3)
        e3.pack()
        la4 = Label(f7, text="Age :")
        la4.pack()
        rd1 = Radiobutton(f8, text="Change")
        rd1.grid(row=0, column=0)
        rd1.config(variable=var4, value="Change")
        rd2 = Radiobutton(f8, text="Not change")
        rd2.grid(row=0, column=1)
        rd2.config(variable=var4, value="Not change")
        e4 = Entry(fE4)
        e4.pack()
        b1 = Button(Fb, text="Confirm")
        b1.grid(row=0, column=0)
        b2 = Button(Fb, text="Close")
        b2.grid(row=0, column=1)
        b1.config(command=lambda : Update())
        b2.config(command=lambda: Close() )
        def Close():
            root2.destroy()
        def Update():

            conn = sqlite3.connect('FaceDataBase.db')
            cursor = conn.execute("SELECT * FROM face WHERE ID=" + str(id))
            record = 0
            parm=(str(e1.get()),str(id))
            parm2 = (str(e2.get()), str(id))
            parm3 = (str(e3.get()), str(id))
            parm4 = (str(e4.get()), str(id))
            for row in cursor:
                record = 1
            if record == 1:
                if var.get() == "Change":
                    conn.execute("UPDATE face SET FName=? WHERE ID=?",parm)
                if var2.get() == "Change":
                    conn.execute("UPDATE face SET LNAME=? WHERE ID=?",parm2)
                if var3.get() == "Change":
                    conn.execute("UPDATE face SET Job=? WHERE ID=?",parm3)
                if var4.get() == "Change":
                    conn.execute("UPDATE face SET Age=? WHERE ID=?",parm4)
            conn.commit()
            conn.close()
            tkMessageBox.showinfo("Face Recognition","Data is Updated Succesfully")
            root2.destroy()
        root2.mainloop()


    root.mainloop()


def RecieveName(ID):
    conn = sqlite3.connect('FaceDataBase.db')
    cursor = conn.execute("SELECT * FROM face WHERE ID="+str(ID))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile
no_gui = 0
SI = 0
s = 0
checkFace=0
id = 0
n_gui=0
confr = 0
while (True):
    ret, frame = cam.read()
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_csc.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            SI = id
            if confr == 0:
                confr= confr + 1
            else :
                conft=conf
            id, conf = rec.predict(gray[y: y + h, x: x + w])
            if conf <= 50:
                profile = RecieveName(id)
                I = profile[0]
                id = profile[1]
                if SI != id and SI != 0 and conft <= 50:
                    no_gui = 0
                if 4<no_gui <6 :
                    ShowInform(I)
                    no_gui = no_gui + 1
                if no_gui != 5:
                    if SI == id:
                        no_gui = no_gui + 1
            elif conf > 50:
                g=g+1
                if g < 40:
                    id = "Unknown"
                elif g >= 40:
                    insertID()
                    time.sleep(3)
                    g = 0
            cv2.cv.PutText(cv2.cv.fromarray(frame), str(id), (x, y + h + 30), font, 255)
        cv2.imshow("Face_recognition",frame)
    if cv2.waitKey(1) == 27 :
        break
cam.release()
cv2.destroyAllWindows()
end= cv2.imread('end.png')
cv2.imshow("Face Recognition",end)
cv2.waitKey(10)
time.sleep(5)
cv2.destroyAllWindows()

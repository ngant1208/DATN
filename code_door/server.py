import cv2
import pyodbc 
import time
import os
from tkinter import *
from tkinter import messagebox
import random
import numpy as np
# DRIVER_NAME=' SQL SERVER'
# SERVER_NAME='DESKTOP-LNGJ4BJ\SQLEXPRESS2019'
# DATABASE_NAME='face_register'
class Get_name_pass():
    def __init__(self) -> None:
        self.name=""
        self.passwd=None
    def get_name_pr(self):
        ws = Tk()
        ws.title('Register')
        ws.geometry('800x480+400+200')
        def show_inform(name):
            tk=Tk()
            tk.geometry('400x100+450+200')
            tk.title("wellcome")
            self.name = name_Tf.get()
            self.passwd=random.randrange(10000,100000)
            Label(tk,text=f'Hi! {self.name}, welcome!!! camera will open after 10 seconds').pack(pady=20)
            tk.after(3000,tk.destroy)
            ws.after(3000,ws.destroy)
            tk.eval('tk::PlaceWindow . center')
            tk.mainloop()
            
        img = PhotoImage(file="XhIeBC.png")
        label = Label(ws,image=img)
        label.place(x=0, y=0)
        Label(ws, text='Enter Name and hit Enter Key',font=50).pack(pady=20)
        name_Tf = Entry(ws,font=('Georgia 15'))
        name_Tf.focus()
        name_Tf.bind('<Return>',show_inform)
        name_Tf.pack()
        # ws.eval('tk::PlaceWindow . center')
        ws.mainloop()

class Get_face:
    def __init__(self):
        self.frame_count=5
        self.folder_output='img_output'
        self.cap=cv2.VideoCapture(0)
        self.cap.set(3,480)
        self.cap.set(4,800)
    # def write_image(self,name):
    #     #make folder 
    #     str_folder=os.path.join(self.folder_output,name)
    #     if not os.path.exists(str_folder):
    #         os.mkdir(str_folder)
    #         print("Directory " , str_folder ,  " Created ")
    #     else:    
    #         print("Directory " , str_folder ,  " already exists")
        
    #     #if os.pardir()
        
    #     #open and write
    #     pass
    # def clear_data(self,name):
    #     import shutil
    #     folder = os.path.join(self.folder_output,name)
    #     # folder = 'img_output'
    #     for filename in os.listdir(folder):
    #         file_path = os.path.join(folder, filename)
    #         try:
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.unlink(file_path)
    #             elif os.path.isdir(file_path):
    #                 shutil.rmtree(file_path)
    #         except Exception as e:
    #             print('Failed to delete %s. Reason: %s' % (file_path, e))
    #     print('Done.')
        
    def get_face_register(self,name,passwd):
        count=0
        pre_time=time.time()
        cnxn=Connection()
        cursor=cnxn.cnn.cursor()
        cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Customer' and xtype='U') CREATE TABLE Customer (Img varbinary(MAX), Name TEXT NOT NULL, Password INT NOT NULL)")
        # cursor.execute("CREATE TABLE IF NOT EXITS Customer (img VARBINARY(MAX) NOT NULL, Name TEXT NOT NULL, Password INT NOT NULL);")
        sql_insert_blob_query = """INSERT INTO Customer(Img,Name,Password) VALUES (?,?, ?)"""
        while 1:
            ret,frame=self.cap.read()
            if count==self.frame_count+1:
                cnxn.stop_connection()
                str="Done!Thanks."
                
            elif time.time() > pre_time+2:
                count+=1
                # xư lý anh truoc khi luu
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                img_encode = cv2.imencode('.jpg', small_frame)[1]
                data_encode = np.array(img_encode)
                byte_encode = data_encode.tobytes()
                # end 
                cursor.execute(sql_insert_blob_query,byte_encode,name,passwd)
                cursor.commit()
                print("Image and file inserted successfully as a BLOB into python_employee table")
                # str1=f'{name}_{count}.jpg'
                # cv2.imwrite(os.path.join(self.folder_output,name,str1),frame)
                pre_time=time.time()
            str=f'Get picture {count}'
            cv2.rectangle(frame, (10, 30), (10 + 250, 30 + 60), (0,0,0), -1)
            cv2.putText(frame, str, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("test",frame)
            if cv2.waitKey(1)&0xFF==ord('q') or count>=self.frame_count+1:
                break
        self.cap.release()
        cv2.destroyAllWindows()


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
        return binaryData
class Connection:
    def __init__(self) -> None:
        self.connection_string = (
    r'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-LNGJ4BJ\SQLEXPRESS2019;'
    r'DATABASE=face_register;'
    r'Trusted_Connection=yes;')
        self.cnn=pyodbc.connect(self.connection_string)
    def stop_connection(self):
        self.cnn.close()
    def clear_all(self):
        cursor=self.cnn.cursor()
        cursor.execute("DELETE FROM Customer")
        cursor.commit()
        cursor.close()
        self.cnn.close()
        
    def write_database(self,frame,name):
        try:
            cnxn = pyodbc.connect(self.connection_string)
            cnxn.execute("CREATE TABLE if not exists Camera (img LONGBLOB, Name TEXT);")
            cnxn.execute("INSERT INTO Camera (img,name) VALUES %s %s",frame,name)
            # print(cnxn)
            cnxn.commit()
            print("Image and file inserted successfully as a BLOB into python_employee table")
        except pyodbc.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))

        finally:
            cnxn.close()
            print("MySQL connection is closed")
    def readBLOB(self,emp_id, photo, bioData):
        print("Reading BLOB data from python_employee table")

        try:
            cnxn = pyodbc.connect(self.connection_string)

            cursor = cnxn.cursor()
            sql_fetch_blob_query = """SELECT * from python_employee where id = %s"""

            cursor.execute(sql_fetch_blob_query, (emp_id,))
            record = cursor.fetchall()
            for row in record:
                print("Id = ", row[0], )
                print("Name = ", row[1])
                image = row[2]
                file = row[3]
                print("Storing employee image and bio-data on disk \n")
                
        except pyodbc.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))

        finally:
            if cnxn.is_connected():
                cursor.close()
                cnxn.close()
                print("MySQL connection is closed")

class App():
    def __init__(self) -> None:
        pass
    def run():
        # get_name_pr()
        t=Get_face()
        t.get_face_regis()
        
t=Get_name_pass()
t.get_name_pr()
# print(t.name,t.passwd)
t1=Get_face()
t1.get_face_register(t.name,t.passwd)
# t1.write_image(t.name)

# t1.get_face_regis('nga')
# t1.clear_data('nga')
# cnn=Connection()
# cnn.write_database()
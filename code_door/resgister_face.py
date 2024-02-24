import cv2
import time
import pyodbc
def store(img):
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=USXXX00345,67800;"
            "Database=DB02;"
            "UID=Alex;"
            "PWD=Alex123;")
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    # cursor.execute("SELECT TOP(100) * FROM associates")
    # first alter the table, adding a column
    cursor.execute("ALTER TABLE associates " +
               "ADD fullName VARCHAR(20)")
    # now update that column to contain firstName + lastName
    cursor.execute("UPDATE associate " +
               "SET fullName = firstName + " " + lastName")

def get_face():
    # get 5 picture
    cap=cv2.VideoCapture(0)
    ret,frame=cap.read()

    cv2.imshow("Register",frame)
import cv2
import pyodbc 

str1="Nhan_vien"


connection_string = (
    r'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-LNGJ4BJ\SQLEXPRESS2019;'
    r'DATABASE=Nhan_vien;'
    r'Trusted_Connection=yes;')
class Connection:
    def __init__(self,dtb) -> None:
        self.cnxn_str = ("DRIVER={{SQL Server}};"
            "SERVER=DESKTOP-LNGJ4BJ\SQLEXPRESS2019;"
            "Database={0};"
            "Trusted_Connection=yes;".format(dtb))
        self.connection_string = (
            r'DRIVER={SQL Server};'
            r'SERVER=DESKTOP-LNGJ4BJ\SQLEXPRESS2019;'
            r'DATABASE=nhanvien;'
            r'Trusted_Connection=yes;')
        self.cnn=pyodbc.connect(self.cnxn_str)
        self.cursor=self.cnn.cursor()
    def stop_connection(self):
        self.cursor.close()
        self.cnn.close()
        print("MySQL connection is closed")

    def run_command(self,exe_cm):
        self.cursor.execute(exe_cm)
        self.cursor.commit()


        
    def clear_all(self):
        cursor=self.cnn.cursor()
        cursor.execute("DELETE FROM Customer")
        cursor.commit()
        cursor.close()
        self.cnn.close()
        
    def write_database(self,string_exec,frame,name):
        try:
            self.cursor.execute(string_exec,frame,name)
            self.cursor.commit()
           
        except pyodbc.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))
            
    def readBLOB(self,emp_id, photo, bioData):
        print("Reading BLOB data from python_employee table")

        try:
            cnxn = pyodbc.connect(self.connection_string)

            cursor = cnxn.cursor()
            sql_fetch_blob_query = "SELECT * from python_employee where id = %s"

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

# t=Connection(str1)
# t.stop_connection()
# t.clear_all()
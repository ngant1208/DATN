# # Echo server program
# import socket

# HOST = ''                 # Symbolic name meaning all available interfaces
# PORT = 50007              # Arbitrary non-privileged port
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen(1)
#     while True:
#         print("Waiting for connection")
#         conn, addr = s.accept()
#         with conn:
#             print('Connected by', addr)
#             while True:
#                 data = conn.recv(1024)
#                 if not data: break
#                 conn.sendall(data)
import pyodbc
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(file_name):
    print("Reading BLOB data from python_employee table")
    connection_string = (
    r'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-LNGJ4BJ\SQLEXPRESS2019;'
    r'DATABASE=face_register;'
    r'Trusted_Connection=yes;')

    try:
        
        cnn=pyodbc.connect(connection_string)

        cursor = cnn.cursor()
        sql_fetch_blob_query = """SELECT TOP 1* from Customer """

        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            
            image = row[0]
            # file = row[3]
            print("name = ", row[1], )
            print("pss = ", row[2])
            print("Storing employee image and bio-data on disk \n")
            write_file(image,file_name)

    except pyodbc.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
            cursor.close()
            cnn.close()
            print("MySQL connection is closed")
readBLOB("nga_1.jpg")
# readBLOB(2, "D:\Python\Articles\my_SQL\query_output\scott_photo.png",
#          "D:\Python\Articles\my_SQL\query_output\scott_bioData.txt")
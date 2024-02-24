import cv2
import pickle
import face_recognition
import numpy as np
from tkinter import messagebox,simpledialog
import pygame
import RPi.GPIO as GPIO
import time
# chose pin
GPIO.setmode(GPIO.BOARD)
# for keypad
L1 = 10
L2 = 12
L3 = 16
L4 = 18

C1 = 7
C2 = 11
C3 = 13
C4 = 15
# for relay
LD=29
# for buttom
# 1 chan nối vao 3.3V(pin 1) 1 chan ni voi GPIO(pin 8)
PB=8
# sensor
SR=31
# door unlock 

# Get a reference to webcam #0 (the default one)#-1 for pi
def Recog_face(img,data):
    sign_face=False
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Find all the faces and face encodings in the current frame of video
    name = "Unknown"
    face_locations =face_recognition .face_locations(rgb_small_frame,model="cnn")
    if len(face_locations)!=0:
        sign_face=True
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # face_names = []
        for face_encoding in face_encodings:
                face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
                best_match_index = np.argmin(face_distances)
                if face_distances[best_match_index]<=0.6:
                    name=data["names"][best_match_index]
    return name,sign_face
def sensor():
    # lock
    GPIO.setup(SR,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    if GPIO.input(SR) == GPIO.LOW:
        return True
    # unlock
    else:
        return False

def open_door(img,sound,data):
    # 1 pin
    # sign_face=recog_face() or press buttom
     # Use physical pin numbering
    sign_door=check_buttom() or Recog_face(img,data)
    GPIO.setup(LD,GPIO.OUT) 
    if sign_door:
        # GPIO.setup(LD,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
        time.sleep(5)
        if sensor():
            # play sound for not open door
            speaker(sound)
        else:
            GPIO.setup(LD,GPIO.OUT,pull_up_down=GPIO.PUD_UP)


def speaker(path_file_sound):
    # change output default from HDMI to audio jack to use jack 3.5 on raspi
    pygame.mixer.init()
    pygame.mixer.music.load(path_file_sound)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
def check_buttom():
    # open door from inside
    # a buttom
    # chân đầu vào sẽ ở mức thấp (0V) khi không nhấn nút. Khi nhấn nút, nó sẽ kết nối chân với 3,3V và thay đổi trạng thái thành cao (3,3V)
    # GPIO.setwarnings(False) # Ignore warning for now
    # Use physical pin numbering
    GPIO.setup(PB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True: # Run forever
        if GPIO.input(PB) == GPIO.HIGH:
            # for test
            # print("Button was pushed!") 
            return True
        else:
            return False

#keypad
def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1 or GPIO.input(C2) == 1 or GPIO.input(C3) == 1 or GPIO.input(C4) == 1:
        if(GPIO.input(C1) == 1):
            return(characters[0])
        if(GPIO.input(C2) == 1):
            return(characters[1])
        if(GPIO.input(C3) == 1):
            return(characters[2])
        if(GPIO.input(C4) == 1):
            return(characters[3])
    else:
        return None
    GPIO.output(line, GPIO.LOW)
def get_key():
    s=None
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)
    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    L=[L1,L2,L3,L4]
    key=[["1","2","3","A"],["4","5","6","B"],["7","8","9","C"],["*","0","#","D"]]
    try:
        while True:
            for i in range(4):
                s=readLine(L[i],key[i])
            # readLine(L1, ["1","2","3","A"])
            # readLine(L2, ["4","5","6","B"])
            # readLine(L3, ["7","8","9","C"])
            # readLine(L4, ["*","0","#","D"])
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
    return s

# init

video_capture = cv2.VideoCapture(0)
width  =video_capture.get(3) 
height = video_capture.get(4)  
y_start=int(1/2*(height-300))
x_start=int(1/2*(width-300))
data = pickle.loads(open("end.pickle", "rb").read())
count=0
no=0
psw=12345
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    cv2.rectangle(frame,(x_start,y_start), (x_start+300,y_start+300), (0, 0, 255),2)
    cv2.putText(frame,'Put your face in retangle',(x_start-30,y_start-30),cv2.FONT_HERSHEY_DUPLEX,1.0,(255,255,0),1)
    cv2.imshow('Video', frame)
    name="Unknown"
    count=count+1
    # print(count)
    if count%20==0:
        img=frame[y_start:y_start+300,x_start:x_start+300]
        name=Recog_face(img,data)
        if name=="Unknown":
            no+=1
    if count==100:
        if no/(6-no)>=1:
            name="Unknown"
        if name!="Unknown":
            info = messagebox.showinfo('Found a matching face.\nDOOR IS OPENING')
            # open door
            open_door()
            break
        else:
            info=messagebox.showinfo('No found a matching face.\nTRY AGAIN OR ENTER *  FOR PASSWORD')
            # get key *
            if get_key()=="*":
                integer_value = simpledialog.askinteger('Dialog Title', 'ENTER YOUR PASSWORD', minvalue=0, maxvalue=1000)
                if integer_value==psw:
                    info=messagebox.showinfo('CORRECT PASSWORD!OPENING DOOR...')
                    open_door()
                    break

            # print(integer_value)
            #check password

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

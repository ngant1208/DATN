import cv2
from multiprocessing import Process,Queue,Manager,Event
import time
from tkinter import Tk,Label
import face_recognition 
import pickle
import numpy as np
import pygame
import RPi.GPIO as GPIO
import time
import keypad

def clear(q):
    if not q.empty():
        while True:
            q.get_nowait()
            if q.empty():
                break
            
def capture(Gloabl,e_keypad,e_unlock,q):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(-1)
    video_capture.set(3,800)
    video_capture.set(4,480)
    count=0
    #print("starting...")
    while not Gloabl.is_exit:
        e_keypad.wait()
        ret, frame = video_capture.read()
        count+=1
        if count%60==0 and e_unlock.is_set():
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            q.put(small_frame)
            count=0
        cv2.imshow("VIDEO STREAM",frame)
            # print(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Global.is_exit = True
            break
    # Release webcam
    video_capture.release()
    cv2.destroyAllWindows()
def process(Global,q,e_keypad,e_unlock):
    data=pickle.loads(open("encodings.pickle", "rb").read())
    while not Global.is_exit:
        e_keypad.wait()
        e_unlock.wait()
        name = "Unknown"
        if not q.empty():
            small_frame = q.get()
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations =face_recognition.face_locations(rgb_small_frame,model="cnn")
            if len(face_locations)>0:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                for face_encoding in face_encodings:
                    face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if face_distances[best_match_index]<=0.6:
                            name=data["names"][best_match_index]
                            Global.name=name
                            clear(q)
                            #print(Global.name)
                            
class Main_process:
    def __init__(self) -> None:
        self.LD=29
        self.PB=8
        self.SR=31
        self.sound_fg="/home/pi/fg.wav"
        self.sound_op="/home/pi/Desktop/DATN/door.wav"
        self.sound_wrg="/home/pi/wrong_face.wav"
        self.pre_process()
    def pre_process(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.SR,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.PB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LD,GPIO.OUT)

                    
    def sensor(self):
        # lock
        #GPIO.setup(SR,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        if GPIO.input(self.SR) == GPIO.LOW:
            return False
        # unlock
        else:
            return True
    
    def speaker(self,path_file_sound):
        # change output default from HDMI to audio jack to use jack 3.5 on raspi
        pygame.mixer.init()
        pygame.mixer.music.load(path_file_sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def open_door(self,e_unlock):
        #print("Opening door.....")
        e_unlock.clear()
        GPIO.output(self.LD,0)
        self.speaker(self.sound_op)
        time.sleep(2)
        GPIO.output(self.LD,1)
        time.sleep(2)
        while self.sensor():
            self.speaker(self.sound_fg)
            time.sleep(2)
        e_unlock.set()
    def run(self,Global,e_unlock):
        while not Global.is_exit:
            GPIO.output(self.LD,1)
            if GPIO.input(self.PB) == GPIO.LOW or Global.name!="Unknown" or Global.unlock:
                self.open_door(e_unlock)
                Global.name="Unknown"
                Global.unlock=False
            
if __name__ == '__main__':
    # Global variables
    Global = Manager().Namespace()
    que = Queue()
    evt_keypad=Event()
    evt_unlock=Event()
    evt_keypad.set()
    evt_unlock.set()
    Global.is_exit = False
    Global.name='Unknown'
    Global.hv_face=False
    Global.unlock=False
    main_process=Main_process()
    k=keypad.Keypad()
    p=Process(target=capture, args=(Global,evt_keypad,evt_unlock,que,))
    p1=Process(target=process,args=(Global,que,evt_keypad,evt_unlock,))
    p2=Process(target=main_process.run,args=(Global,evt_unlock,))
    p3=Process(target=k.run,args=(evt_keypad,Global,))
    p.start()
    p1.start()
    p2.start()
    p3.start()
    p.join()
    p.terminate()
    p1.terminate()
    p2.terminate()
    p3.terminate()
    GPIO.cleanup()
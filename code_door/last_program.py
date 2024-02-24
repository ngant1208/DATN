import RPi.GPIO as GPIO
import time
from tkinter import *
import cv2
from multiprocessing import Process,Queue,Manager,Event
import time
from tkinter import *
import numpy
import pickle
import numpy as np
import face_recognition 

#GPIO Setup
GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)
#set gpio for key pad


# video_stream
class video_stream():
    def __init__(self,evt_stop,queu_frame) -> None:
        self.even_stop=evt_stop
        self.que_frame=queu_frame
    def capture(self):
        video_capture = cv2.VideoCapture(0)
        count=0
        while True:
            self.even_stop.wait()
            ret, frame = video_capture.read()
            count+=1
            if count%60==0:
                self.que_frame.put(frame)
            cv2.imshow("test",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release webcam
        video_capture.release()
        cv2.destroyAllWindows()
    def run(self) -> None:
        self.capture()

class Face_process():
    def __init__(self,event_stop,queue_get_frame):
         self.data=pickle.loads(open("end.pickle", "rb").read())
         self.name="Unknown"
         self.hv_face=False
         self.event_stopped=event_stop
         self.que_face=queue_get_frame

    def recogniton(self):
        while True:
            self.event_stopped.wait()
            self.name = "Unknown"
            if not self.que_face.empty():
                frame_process = self.que_face.get()
                small_frame = cv2.resize(frame_process, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations =face_recognition.face_locations(rgb_small_frame,model="cnn")
                if len(face_locations)>0:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    for face_encoding in face_encodings:
                        face_distances = face_recognition.face_distance(self.data["encodings"], face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if face_distances[best_match_index]<=0.6:
                                name=self.data["names"][best_match_index]
                                self.name=name

class Main_process:
    def __init__(Global,self) -> None:
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
        if GPIO.input(self.SR) == GPIO.LOW:
            return False
        # unlock
        else:
            return True
    
    def speaker(self,path_file_sound):
        pygame.mixer.init()
        pygame.mixer.music.load(path_file_sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    def open_door(self):
        GPIO.output(self.LD,0)
        self.speaker(self.sound_op)
        time.sleep(5)
        GPIO.output(self.LD,1)
        time.sleep(5)
        if self.sensor():
            self.speaker(self.sound_fg)
    def run(self,Global):
        while True:
            GPIO.output(self.LD,1)
            if GPIO.input(self.PB) == GPIO.LOW or Global.name!="Unknown":
                self.open_door(self.sound_fg,self.sound_op)
            if Global.is_exit:
                GPIO.cleanup()
                break

def main():
   # Global variables
    Global = Manager().Namespace()
    que = Queue()
    evt=Event()
    ev1=Event()
    ev1.set()
    Global.is_exit = False
    Global.name='Unknown'
    Global.hv_face=False
    main_process=Main_process()
    p1=video_stream()
    p2=Face_process()
    pc1=Process(target=p1.capture,args=())
    p=Process(target=capture, args=(Global,ev1,que,))
    p1=Process(target=process,args=(Global,que,evt,))
    p2=Process(target=main_process.speaker,args=(main_process.sound_op))
    p.start()
    p1.start()    
    p.join()
    p1.join()
   #not done 

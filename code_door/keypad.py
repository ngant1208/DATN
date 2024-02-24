import RPi.GPIO as GPIO
from tkinter import *
import time
from threading import Thread,Event
import tkinter.messagebox as messagebox
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
class Keypad():
    def __init__(self) -> None:
        self.COL = [11,13,15,19]
        self.ROW = [16,22,24,26]
        self.MATRIX =   [["1","2","3","A"],
              ["4","5","6","B"],
              ["7","8","9","C"],
              ["*","0","#","D"]]

        self.result=""
        self.pre_setup()
        self.stop=False
        self.event=Event()
        self.event_stop_all=False
        self.psswd=" 12345"
        self.try_again=False
    def message(self,text_mess):
        top = Tk()
        top.title('Welcome')
        top.geometry('410x80+220+250')
        #top.eval('tk::PlaceWindow . center')
        Label(top, text=text_mess).pack(pady=20)
        top.after(1000, top.destroy)
        top.mainloop()
    def scan(self,Global):
        self.pre_setup()
        self.result=" "
        self.event_stop_all=False
        while True:
            if self.event_stop_all==True:
                GPIO.cleanup()
                break
            self.try_again=False
            self.get_pss=False
            for j in range(4):
                GPIO.output(self.COL[j], 0)
                for i in range(4):
                    if GPIO.input(self.ROW[i]) == 0:
                        time.sleep(0.1)
                        self.event.set()
                        self.result = self.result + self.MATRIX[i][j]
                        #print(self.result)
                        while(GPIO.input(self.ROW[i]) == 0):
                            time.sleep(0.1)
                GPIO.output(self.COL[j], 1)
                
                if len(self.result) >=6:
                    self.event.clear()
                    if self.result==self.psswd:
                        tx="PASSWORD IS CORRECT.DOOR IS OPENING..."
                        self.message(tx)
                        Global.unlock=True
                        time.sleep(0.5)
                        self.event_stop_all=True
                        break
                    else:
                        tx="PASSWORD IS WRONG. PRESS D TO EXIT OR TRY AGAIN"
                        self.message(tx)
                        self.try_again=True
                        time_start=time.time()
                        while time.time() < time_start + 3:
                            GPIO.output(self.COL[3], 0)
                            if GPIO.input(self.ROW[3]) == 0:
                                self.event_stop_all=True
                                GPIO.output(self.COL[0],1)
                                break
                    self.result=" "
                
    def insert_slow(self,pr,widget):
        if self.event_stop_all:
            pr.destroy()
        if self.event.is_set():
            widget.insert("end","  * ")
            widget.xview("end")
            self.event.clear()
        if self.try_again:
            widget.delete(0, END)
            self.try_again=False
        widget.after(100, self.insert_slow, pr,widget)
    def pre_setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        for j in range(4):
            GPIO.setup(self.COL[j], GPIO.OUT)
            GPIO.output(self.COL[j], 1)
        for i in range(4):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def get_change(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.output(self.COL[0], 0)
        if GPIO.input(self.ROW[3]) == 0:
            GPIO.output(self.COL[0],1)
            return True
        else:
            return False
    def display_scanning(self):
        root=Tk()
        root.geometry('800x480')
        img = PhotoImage(file="nmasK1.png")
        label = Label(root,image=img)
        label.place(x=0, y=0)

        f=Frame(root,bd=2,relief=RAISED,height=500,width=500)
        f.pack(pady=80)
        label=Label(f,text=" ENTER YOUR PASSWORD ",font=50)
        label.pack(pady=10)
        label1=Label(f,text=" SCANNING... ",font=20)
        label1.pack(pady=10)
        entry = Entry(width=10, font=('Georgia 20'))
        entry.pack()
        self.insert_slow(root,entry)
        root.mainloop()
    def run(self,evt_keypad,Global):
        while not Global.is_exit:
            if self.get_change():
                evt_keypad.clear()
                time.sleep(0.5)
                t1=Thread(target=self.display_scanning)
                t2=Thread(target=self.scan,args=(Global,))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                evt_keypad.set()
                GPIO.cleanup()
            

            
'''class gl:
    def __init__(self):
        gl.unlock=False
e=Event()
k=Keypad()
k.run(e,gl)'''

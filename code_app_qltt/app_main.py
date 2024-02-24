import tkinter as tk
from tkinter import messagebox
from connection import Connection
import PIL.Image, PIL.ImageTk
import cv2
formal_font=("Microsoft Yahei UI Light",13,"normal")
font_cambria=("Cambria",15,"bold")
cap1=cv2.VideoCapture(0)
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self,*args, **kwargs)
        self.geometry("800x450")
        self.title("HỆ THỐNG QUẢN LÝ THÔNG TIN")
        # creating a container
        container = tk.Frame(self)
        # container.grid(columnspan=6,rowspan=6)

        self.canvas = tk.Canvas(self, width=400, height=300)
        # self.canvas.place(x=35,y=80)
        # tk.Canvas.itemconfigure(self.canvas, state='hidden')


        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {} 
        for F in (LoginPage,StartPage2,Room,Check_IN,Check_OUT,Face_register):
  
            frame = F(container, self)
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def creat_canvas(self):
        self.canvas=tk.Canvas(self, width=400, height=300)
    def delete(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

    def show_cv(self):
        self.canvas.place(x=35,y=80)
        # self.canvas.itemconfigure(id, state='hidden')

class LoginPage(tk.Frame):
    #Đăng nhập
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        # hình nền
        self.controller_l=controller
        logo = tk.PhotoImage(file="Beach1.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)
        # khối đăng nhập
        # username
        # lb1=tk.Label(self,text="ID USER",fg='black',font=formal_font).place(x=260,y=150)
        self.et1=tk.Entry(self,font=formal_font,width=25,bd=0)
        self.et1.insert(0,"Enter your username")
        self.et1.place(x=300,y=150)
        self.et1.bind("<FocusIn>", self.delete_name)
        tk.Frame(self,width=228,height=2,bg='#375454').place(x=300,y=175)

        self.et2=tk.Entry(self,font=formal_font,width=25,bd=0)
        self.et2.insert(0,"Enter your password")
        self.et2.place(x=300,y=200)
        self.et2.bind("<FocusIn>", self.delete_pss)
        tk.Frame(self,width=228,height=2,bg='#375454').place(x=300,y=225)

        bt=tk.Button(self,text='LOGIN',bg="#375454",fg='white',font=("Microsoft Yahei UI Light",15,"normal"),width=10,
                    command = lambda : self.check_login()).place(x=350,y=250)


    def delete_name(self,e):
        if self.et1.get()=='Enter your username':
            self.et1.delete(0,"end")
    def delete_pss(self,e):
        if self.et2.get()=='Enter your password':
            self.et2.delete(0,"end")
        self.et2.config(show="*")

    def check_login(self):
        cnn=Connection(dtb="Nhan_vien")
        str_cm='SELECT * FROM ttnv WHERE MaNV=? AND Pwd=?'
        MaNV=self.et1.get()
        pss=self.et2.get()
        # print(MaNV," ",pss)
        if MaNV=='' or pss=='':
            messagebox.showerror('Error',"Fill the empty field!!!")
        else:
            cnn.cursor.execute(str_cm,MaNV,pss)
            # record=cnn.cursor.fetchall()
            if cnn.cursor.fetchone():
                cnn.stop_connection()
                self.controller_l.show_frame(StartPage2)
                
            else:
                messagebox.showerror(title="Inform",message="USERNAME hoặc PASSWORD sai.Mời nhập lại.")

        # cnn.cursor.execute(str_cm,MaNV)
        # record=cnn.cursor.fetchall()
        # for row in record:
        #     print(row[0])
        #     # print("Name = ", row[1])
        #     print(row[3])
        #     # cnn.stop_connection()
        #     if row[3]!=pss or row[0]!=MaNV:
        #         messagebox.showerror(title="Inform",message="USERNAME hoặc PASSWORD sai.Mời nhập lại.")
        #     else:
        #         cnn.stop_connection()


class StartPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #hình nền
        logo = tk.PhotoImage(file="option.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)

        # khoi xu ly thoat dang nhap
        self.controller_op=controller
        self.pr=parent

        self.photo1 = tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\user.png")
        self.photoimage1 = self.photo1.subsample(2, 2)
        tk.Button(self,image=self.photoimage1,bd=0,command=lambda:controller.show_frame(LoginPage)).place(x=16,y=4)
        
        # khoi xem thong tin phong
        self.pt2=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\ttp.png")
        # self.ptm2 = self.pt2.subsample(2, 2)
        tb1=tk.Button(self,background="#ffffff",bd=0,image=self.pt2,command=lambda:controller.show_frame(Room)).place(x=253,y=110)

        # khoi them tt
        self.pt3=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\ttchekin.png")
        tb2=tk.Button(self,background="#ffffff",bd=0,image=self.pt3,command=lambda:controller.show_frame(Check_IN)).place(x=440,y=110)

        # khoi dky khuon mat
        self.pt4=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\dky.png")
        tb4=tk.Button(self,background="#ffffff",bd=0,image=self.pt4,command=lambda:self.show_face()).place(x=253,y=270)

        # check-out
        self.pt5=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\ttchout.png")
        tb5=tk.Button(self,background="#ffffff",bd=0,image=self.pt5,command=lambda:controller.show_frame(Check_OUT)).place(x=440,y=270)

    def show_face(self):
        cap1=cv2.VideoCapture(0)
        self.controller_op.show_frame(Face_register)
class Room(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #hình nền
        logo = tk.PhotoImage(file="xemphong1.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)

        # back buttom
        
        self.tt1=True
        self.color1="#20AA23"
        # tung phong
        # self.check_status()
        self.controller_back=controller
        bt1=tk.Button(self,text="BACK",font=font_cambria,bg="#375454",fg='white',width=6,height=1,command=lambda:controller.show_frame(StartPage2)).place(x=15,y=405)
        
        self.rl=tk.PhotoImage(file=r"E:\TAI LIEU\năm 4\Face_DATN\imgs\sm.png")
        bt2=tk.Button(self,bd=0,image=self.rl,command=lambda:self.check_status()).place(x=0,y=0)
        # tang 1
        # phong 101
        self.f101=tk.Frame(self,bg=self.color1,width=112,height=97)
        self.f101.place(x=135,y=112)
        self.lb101=tk.Label(self,text="Phòng 101",font=("Cambria",15,"bold"),bg=self.color1,fg='white')
        self.lb101.place(x=140,y=115)
        self.cus101=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\small_cus.png")
        bt101=tk.Button(self,bd=0,image=self.cus101,command=lambda:self.show_infokh()).place(x=165,y=151)

        # phong 101
        tk.Frame(self,bg="#DE1616",width=112,height=97).place(x=254,y=112)
        lb102=tk.Label(self,text="Phòng 102",font=("Cambria",15,"bold"),bg="#DE1616",fg='white').place(x=260,y=115)
        self.cus102=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\small_cus.png")
        bt101=tk.Button(self,bd=0,image=self.cus102,command = lambda :self.show_infor()).place(x=285,y=151)

    def show_infor(self):
        messagebox.showinfo(title="Information",message="Ten:NGUYEN VAN A\nNgaythue:29/01/2023\nNgayftra:31/09/2023")

        # phong103
        # tk.Frame(self,bg="#20AA23",width=112,height=97).place(x=254,y=112)
        # lb102=tk.Label(self,text="Phòng 102",font=("Cambria",15,"bold")).place(x=260,y=115)
        # self.cus102=tk.PhotoImage(file = r"E:\TAI LIEU\năm 4\Face_DATN\imgs\small_cus.png")
        # bt101=tk.Button(self,bd=0,image=self.cus102).place(x=285,y=151)

    def show_infokh(self):
        cnn=Connection(dtb="R101")
        str_cm='SELECT * from ttkh'
        cnn.cursor.execute(str_cm)
        record=cnn.cursor.fetchone()
        str=f''
        if record:
            name=record[0]
            nt=record[5]
            nr=record[6]
            str=f'Họ tên:{name}\nNgaythue:{nt}\nNgayftra:{nr}'

        else:
            str="Phòng trống"
        messagebox.showinfo(title="Information",message=str)

    def check_status(self):
        cnn=Connection(dtb="R101")
        str_cm='SELECT Trangthai from ttphong'
        cnn.cursor.execute(str_cm)
        record=cnn.cursor.fetchone()
        self.tt = record
        
        if self.tt[0]:
            self.color1="#20AA23"
        else:
            self.color1="#DE1616"
        cnn.stop_connection()
        # self.color1="#DE1616"
        self.f101.config(bg=self.color1)
        self.lb101.config(bg=self.color1)
class Check_IN(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #hình nền
        logo = tk.PhotoImage(file="checkin.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)

        # khoi tt
        tk.Label(self,text="Số phòng",font=("Cambria",13,"bold"),bg="#ffffff").place(x=36,y=90)
        self.et1=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et1.place(x=120,y=90)
        # tuoi
        tk.Label(self,text="Họ Tên",font=("Cambria",13,"bold"),bg="#ffffff").place(x=36,y=150)
        self.et2=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et2.place(x=120,y=150)
        
        # gioi tính
        tk.Label(self,text="Ngày Sinh",font=("Cambria",13,"bold"),bg="#ffffff").place(x=36,y=210)
        self.et3=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et3.place(x=120,y=210)
        # tk.Frame(self,width=228,height=2,bg='#375454').place(x=100,y=235)

        tk.Label(self,text="Giới tính",font=("Cambria",13,"bold"),bg="#ffffff").place(x=36,y=270)
        self.et4=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et4.place(x=120,y=270)
        # sdt
        tk.Label(self,text="CCCD",font=("Cambria",13,"bold"),bg="#ffffff").place(x=430,y=90)
        self.et5=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et5.place(x=500,y=90)

        tk.Label(self,text="SDT",font=("Cambria",13,"bold"),bg="#ffffff").place(x=430,y=150)
        self.et6=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et6.place(x=500,y=150)

        tk.Label(self,text="Ngày Thuê",font=("Cambria",13,"bold"),bg="#ffffff").place(x=410,y=210)
        self.et7=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et7.place(x=500,y=210)

        tk.Label(self,text="Ngày Trả",font=("Cambria",13,"bold"),bg="#ffffff").place(x=410,y=270)
        self.et8=tk.Entry(self,font=font_cambria,width=20,highlightthickness=2,highlightbackground="#375454")
        self.et8.place(x=500,y=270)

        # lưu buttom
        self.bt_save=tk.Button(self,text="SAVE",font=font_cambria,bg="#375454",fg='white',width=10,command=lambda:self.save_kh()).place(x=620,y=350)
        # back
        self.bt_back=tk.Button(self,text="BACK",font=font_cambria,bg="#375454",fg='white',width=10,command=lambda:controller.show_frame(StartPage2)).place(x=50,y=350)
        self.empty=False
    def save_kh(self):
        # Rom101
        sp=self.et1.get()
        ht=self.et2.get()
        ns=self.et3.get()
        gt=self.et4.get()
        cccd=self.et5.get()
        sdt=self.et6.get()
        nth=self.et7.get()
        nt=self.et8.get()
        for chidren in self.winfo_children():
            if isinstance(chidren, tk.Entry):
                if chidren.get()=="":
                    messagebox.showwarning(title="Warning",message="Fill all blank")
                    self.empty=True
                    break
                else:
                    self.empty=False
        if not self.empty:
            val=(ht,ns,gt,cccd,sdt,nth,nt)
            cnn=Connection(dtb=sp)
            str_cm='INSERT INTO ttkh (TenKH,Ngaysinh,Gioitinh,CCCD,SDT,Ngaythue,Ngaytra) values(?,?,?,?,?,?,?)'
            cnn.cursor.execute(str_cm,val)
            cnn.cursor.commit()
            str_cm='''UPDATE ttphong SET  Trangthai= 0 WHERE Sophong=R101'''
            cnn.cursor.commit()
            cnn.stop_connection()

        for chidren in self.winfo_children():
            if isinstance(chidren, tk.Entry):
                chidren.delete(0,"end")
        
        cnn=Connection(dtb=sp)
        cnn.cursor.execute ("UPDATE ttphong SET Trangthai=? WHERE Sophong=?" ,(False,sp))
        cnn.cursor.commit()
        cnn.stop_connection()

class Check_OUT(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #hình nền
        logo = tk.PhotoImage(file="checkout.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)
        self.ctr=controller

        self.lb1=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lb1.place(x=280,y=110) 
        self.lbnopers=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lbnopers.place(x=200,y=120) 


        self.lbname=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lbname.place(x=140,y=150) 

        self.lbcccd=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lbcccd.place(x=140,y=180) 

        self.lbnd=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lbnd.place(x=450,y=150)


        self.lbnr=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.lbnr.place(x=450,y=180)

        self.cost=tk.Label(self,text="",font=font_cambria,bg="#ffffff")
        self.cost.place(x=140,y=250)
        
        self.et1=tk.Entry(self,width=8,bd=0,font=("Cambria",18,"bold"))
        self.et1.bind('<Return>', self.Search)
        self.et1.place(x=320,y=68)
        
        self.bt_save=tk.Button(self,text="DELETE",font=font_cambria,bg="#375454",fg='white',width=10,command=lambda:self.deletekh()).place(x=640,y=400)
        # back
        self.bt_back=tk.Button(self,text="BACK",font=font_cambria,bg="#375454",fg='white',width=10,command=lambda:self.update()).place(x=20,y=400)


    def Search(self, event):
        room=self.et1.get()
        if room=="":
            messagebox.showwarning(title="Warning",message="Fill in the search")
        else:
            str=f'Thông tin khách hàng {room}'
            cnn=Connection(dtb=room)
            str_cm='SELECT * from ttkh'
            cnn.cursor.execute(str_cm)
            record1=cnn.cursor.fetchone()
            str_cm='SELECT Gia from ttphong'
            cnn.cursor.execute(str_cm)
            record2=cnn.cursor.fetchone()
            cost=record2[0]
            if record1:
                name=record1[0]
                cccd=record1[3]
                nt=record1[5]
                nr=record1[6]
                kc=(int(nr[8:])-int(nt[8:]))*int(cost)
                self.lb1.config(text=str)
                self.lbname.config(text=f'Họ tên: {name}')
                self.lbcccd.config(text=f'CCCD  : {cccd}')
                self.lbnd.config(text=f'Ngày đến: {nt}')
                self.lbnr.config(text=f'Ngày đi:{nr} ')
                self.cost.config(text=f'Tổng tiền thanh toán: {kc}')
            else:
                self.lb1.config(text="")
                self.lbname.config(text="")
                self.lbcccd.config(text="")
                self.lbnd.config(text="")
                self.lbnr.config(text="")
                self.cost.config(text="")
                self.lb1.config(text="")
                self.lbnopers.config(text=f'Không tìm thấy thông tin khách hàng phòng {room}')

            cnn.stop_connection()

    def deletekh(self):
        room=self.et1.get()
        cnn=Connection(dtb=room)
        str_cm='DELETE from ttkh'
        cnn.cursor.execute(str_cm)
        cnn.cursor.commit()
        str_cm='''UPDATE ttphong SET  Trangthai= 1 WHERE Sophong=R101'''
        cnn.cursor.commit()
        cnn.stop_connection()


    def update(self):
            self.et1.delete(0,"end")
            self.lb1.config(text="")
            self.lbname.config(text="")
            self.lbcccd.config(text="")
            self.lbnd.config(text="")
            self.lbnr.config(text="")
            self.cost.config(text="")
            self.lbnopers.config(text="")
            self.ctr.show_frame(StartPage2)

    
class Face_register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #hình nền
        logo = tk.PhotoImage(file="face_rg5.png")
        BGlabel = tk.Label(self,image=logo)
        BGlabel.image = logo
        BGlabel.place(x=0,y=0,width=800,height=450)

        # self.img_done=tk.PhotoImage(file=r"E:\TAI LIEU\năm 4\Face_DATN\imgs\dkytc.png")
        # self.bgtc=tk.Label(self,image=self.img_done)
        # self.bgtc.pack_forget()
        


        self.window = controller

        # back
        self.vid = cap1

        bt_back=tk.Button(self,text="BACK",font=font_cambria,bg="#375454",fg='white',width=8,command=lambda:self.stop_video()).place(x=20,y=405)
        bt_start=tk.Button(self,text="START",font=font_cambria,bg="#375454",fg='white',width=8,command=lambda:self.show()).place(x=570,y=245)

        # bt_stop=tk.Button(self,text="STOP",font=font_cambria,bg="#375454",fg='white',width=8,command=lambda:self.stop_video()).place(x=570,y=400)

        self.canvas=self.window.canvas
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1000
        self.cam_on=True
        self.job=None
        self.cv=None
        # self.update_widget()
        self.fill_blk=True
        self.count_frame=1
        self.cnn=Connection(dtb='R101')

        self.et1=tk.Entry(self,font=font_cambria,width=10,highlightthickness=2,highlightbackground="#375454").place(x=600,y=130)
        self.et2=tk.Entry(self,font=font_cambria,width=10,highlightthickness=2,highlightbackground="#375454").place(x=600,y=180)

    def update_widget(self):
        # hiện video và luu vao cơ sở dữ liệu
        # Get a frame from the video source
        if self.cam_on and self.count_frame<6:
            # ret, frame = self.vid.read()
            ret, frame = cap1.read()
            frame = cv2.resize(frame,(440,330))
            if self.count_frame==5:
                str="Done"
                self.cnn.stop_connection()
            else:
                str=f'Picture {self.count_frame}'
            cv2.putText(frame, str, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # xư lý anh truoc khi luu
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            img_encode = cv2.imencode('.jpg', small_frame)[1]
            data_encode = np.array(img_encode)
            byte_encode = data_encode.tobytes()
            # end 
            # lưu vao csdl
           
            str_cm=f'INSERT INTO ttkh (Hinh{self.count_frame}) values(?)'
            self.cnn.cursor.execute(str_cm,byte_encode)
            self.cnn.cursor.commit()
            if ret:
                # hiện video trên app
                self.image = PIL.Image.fromarray(frame)
                self.photo = PIL.ImageTk.PhotoImage(image=self.image)
                self.cv=self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
                self.count_frame+=1
            # self.window.after(self.delay, self.update_widget)
            self.job=self.window.after(self.delay, self.update_widget)
        else:
             self.window.after_cancel(self.job)
             self.count_frame=5
             self.job = None
             self.window.delete()
            #  self.bgtc.place(x=90,y=150)
             cap1.release()
            # print(self.job)
    def show(self):
        self.window.creat_canvas()
        self.canvas=self.window.canvas
        for ch in self.winfo_children():
            if isinstance(ch, tk.Entry):
                if ch.get()=="":
                    self.fill_blk=True
                    messagebox.showwarning(title="Warning",message="Fill the blank")
                    break
                else:
                    self.fill_blk=False
        if not self.fill_blk:
            self.cam_on=True
            self.window.show_cv()
            self.update_widget()
            cap1=cv2.VideoCapture(0)
            # self.vid = cv2.VideoCapture(0)
    def stop_video(self):
        
        # self.window.after_cancel(self.job)
        for ch in self.winfo_children():
            if isinstance(ch, tk.Entry):
                ch.delete(0,"end")
        self.cam_on=False
        # self.bgtc.pack_forget()
        # if self.vid.isOpened():
        #     self.vid.release()
        # cap1.release()
        if self.job is not None:
            self.window.after_cancel(self.job)
            self.job = None
            self.window.delete()
        # self.window.delete()
        
        self.window.show_frame(StartPage2)


app = tkinterApp()
app.mainloop()
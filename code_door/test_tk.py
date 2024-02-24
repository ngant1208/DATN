# import tkinter as tk
# import time
# class App(tk.Tk):
#     def __init__(self,*args, **kwargs):
#          tk.Tk.__init__(self, *args, **kwargs)
#          self.label1 = tk.Label(self, text="", width=20, anchor="w")
#          self.geometry('800x480')
#          self.img_bg=tk.PhotoImage(file="XhIeBC.png")
#          self.label=tk.Label(self,image=self.img_bg).place(x=0, y=0)
#          self.f=tk.Frame(self,bd=2,relief="raise",height=500,width=500).pack(pady=80)
#          self.label2=tk.Label(self.f,text="ENTER YOUR PASSWORD",font=50).pack(pady=10)
#          self.label3=tk.Label(self.f,text="SCANNING...",font=20).pack(pady=10)
#         #  self.start()
#         #  self.label.pack(side="top",fill="both",expand=True)
#         #  self.print_label_slowly("Hello, world!")
        
    # def print_label_slowly(self, message):
    #         '''Print a label one character at a time using the event loop'''
    #         t = self.label1.cget("text")
    #         t += message[0]
    #         self.label1.config(text=t)
    #         if len(message) > 1:
    #             self.after(500, self.print_label_slowly, message[1:])
    # def start(self):
        
    #     label.pack(pady=10)
    #     label1=tk.Label(self.f,text="SCANNING...",font=20)
    #     label1.pack(pady=10)
from tkinter import *
# def print_label_slowly(pr,labl,message="* * * * *"):
#         '''Print a label one character at a time using the event loop'''
#         t = labl.cget("text")
#         t += message[0]
#         labl.config(text=t)
#         if len(message) > 1:
#             pr.after(500,print_label_slowly, pr,labl,message[1:])

# def check(m,g):
#     if m>0:
#         g[0].pack(side=LEFT,padx=20,pady=20)
#         m-=1


# def frame_get_pswd():
#     root=Tk()
#     root.geometry('800x480')
#     # root.config(bg='#f7ef38')
#     img = PhotoImage(file="XhIeBC.png")
#     label = Label(root,image=img)
#     label.place(x=0, y=0)

#     f=Frame(root,bd=2,relief=RAISED,height=500,width=500)
#     f.pack(pady=80)
#     label=Label(f,text="ENTER YOUR PASSWORD",font=50)
#     label.pack(pady=10)
#     label1=Label(f,text="SCANNING...",font=20)
#     label1.pack(pady=10)
#     gs=[]
#     for i in range(5):
#         lb2=Label(f,text="* ",font=20)
#         lb2.pack_forget()
#         gs.append(lb2)
#     root.after(500,check,gs)
#     root.mainloop()
        
        
            
    
# frame_get_pswd()
# app = App()
# app.mainloop()




# # def printSomething():
# #     # if you want the button to disappear:
# #     # button.destroy() or button.pack_forget()
# #     for x in range(9): # 0 is unnecessary
# #         label = Label(root, text= str(x))
# #     # this creates x as a new label to the GUI
# #         label.pack() 

# # root = Tk()

# # button = Button(root, text="Print Me", command=printSomething) 
# # button.pack()

# # root.mainloop()

# import pygame
# from pygame.locals import *
# import time
 
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GRAY = (200, 200, 200)

# pygame.init()
# screen = pygame.display.set_mode((640, 240))

# text = 'this text is editable'
# font = pygame.font.SysFont(None, 48)
# img = font.render(text, True, RED)

# rect = img.get_rect()
# rect.topleft = (20, 20)
# cursor = Rect(rect.topright, (3, rect.height))

# running = True
# background = GRAY

# while running:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running = False
        
#         if event.type == KEYDOWN:
#             if event.key == K_BACKSPACE:
#                 if len(text)>0:
#                     text = text[:-1]
#             else:
#                 text += event.unicode
#             img = font.render(text, True, RED)
#             rect.size=img.get_size()
#             cursor.topleft = rect.topright
    
#     screen.fill(background)
#     screen.blit(img, rect)
#     if time.time() % 1 > 0.5:
#         pygame.draw.rect(screen, RED, cursor)
#     pygame.display.update()

# pygame.quit()

# import tkinter as tk

# class App(tk.Tk):
#     def __init__(self,*args, **kwargs):
#          tk.Tk.__init__(self, *args, **kwargs)
#          self.label = tk.Label(self, text="", width=20, anchor="w")
#          self.label.pack(side="top",fill="both",expand=True)
#          self.print_label_slowly("Hello, world!")

#     def print_label_slowly(self, message):
#          '''Print a label one character at a time using the event loop'''
#          t = self.label.cget("text")
#          t += message[0]
#          self.label.config(text=t)
#          if len(message) > 1:
#              self.after(500, self.print_label_slowly, message[1:])

# app = App()
# app.mainloop()
f = open('nga_1.jpg', 'rb')
hex_string = f.read() 
bytearray.fromhex(hex_string)
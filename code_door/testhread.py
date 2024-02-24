# from multiprocessing import Pipe,Process
# def fnc1(cnn2):
#     for i in range(60):
#         if i%10==0:
#             cnn2.send(i)
# def fnc2(cnn1):
#     while cnn1.poll():
#         print(cnn1.recv())
# if __name__ == '__main__':

#     # Global variables
#     # Global = Manager().Namespace()
#     # Global.buff_num = 1
#     # Global.read_num = 1
#     # Global.write_num = 1
#     # Global.frame_delay = 0
#     # Global.is_exit = False
#     # read_frame_list = Manager().dict()
#     # write_frame_list = Manager().dict()
#     # print(cpu_count())
#     # print(read_frame_list)
#     cnn1,cnn2=Pipe()
#     p=Process(target=fnc1,args=(cnn2,))
#     p.start()
#     p2=Process(target=fnc2,args=(cnn1,))
#     p2.start()

#     p.join()
#     p2.join()

# 
# test video
import cv2
import time
cap=cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)
new_frame_time=0
prev_frame_time=0
img_background=cv2.imread('br.jpg')
width  =cap.get(3) 
height = cap.get(4)  
y_start=int(1/2*(height-350))
x_start=int(1/2*(width-450))
while 1:
    ret,frame=cap.read()
    small_frame=frame[y_start:y_start+350,x_start:x_start+450]
    v_img= cv2.copyMakeBorder(small_frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = 0)
    # print(frame)
    # new_frame_time = time.time()
    # fps = 1/(new_frame_time-prev_frame_time)
    # fps = int(fps)
    # fps = str(fps)
    # prev_frame_time = new_frame_time
    # cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
    img_background[60:430,40:510]=v_img
    cv2.imshow("test",img_background)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
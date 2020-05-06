from pynput.keyboard import Key, Controller
import time
import cv2
import numpy as np 

keyboard = Controller()

font = cv2.FONT_HERSHEY_SIMPLEX 

i = 0
cam = cv2.VideoCapture(0)

UP_THRESH = 220
LEFT_THRESH = 180
RIGHT_THRESH = 230

ready = 0

def key_w(ready):

    if ready:
        keyboard.press('w')
        time.sleep(0.4)
        keyboard.release('w')

def key_d(ready):

    if ready:
        keyboard.press('d')
        time.sleep(0.05)
        keyboard.release('d')

def key_a(ready):

    if ready:
        keyboard.press('a')
        time.sleep(0.05)
        keyboard.release('a')




while(True):

    _,frame = cam.read()
    frame = cv2.flip(frame,1)

    image = frame.copy()
    output = frame.copy()

    roi_up = frame[:200,:,:]
    roi_left = frame[200:576,:426,:]
    roi_right = frame[200:576,852:1280,:]
    roi_neutral = frame[200:576,426:852,:]


    cv2.rectangle(image, (0, 0), (426, 720),(0, 0, 255), -1)
    cv2.rectangle(image,(426,0),(852,720),(0,255,0),-1)
    cv2.rectangle(image,(852,0),(1280,720),(255,0,0),-1)
    cv2.rectangle(image,(0,0),(1280,200),(255,0,255),-1)
    cv2.rectangle(image,(0,576),(1280,720),(255,255,0),-1)

    alpha = 0.3
    cv2.addWeighted(image, alpha, output, 1 - alpha,
		0, output)
    
    cv2.rectangle(output,(1120,600),(1250,660),(0,0,255),-1)

    roi_ready = frame[600:660,1120:1250,:]

    gray_ready = cv2.cvtColor(roi_ready,cv2.COLOR_BGR2GRAY)

    _,gray_thresh = cv2.threshold(gray_ready,127,255,cv2.THRESH_BINARY)

    

    output = cv2.putText(output, '* UP', (550,50), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA)  
    output = cv2.putText(output, '* LEFT', (190,250), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA) 
    output = cv2.putText(output, '* NEUTRAL', (550,250), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA) 
    output = cv2.putText(output, '* RIGHT', (1000,250), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA) 

    output = cv2.putText(output, 'Kodathala Sai Varun', (50,650), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA) 

    output = cv2.putText(output, 'Ready?', (1120,630), font, 1, 
                  (0,0,0), 2, cv2.LINE_AA) 

    if(i>0):

        gray_up = cv2.cvtColor(roi_up,cv2.COLOR_BGR2GRAY)
        gray_left = cv2.cvtColor(roi_left,cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(roi_right,cv2.COLOR_BGR2GRAY)
        gray_neutral = cv2.cvtColor(roi_neutral,cv2.COLOR_BGR2GRAY)

        diff_up = cv2.absdiff(gray_up,temp_up)
        diff_left = cv2.absdiff(gray_left,temp_left)
        diff_right = cv2.absdiff(gray_right,temp_right)
        diff_neutral = cv2.absdiff(gray_neutral,temp_neutral)


        _,thresh_up = cv2.threshold(diff_up,127,255,cv2.THRESH_BINARY)
        _,thresh_left = cv2.threshold(diff_left,127,255,cv2.THRESH_BINARY)
        _,thresh_right = cv2.threshold(diff_right,127,255,cv2.THRESH_BINARY)
        _,thresh_neutral = cv2.threshold(diff_neutral,127,255,cv2.THRESH_BINARY)

        mean_up = np.mean(thresh_up)
        mean_left = np.mean(thresh_left)
        mean_right = np.mean(thresh_right)

        # print(mean_up,mean_left,mean_right)

        if(np.mean(gray_thresh)<230):
            ready = 1

        if(mean_up<248):
            key_w(ready)
        if(mean_right<230):
            key_d(ready)
        if(mean_left<230):
            key_a(ready)

    
    else:

        roi_up = cv2.cvtColor(roi_up,cv2.COLOR_BGR2GRAY)
        roi_left = cv2.cvtColor(roi_left,cv2.COLOR_BGR2GRAY)
        roi_right = cv2.cvtColor(roi_right,cv2.COLOR_BGR2GRAY)
        roi_neutral = cv2.cvtColor(roi_neutral,cv2.COLOR_BGR2GRAY)

        temp_up = roi_up
        temp_left = roi_left
        temp_right = roi_right
        temp_neutral = roi_neutral
        
    i+=1

    output = cv2.resize(output,(720,630))
    cv2.imshow('image',output)

    if(cv2.waitKey(1)&0xff == ord('q')):
        break

cv2.destroyAllWindows()
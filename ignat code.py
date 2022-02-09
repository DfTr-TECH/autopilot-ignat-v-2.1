#подключение библиотек и объявление переменных 

import cv2  

import numpy as np 

import time 

from playsound import playsound 

x_red = 0 

y_red = 0 

x_line = 0 

y_line = 0 

flag1 = 0 

flag2 = 0 

  

cap = cv2.VideoCapture(0)#захват видеопотока 

  

if not cap.isOpened(): 

    print("Cannot open camera") 

    exit() 

    cv2.resizeWindow('-', 10, 10) 

     

    #границы красного цвета в HSV 

high_red = np.array((255, 125, 47), np.uint8) 

low_red = np.array((161, 29, 0), np.uint8) 

  

    #граница для белого цвета 

high_white = np.array((255, 255, 255), np.uint8) 

low_white = np.array((127, 139, 141), np.uint8) 

playsound('voice/privet.mp3') 

def otvet(): 

    playsound("voice/linia.mp3") 

while True: 

   

    ret, frame = cap.read() 

    

    if not ret: 

        print('ops') 

        break 

         

    preout= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    out_line = cv2.inRange(preout, low_white, high_white) 

    # output of capture red objects 

    out_red = cv2.inRange(preout, low_red, high_red) 

    moments = cv2.moments(out_red, 1) 

    dM01 = moments['m01'] 

    dM10 = moments['m10'] 

    dArea = moments['m00'] 

    if dArea > 150: 

        x_red = int(dM10/dArea) 

        y_red = int(dM01/dArea) 

    cv2.circle(frame, (x_red,y_red), 10, (0, 0, 255), -1) 

    

    # output of capture white line 

     

     

    moments2 = cv2.moments(out_line, 1) 

    y_white = moments2['m01'] 

    x_white = moments2['m10'] 

    s = moments2['m00'] 

    if s > 150: #проверка белой линии в кадре 

        x_line = int(x_white/s) 

        y_line = int(y_white/s) 

    cv2.circle(frame, (x_line,y_line), 15, (255, 255, 255), -1) 

     

    cv2.imshow('-', frame) 

     

#searching red barrier block 

    if x_red > 330 and x_red < 380:# условие проверки на наличие красного цвета в кадре 

        print('stop') 

        flag1 = 0 

        flag2 = 0 

        playsound('voice/krasny cvet.mp3')#проигрывание аудиодорожки с синтезированным голосом 

        Break #выход из цикла после появления в середине кадра красного барьера 

 

    if x_line < 350:#проверка наличия белой линии в центре кадра 

        flag1 = 1 

        flag2 = 0 

    if x_line > 350: 

        otvet 

        flag1 = 0 

        flag2 = 1 

         

    if cv2.waitKey(5) == ord('q'):#процесс завершения видеопотока при нажатии "Q" 

        playsound('voice/vixod.mp3') 

        break 

cap.release()#освобождение канала камеры 

cv2.destroyAllWindows()#закрытие окна видеопотока 

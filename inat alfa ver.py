import cv2 
import numpy as np
import RPi.GPIO as RPIO
from playsound import playsound
x_red = 0
y_red = 0
x_white = 0
y_white = 0
x_line = 0 
y_line = 0
flag1 = 0
flag2 = 0
RPIO.setmode(RPIO.BCM)
RPIO.setup(22, RPIO.OUT)
RPIO.setup(23, RPIO.OUT)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    cv2.resizeWindow('-', 10, 10)
    
    #red color gran
high_red = np.array((250, 125,47), np.uint8)
low_red = np.array((161, 29, 0), np.uint8)

    #white color gran
high_white = np.array((250, 250, 250), np.uint8)
low_white = np.array((127, 139, 141), np.uint8)
playsound('voice/privet.mp3')
while True:
  
    ret, frame = cap.read()
   
    if not ret:
        print('oops')
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
    cv2.circle(frame, (x_red,y_red), 10, (255, 0, 0), -1)
   
    # output of capture white line
    
    
    moments2 = cv2.moments(out_line, 1)
    y_white = moments2['m01']
    x_white = moments2['m10']
    s = moments2['m00']
    if s > 150:
        x_line = int(x_white/s)
        y_line = int(y_white/s)
    cv2.circle(frame, (x_line,y_line), 15, (0, 0, 255), -1)
    
    cv2.imshow('-', frame)
    
 #searching red barrier block
    if x_red > 330 and x_red < 380:
        RPIO.output(22, 0)
        RPIO.output(23, 0)
        playsound('voice/crasny cvet.mp3')
        break
       
    if x_line < 355:
        flag1 = 1
        flag2 = 0
    if x_line > 350:
        flag1 = 0
        flag2 = 1
        
    RPIO.output(22, flag1)
    RPIO.output(23, flag2)
    
    if cv2.waitKey(5) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()


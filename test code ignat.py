import cv2 
import numpy as np
from playsound import playsound
#объявление переменных координат баръеров и линии, и объявление флагов
x_red = 0
y_red = 0
x_white = 0
y_white = 0
x_line = 0 
y_line = 0
flag1 = 0
flag2 = 0

#запись в переменную захваченных кадров
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera") #условие проверки работоспособности камеры
    exit()
#установка фиксированного размера окна для отладки кадра
    cv2.resizeWindow('-', 10, 10)
    
    #границы оранжевого цвета в RGB
high_red = np.array((250, 125,47), np.uint8)
low_red = np.array((161, 29, 0), np.uint8)

    #границы белого цвета в RGB
high_white = np.array((250, 250, 250), np.uint8)
low_white = np.array((127, 139, 141), np.uint8)
playsound('voice/privet.mp3')
while True:
  #начало записи видеопотока и флаг его состояния(ret)
    ret, frame = cap.read()
   #проверка на наличие проблем с записью видеосигнала
    if not ret:
        print('oops')
        break
    # перевод кадра из цветового пространства BGR в RGB 
    preout= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #отделение белой линии от остальных оъектов
    out_line = cv2.inRange(preout, low_white, high_white)
    # отделение оранжевых предметов от общего кадра 
    out_red = cv2.inRange(preout, low_red, high_red)
    #подключение функции moments
    moments = cv2.moments(out_red, 1)
	#вычисление площади, суммы пикселей по  осям X Y
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']
   #вычисление координат барьера в кадре
    if dArea > 150:
        x_red = int(dM10/dArea)
        y_red = int(dM01/dArea)
    cv2.circle(frame, (x_red,y_red), 10, (255, 0, 0), -1) #отрисовка красной метки для оранжевого барьера
#подключение moments для белого цвета
    moments2 = cv2.moments(out_line, 1)
#функции вычисления суммы осей X Y и площади пикселей для белой линии 
    y_white = moments2['m01']
    x_white = moments2['m10']
    s = moments2['m00']
# определение координат белой линии в кадре
    if s > 150:
        x_line = int(x_white/s)
        y_line = int(y_white/s)
    cv2.circle(frame, (x_line,y_line), 15, (0, 0, 255), -1)#отрисовка белой метки для линии в кадре
    
    cv2.imshow('-', frame)# отображение кадра с наложенными метками объектов
    
 #проверка позиции барьера: если объект в центре кадра по оси Х, то остановиться и уведомить об остановке
    if x_red > 330 and x_red < 380:
        playsound('voice/crasny cvet.mp3')
        break
       #удержание белой линии в центре кадра: если линия справа, то поднять первый флаг и опустить второй.
    if x_line < 355:
        flag1 = 1
        flag2 = 0
	# если линия слева, то поднять второй флаг и опустить первый
    if x_line > 350:
        flag1 = 0
        flag2 = 1
    if cv2.waitKey(5) == ord('q'): #выход из главного цикла после нажатия кнопки "Q"
        break
#освобождение канала данных камеры и закрытие окна видеопотока
cap.release()
cv2.destroyAllWindows()
#завершение работы программы

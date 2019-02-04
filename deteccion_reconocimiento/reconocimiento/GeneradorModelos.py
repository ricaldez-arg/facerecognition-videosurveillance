from imutils.video import VideoStream
import imutils
import cv2
import os
import time

clasifier = cv2.CascadeClassifier('../deteccion_persona/haarcascades/haarcascade_frontalface_default.xml')
ruta_datos = './data/'
def capturar(camara, nombre):

    ds = os.path.join(ruta_datos, nombre)
    data = os.listdir(ruta_datos)
    if nombre not in data:
        os.mkdir(ds)
        print 'DIRECTORIO creado: ' + ds + "/"

    detectarRostro(camara, ds+'/')



def detectarRostro(camara, destino):
    contador = 0
    seg_ant = time.strftime('%S')
    bol = True
    cont = 3
    while True:
        #ret, imagen = camara.read()
        imagen = camara.read()
        imagen = imutils.resize(imagen, width=720)
        """if bol:
            cv2.putText(imagen,str(cont),(100,100),cv2.FONT_HERSHEY_COMPLEX,2,255,2)
            seg_act = time.strftime('%S')
            if seg_act - seg_ant > 2:
                seg_ant = seg_act
                bol = False
            cv2.imshow('CAMARA', imagen)
            cont -= 1
            print 'sleep'
            continue
        cont = 3
        bol = True"""
        gray = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        rostros = clasifier.detectMultiScale(gray,1.3,5)

        for x,y,w,h in rostros:
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(0,255,0),2)
            ro_hum = gray[y:y+h,x:x+w]
            ro_hum = cv2.resize(ro_hum,(200,200))
            cv2.imwrite(destino + '%s.pgm' % str(contador),ro_hum)
            contador +=1
        cv2.imshow('CAMARA', imagen)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

if __name__ == '__main__':

    #src = 0
    #camara = cv2.VideoCapture(src)
    # src = 'rtsp://admin:Password@192.168.43.108/Streaming/channels/2'
    src = 'rtsp://admin:Password@192.168.43.108/doc/page/playback.asp'
    # src='rtsp://admin:Password@192.168.1.64/doc/page/preview.asp'
    # src = 0
    camara = VideoStream(src).start()
    persona = 'ar'
    capturar(camara, persona)

    camara.release()
    cv2.destroyAllWindows()
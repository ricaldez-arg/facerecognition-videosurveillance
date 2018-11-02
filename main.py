from imutils.video import VideoStream
from DeteccionMovimiento import DetectorMovimiento
from DeteccionPersona import DetectorRostro
from Reconocimiento import ReconocedorPersona
import numpy as np
import cv2
import imutils

fuente = 0

#src = 'rtsp://admin:Password@192.168.43.108/Streaming/channels/2'
#src='rtsp://admin:Password@192.168.43.108/doc/page/playback.asp'
#src='rtsp://admin:Password@192.168.1.64/doc/page/preview.asp'
#src ='./inputVideo.avi'
src=0
#camara = VideoStream(src).start()
camara = cv2.VideoCapture(src)
#camara2 = cv2.VideoCapture(src)
detectorM = DetectorMovimiento()
detectorR = DetectorRostro('./util/haarcascades/haarcascade_frontalface_default.xml')
reconocedor = ReconocedorPersona()
reconocedor.entrenar('./util/data/')

def dibujaRectangulo(puntos, img):
    for (x,y,w,h) in puntos:
        cv2.rectangle(img,(x,y),(x+w,y+h),(200,200,200),2)

def dibujaRectangulo2(pts_cds, img):

    if len(pts_cds)>0:
        for (pts, cds) in pts_cds:
            for (x,y,w,h) in pts:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

writer = None
output='outputVideo.avi'

while True:
    
    ret, img = camara.read()
    #ret2, img2 = camara.read()

    #img = camara.read()
    imgc = img.copy()
    img = imutils.resize(img, width=720)
    puntos, cuadros = detectorM.detectar(img)

    #dibujarRectangulo = lambda (x,y,w,h): cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #mostrador = lambda cuadro:cv2.imshow("detect2",cuadro)
    #map(mostrador, cuadros)
    #map(dibujarRectangulo, puntos)
    #[dibujarRectangulo(x) for x in puntos]
    #[cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) for (x,y,w,h) in puntos]
    dibujaRectangulo(puntos, img)

    #for cuadro in cuadros:
    #    pts, cds = detectorR.detectar(cuadro)
    '''if len(cuadros) > 0:
        cc = detectorR.detectar(cuadros[0])
    '''
    #pts_cds = [detectorR.detectar(cuadro) for cuadro in cuadros if len(cuadro) > 0]
    pts_cds = detectorR.detectar(img)
    dibujaRectangulo2([pts_cds],img)
    #dibujaRectangulo2(pts_cds,img)

    #estapa reconocimiento
    pts,cds = pts_cds
    for (x,y,w,h),cd in zip(pts,cds):
        nombre, predi = reconocedor.predecir(cd)
        cv2.putText(img, nombre, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)



    cv2.imshow("detect",img)

    if writer is None and output is not None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(output, fourcc,20,
	        (img.shape[1], img.shape[0]), True)

    if writer is not None:
        writer.write(img)

    if cv2.waitKey(1)& 0xff == ord('q'):
        break
if writer is not None:
    writer.release()
camara.release()
cv2.destroyAllWindows()

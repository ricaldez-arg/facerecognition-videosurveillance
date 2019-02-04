#!/usr/bin/env python
import argparse

import cv2
import imutils
from deteccion_reconocimiento import *
from imutils.video import VideoStream

from deteccion_reconocimiento.notificador import GestionAlarma
from deteccion_reconocimiento.procesador import Procesador
from deteccion_reconocimiento.reconocimiento import ReconocedorPersona

import time
def init(camara, procesador,args):
    #tiempo_actual = lambda: int(round(time.time() * 1000))
    #iniciot = tiempo_actual()
    #datos = []
    while True:
        try:

            img = camara.read()
            if img is None:
                break
            img = imutils.resize(img, width=720)
            #print img.shape[0]
            #print img.shape[1]

            #fint = tiempo_actual()
            #if (fint - iniciot) > 35000:
                #print datos
                #pass
            #inicio = tiempo_actual()

            img = procesador.procesar(img)

            #fin = tiempo_actual()
            #tiempo_empleado = fin - inicio
            #datos.append(tiempo_empleado)

            if args["mostrar"] > 0:
                cv2.imshow("LIVE STREAM", img)
                key = cv2.waitKey(1000) & 0xFF
                if key == ord("q"):
                    break
        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()
    camara.stop()
    #camara.release()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    src = 0
    #src = '../moduloseguridad-ejemplos/video2.avi'
    ap.add_argument("-f", "--fuente", default=src, help="fuente del video o camara")
    ap.add_argument("-m", "--mostrar", type=int, default=1, help="muestra si es 1 y no muestra si es 0")
    args = vars(ap.parse_args())

    src = args['fuente']
    camara = VideoStream(src).start()
    #camara = cv2.VideoCapture(src)

    detectorM = DetectorMovimiento()
    detectorR = DetectorRostro('./util/haarcascades/haarcascade_frontalface_default.xml')
    #detectorR = DetectorRostro('./util/haarcascades/haarcascade_profileface.xml')
    reconocedor = ReconocedorPersona()
    reconocedor.entrenar('./util/data/')

    gestion_alarma  = GestionAlarma()
    procesador = Procesador(detectorM=detectorM,detectorR=detectorR,reconocedor=reconocedor,
                            gestion_alarma=gestion_alarma,output_path='./grabaciones/')

    init(camara,procesador,args)


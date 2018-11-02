from imutils.video import VideoStream
import imutils
import numpy as np
import cv2
import os
import sys


class ReconocedorPersona(object):

    def __init__(self):
        #self.modelo = cv2.face.EigenFaceRecognizer_create()
        #self.modelo = cv2.face.FisherFaceRecognizer_create()
        self.modelo = cv2.face.LBPHFaceRecognizer_create()
        self.nombres = {'n':'NoReconoce'}
    def lectura_imagenes(self, ruta):
        x,y = [],[]
        contador = 0

        for directorio, directorios, archivos in os.walk(ruta):

            for subdirectorio in directorios:
                ruta_subdirectorio = os.path.join(directorio,subdirectorio)
                self.nombres[contador] = subdirectorio
                for archivo in os.listdir(ruta_subdirectorio):
                    try:
                        if archivo == '.directory':
                            pass
                        ruta_archivo = os.path.join(ruta_subdirectorio,archivo)

                        imagen = cv2.imread(ruta_archivo,cv2.IMREAD_GRAYSCALE)
                        imagen = cv2.resize(imagen,(200,200))
                        x.append(np.asarray(imagen,dtype=np.uint8))
                        y.append(contador)
                        print str(contador) + ':: ' + ruta_archivo
                    except IOError, (erron, strerror):
                        print 'I/O error ({0}):{1}'.format(erron,strerror)
                        #print 'I/O error (%s) :%d' % (erron,strerror)
                    except:
                        print 'Unexpected error:', sys.exc_info()[0]
                contador += 1
        return (x,y)

    def entrenar(self, ruta):
        imgs, inds = self.lectura_imagenes(ruta)
        inds = np.asarray(inds,dtype=np.int32)

        self.modelo.train(np.asarray(imgs), np.asarray(inds))
        print self.nombres

    def predecir(self,rostro):
        rostro = cv2.cvtColor(rostro,cv2.COLOR_BGR2GRAY)
        rostro = cv2.resize(rostro,(200,200),interpolation=cv2.INTER_LINEAR)
        prediccion = self.modelo.predict(rostro)
        etiqueta = prediccion[0]
        confianza = prediccion[1]
        print "Etiqueta: %s, confianza: %.2f" % (etiqueta, confianza)

        if confianza > 80:
            return self.nombres['n'], confianza
        return self.nombres[etiqueta], confianza



if __name__ == '__main__':
    reconocedor = ReconocedorPersona()
    #print reconocedor.lectura_imagenes('./data/')
    reconocedor.entrenar('./data/')

    # src = 'rtsp://admin:Password@192.168.43.108/Streaming/channels/2'
    src='rtsp://admin:Password@192.168.43.108/doc/page/playback.asp'
    #src='rtsp://admin:Password@192.168.1.64/doc/page/preview.asp'
    #src = 0
    camara = VideoStream(src).start()
    #camara = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('../DeteccionPersona/haarcascades/haarcascade_frontalface_default.xml')
    while True:
        #ret, imagen = camara.read()
        imagen = camara.read()
        imagen = imutils.resize(imagen, width=720)
        result = imagen.copy()
        rostros = face_cascade.detectMultiScale(imagen,1.3,5)
        imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)

        for x,y,w,h in rostros:
            result = cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)
            roi = imagen[y:y + h, x:x + w]
            cv2.imshow('roi',roi)
            nombre, predi= reconocedor.predecir(roi)
            cv2.putText(result, nombre, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

        cv2.imshow('DETECTING',result)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    camara.release()
    cv2.destroyAllWindows()


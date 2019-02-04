
import numpy as np
import cv2
import os
import sys


class ReconocedorPersona(object):

    def __init__(self):
        #self.modelo = cv2.face.EigenFaceRecognizer_create()
        #self.modelo = cv2.face.FisherFaceRecognizer_create()
        self.modelo = cv2.face.LBPHFaceRecognizer_create()
        self.nombres = {'n':'desconocido'}

    def entrenar(self, ruta):
        imgs, inds = self.__lectura_imagenes(ruta)
        inds = np.asarray(inds,dtype=np.int32)

        self.modelo.train(np.asarray(imgs), np.asarray(inds))
        print self.nombres

    def __lectura_imagenes(self, ruta):
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
                    except:
                        print 'Unexpected error:', sys.exc_info()[0]
                contador += 1
        return (x,y)


    def predecir(self,rostro):
        rostro = cv2.cvtColor(rostro,cv2.COLOR_BGR2GRAY)
        rostro = cv2.resize(rostro,(200,200),interpolation=cv2.INTER_LINEAR)

        prediccion = self.modelo.predict(rostro)

        etiqueta = prediccion[0]
        confianza = prediccion[1]
        #print "Etiqueta: %s, confianza: %.2f" % (etiqueta, confianza)

        if confianza > 80:
            return self.nombres['n'], confianza
        return self.nombres[etiqueta], confianza

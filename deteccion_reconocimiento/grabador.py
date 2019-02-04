import cv2
import time
from os import path

class Grabador(object):
    def __init__(self, ruta_grabacion):
        self.ruta_grabacion = ruta_grabacion
        self.writer = None
        self.tiempo_actual = lambda: int(round(time.time() * 1000))
        self.tiempo_inicio = self.tiempo_actual()
        self.grabando = False
        self.ruta_archivo = None
    def __iniciar_grabacion(self):
        ruta = time.strftime('%Y-%m-%d') + "_"+time.strftime("%H:%M:%S") +".avi"
        self.ruta_archivo = path.join(self.ruta_grabacion,ruta)

    def grabacion(self,imagen,nivel):

        if nivel > 0:
            self.tiempo_inicio = self.tiempo_actual()
            if not self.grabando:
                self.__iniciar_grabacion()
                self.grabando = True
            self.__grabar(imagen)
        else:
            tiempo = self.tiempo_actual() - self.tiempo_inicio
            #print tiempo
            if tiempo < 10000:
                if not self.grabando:
                    print "Inicia grabacion..."
                    self.__iniciar_grabacion()
                    self.grabando = True
                self.__grabar(imagen)
            else:
                print "grabacion::[off]"
                self.stop()
                self.grabando = False
                self.ruta_archivo = None
                self.writer = None

    def __grabar(self, img):

        if self.writer is None and self.ruta_archivo is not None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            self.writer = cv2.VideoWriter(self.ruta_archivo, fourcc, 20,
                                          (img.shape[1], img.shape[0]), True)
        if self.writer is not None:
            self.writer.write(img)

    def stop(self):
        if self.writer is not None:
            self.writer.release()
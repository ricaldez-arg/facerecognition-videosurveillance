import cv2

from deteccion_reconocimiento.grabador import Grabador

class Procesador(object):

    def __init__(self, detectorM, detectorR, reconocedor, gestion_alarma, output_path=None):
        self.detectorM = detectorM
        self.detectorR = detectorR
        self.output_path = output_path
        self.reconocedor = reconocedor
        self.gestion_alarma = gestion_alarma
        self.colorM = (200, 200, 200)
        self.colorD = (0, 255, 0)
        self.colorR = (255,0,0)
        if output_path is not None:
            self.grabador = Grabador(output_path)

    def __analizar(self,img):

        nivelAlarma = 0
        puntos, cuadros = self.detectorM.detectar(img)
        self.dibujaRectangulo(puntos, img)

        #si no se detecta movimiento
        if len(puntos) == 0:
            self.gestion_alarma.activar(nivelAlarma)
            return img,nivelAlarma

        nivelAlarma = 1
        pts_cds = self.detectorR.detectar(img)
        self.dibujaRectangulo2([pts_cds], img)
        pts, cds = pts_cds

        #si no se detecta rostro
        if len(pts) == 0:
            self.gestion_alarma.activar(nivelAlarma)
            return img,nivelAlarma

        nivelAlarma = 2

        for (x, y, w, h), cd in zip(pts, cds):
            try:
                nombre, predi = self.reconocedor.predecir(cd)

                cv2.putText(img, nombre, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,self.colorR, 2)
                #Si se detecta como persona desconocida
                if nombre == "desconocido":
                    nivelAlarma += 1
            except Exception as ex:
                pass
                #print "Ocurrio un error con el modulo reconocedor:\n" + str(ex.message)

        self.gestion_alarma.activar(nivelAlarma)
        return img,nivelAlarma

    def dibujaRectangulo(self, puntos, img):
        for (x, y, w, h) in puntos:
            cv2.rectangle(img, (x, y), (x + w, y + h), self.colorM, 2)


    def dibujaRectangulo2(self, pts_cds, img):
        if len(pts_cds) > 0:
            for (pts, cds) in pts_cds:
                for (x, y, xf, yf) in pts:
                    cv2.rectangle(img, (x, y), (xf, yf), self.colorD, 2)

    def procesar(self, img):

        imagen,nivel = self.__analizar(img)

        if self.output_path is not None:
            self.grabador.grabacion(imagen,nivel)

        return imagen

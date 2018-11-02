
import numpy as np
import cv2
import imutils

class Procesador(object):
    def __init__(self, detectorM, detectorR, reconocedor, output_path=None):
        self.detectorM = detectorM
        self.detectorR = detectorR
        self.reconocedor = reconocedor
        self.output_path = output_path
        if output_path:
            self.writer = None

    def dibujaRectangulo(self, puntos, img):
        for (x, y, w, h) in puntos:
            cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), 2)


    def dibujaRectangulo2(self, pts_cds, img):
        if len(pts_cds) > 0:
            for (pts, cds) in pts_cds:
                for (x, y, w, h) in pts:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def procesar(self, img):
        puntos, cuadros = self.detectorM.detectar(img)
        self.dibujaRectangulo(puntos, img)

        pts_cds = self.detectorR.detectar(img)
        self.dibujaRectangulo2([pts_cds], img)

        pts, cds = pts_cds
        for (x, y, w, h), cd in zip(pts, cds):
            nombre, predi = self.reconocedor.predecir(cd)
            cv2.putText(img, nombre, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

        #cv2.imshow("detect", img)

        if self.writer is None and self.output_path is not None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            self.writer = cv2.VideoWriter(self.output_path, fourcc, 20,
                                     (img.shape[1], img.shape[0]), True)

        if self.writer is not None:
            self.writer.write(img)

        return img

    def stop(self):
        if self.writer is not None:
            self.writer.release()

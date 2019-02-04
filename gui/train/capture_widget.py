from PyQt4 import QtGui

import cv2
import numpy as np

from deteccion_reconocimiento import Generador


class CaptureWidget(QtGui.QWidget):

    def __init__(self,  data_path, cascade_path, parent=None):
        super(CaptureWidget,self).__init__(parent)

        self.generador = Generador(data_path)

        self.classifier = cv2.CascadeClassifier(cascade_path)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._green = (0, 255, 0)
        self._blue = (255,0 ,0)

        self._width = 2
        self.capt = False
        self.starting = True

    def detect_faces(self, image= np.ndarray):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.1,
                                                 minNeighbors=3)
                                                 #flags=cv2.CASCADE_SCALE_IMAGE)

        return faces


    def image_data_slot(self, image_data):
        if self.starting:
            faces = self.detect_faces(image_data)
            for (x, y, w, h) in faces:
                cv2.rectangle(image_data,
                              (x, y),
                              (x+w, y+h),
                              self._green,
                              self._width)
            if self.capt:
                for (x,y,w,h) in faces:
                    rostro = image_data[y:y+h,x:x+w]
                    self.generador.guardar(self.usuario,rostro)
                self.capt = False


            image_data = cv2.resize(image_data,(0,0),fx=0.7,fy=0.7)
            self.image = self.get_qimage(image_data)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())

            self.update()

    def capturar_guardar(self,usuario):
        self.usuario = usuario
        self.capt = True

    def get_qimage(self, image= np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def start(self):
        if not self.starting:
            self.starting = True
    def stop(self):
        if self.starting:
            self.starting = False

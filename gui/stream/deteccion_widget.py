from PyQt4 import QtGui
import numpy as np
import cv2
class DetectionWidget(QtGui.QWidget):
    def __init__(self, procesador, parent=None):
        super(DetectionWidget,self).__init__(parent)
        self.procesador = procesador
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)
        self.starting = True
        self.cont = 0

    def detect(self, img = np.ndarray):
        imagen = self.procesador.procesar(img)
        return imagen

    def image_data_slot(self, image_data):
        if self.starting:
            image_data = self.detect(image_data)
            #image_data = imutils.resize(image_data, width=720)
            self.image = self.get_qimage(image_data)
            if self.image.size() != self.size():
                self.setFixedSize(self.image.size())
                a = 0

            self.update()

    def get_qimage(self, image= np.ndarray):
        #print image
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
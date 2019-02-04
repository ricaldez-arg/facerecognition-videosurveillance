from PyQt4 import QtCore
from imutils.video import VideoStream
import numpy as np
import imutils
import cv2

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)
    image_dataT = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super(RecordVideo,self).__init__(parent)
        self.puerto = camera_port
        self.camera = VideoStream(camera_port).start()
        self.is_opened =  self.camera.stream.isOpened()

        self.timer = QtCore.QBasicTimer()
        self.outline = np.zeros((480, 720, 3), np.uint8)
        cv2.putText(self.outline,'CAMARA FUERA DE LINEA',(100,250),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)#,cv2.LINE_AA)

    def start_recording(self):
        self.timer.start(0, self)
        if self.camera is None:
            self.camera = VideoStream(self.puerto).start()

    def stop_recording(self):
        self.timer.stop()
        self.camera.stop()
        self.camera = None

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        data = self.camera.read()
        if data is not None:
            data = imutils.resize(data, width=720)
            self.image_data.emit(data.copy())
            self.image_dataT.emit(data.copy())
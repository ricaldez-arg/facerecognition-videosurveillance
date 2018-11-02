from PyQt4 import QtCore
import numpy as np
import cv2

class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)
    image_dataT = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super(RecordVideo,self).__init__(parent)
        self.puerto = camera_port
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)
        if not self.camera.isOpened():
            self.camera = cv2.VideoCapture(self.puerto)

    def stop_recording(self):
        self.timer.stop()
        self.camera.release()

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data.copy())
            self.image_dataT.emit(data.copy())

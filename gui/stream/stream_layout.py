from PyQt4 import QtGui
from deteccion_widget import DetectionWidget
from gui.record_video import RecordVideo

class StreamLayout(QtGui.QVBoxLayout):
    def __init__(self,recorder, procesador, parent=None):
        super(StreamLayout, self).__init__()
        self.detection_widget = DetectionWidget(procesador)

        # TODO: set video port
        #self.record_video = RecordVideo()
        self.record_video = recorder

        image_data_slotT = self.detection_widget.image_data_slot
        self.record_video.image_dataT.connect(image_data_slotT)

        #layout = QtGui.QVBoxLayout()

        # layout.addWidget(self.detection_widget)
        self.run_button = QtGui.QPushButton('Start Live')
        self.start = False
        self.addWidget(self.run_button)
        self.addWidget(self.detection_widget)


        self.run_button.clicked.connect(self.start_stop)
        #self.setLayout(layout)
    def startt(self):
        self.detection_widget.start()
    def stop(self):
        self.detection_widget.stop()

    def start_stop(self):
        if self.start:
            self.record_video.stop_recording()
            self.start = not self.start
            self.run_button.setText('Start live')
        else:
            self.record_video.start_recording()
            self.start = not self.start
            self.run_button.setText('Stop live')
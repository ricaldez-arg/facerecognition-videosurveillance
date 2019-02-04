from PyQt4 import QtGui
from capture_widget import CaptureWidget

class VideoLayout(QtGui.QVBoxLayout):
    def __init__(self, recorder, data_path, cascade_path, parent=None):
        super(VideoLayout, self).__init__()
        self.capture_widget = CaptureWidget(data_path, cascade_path)

        self.record_video = recorder

        image_data_slot = self.capture_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        #layout = QtGui.QVBoxLayout()

        # layout.addWidget(self.face_detection_widget)
        #self.run_button = QtGui.QPushButton('Start Live')
        #self.start = False
        #self.addWidget(self.run_button)
        self.addWidget(self.capture_widget)
        self.record_video.start_recording()


        #self.run_button.clicked.connect(self.start_stop)
        #self.setLayout(layout)
    def capturar(self, usuario):
        self.capture_widget.capturar_guardar(usuario)

    def start_stop(self):
        if self.start:
            self.record_video.stop_recording()
            self.start = not self.start
            #self.run_button.setText('Start live')
        else:
            self.record_video.start_recording()
            self.start = not self.start
            #self.run_button.setText('Stop live')

    def start(self):
        self.capture_widget.start()
    def stop(self):
        self.capture_widget.stop()

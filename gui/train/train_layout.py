from PyQt4 import QtGui
from ui_frame import Ui_Frame

class TrainLayout(QtGui.QVBoxLayout):
    def __init__(self,recorder,data_path, cascade_path, parent=None):
        super(TrainLayout,self).__init__(parent)

        self.ui = Ui_Frame(recorder, cascade_path)
        self.ui.setupUi(data_path)
        self.ui.show()
        self.addWidget(self.ui)
    def stop(self):
        self.ui.stop()
    def startt(self):
        self.ui.start()
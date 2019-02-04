from PyQt4 import QtGui
from ui_frame import Ui_Frame

class TrainLayout(QtGui.QVBoxLayout):
    def __init__(self,recorder,data_path, cascade_path, parent=None):
        super(TrainLayout,self).__init__(parent)
        print "train layout 1"
        self.ui = Ui_Frame(recorder, cascade_path)
        print "train layout 2"
        self.ui.setupUi(data_path)
        print "train layout 3"
        self.ui.show()
        print "train layout 4"
        self.addWidget(self.ui)
        print "trainlayoiut"
    def stop(self):
        self.ui.stop()
    def startt(self):
        self.ui.start()
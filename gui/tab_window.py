import sys
from os import path
from PyQt4.QtGui import *
from stream.stream_layout import StreamLayout
from train.train_layout import TrainLayout
from record_video import RecordVideo
from DeteccionMovimiento import DetectorMovimiento
from DeteccionPersona import DetectorRostro
from Reconocimiento import ReconocedorPersona
from procesador import Procesador

class TabWindow(QTabWidget):
    def __init__(self, recorder,data_path,cascade , parent=None):
        self.data_path = data_path
        self.cascade_filepath = cascade
        self.recorder = recorder
        super(TabWindow, self).__init__(parent)

        self.tab0 = QWidget()
        self.tab1 = QWidget()
        #self.tab2 = QWidget()

        self.tabs = [self.tab0,self.tab1]


        #self.tab3 = QWidget()
        self.addTab(self.tab0,"Tab 0")
        self.addTab(self.tab1,"Tab 1")
        #self.addTab(self.tab2,"Tab 2")
        #self.addTab(self.tab3,"Tab 3")
        self.tab0UI(cascade)
        self.tab1UI()
        #self.tab2UI()
        #self.tab3UI()
        self.setWindowTitle("tab demo")
        self.currentChanged.connect(self.change)
        self.change()
    def change(self):
        index = self.currentIndex()
        current =  self.currentWidget()
        y = current.layout()
        y.startt()
        print "change to: " + str(index)
        #layout = self.tab1.layout()
        [x.layout().stop() for x in self.tabs if x !=current]


    def tab0UI(self, cascade):
        detectorM = DetectorMovimiento()
        detectorR = DetectorRostro()
        reconocedor = ReconocedorPersona()
        reconocedor.entrenar(self.data_path)

        procesador = Procesador(detectorM,detectorR,reconocedor,'output.avi')

        layout = StreamLayout(self.recorder, procesador)

        self.setTabText(0, "Stream")
        self.tab0.setLayout(layout)

    def tab1UI(self):
        layout = TrainLayout(self.recorder,self.data_path, self.cascade_filepath)
        self.setTabText(1, "Generador de Modelos")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout=QFormLayout()
        sex=QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())
        self.setTabText(2,"Personal Details")
        self.tab2.setLayout(layout)
    def tab3UI(self):
        layout=QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(3,"Education Details")
        self.tab3.setLayout(layout)
def main(cascade_file_path):
    app = QApplication(sys.argv)
    recorder = RecordVideo(0)
    ex = TabWindow(recorder, cascade_file_path)
    ex.setGeometry(200, 50, 850, 700)
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir, '../util/haarcascades/haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)
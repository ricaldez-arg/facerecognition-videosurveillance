import sys
from os import path
from PyQt4 import QtCore
from PyQt4.QtGui import *
from deteccion_reconocimiento import *
from record_video import RecordVideo
from stream.stream_layout import StreamLayout
from train.train_layout import TrainLayout
from gestion_usuario import GestionadorLayout
from about import About


class TabWindow(QTabWidget):

    def __init__(self, recorder,data_path,cascade , dir_grabaciones=None, parent=None):
        super(TabWindow, self).__init__(parent)
        self.dir_grabaciones = dir_grabaciones
        self.data_path = data_path
        self.cascade_filepath = cascade
        self.recorder = recorder

        self.setGeometry(200, 50, 850, 850)
        self.reconocedor = ReconocedorPersona()

        self.tab0 = QWidget()
        #self.tab0.setGeometry(100, 100, 800, 800)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs = [self.tab0,self.tab1,self.tab2,self.tab3]

        self.addTab(self.tab0,"Tab 0")
        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2,"Tab 2")
        self.addTab(self.tab3,"Tab 3")
        self.tab0UI()
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        icono_s = QIcon('./util/iconos/security-camera.png')
        self.setTabIcon(0, icono_s)

        icono_s = QIcon('./util/iconos/security-camera(1).png')
        self.setTabIcon(1, icono_s)

        icono_s = QIcon('./util/iconos/insurance.png')
        self.setTabIcon(2, icono_s)

        icono_s = QIcon('./util/iconos/info.png')
        self.setTabIcon(3, icono_s)

        self.setWindowTitle("Deteccion y Reconocimiento")
        self.setCurrentIndex(3)
        self.currentChanged.connect(self.change)

        self.setStyleSheet(CssTab.Css_tabp)
        #self.change()
    def change(self):
        index = self.currentIndex()
        current =  self.currentWidget()
        y = current.layout()
        if self.layout == y:
            self.actualizarReconocedor()
            #self.reconocedor.entrenar(self.data_path)
        y.startt()
        print "actual: " + str(index)
        [x.layout().stop() for x in self.tabs if x !=current]

    def actualizarReconocedor(self):
        try:
            self.reconocedor.entrenar(self.data_path)
            self.layout.mensaje.setText("")
        except:
            mensaje = "No existe usuario registrado o fotos del usuario registardo, primero debe crear usuarios y\n " \
                      "capturar los modelos(fotos de rostro), para el reconocimiento en la seccion <Generador de Modelos>."
            self.layout.mensaje.setText(mensaje)

    def tab0UI(self):

        detectorM = DetectorMovimiento()
        detectorR = DetectorRostro(rutaModelo=self.cascade_filepath)
        #self.reconocedor = ReconocedorPersona()
        #self.reconocedor.entrenar(self.data_path)

        gestion_alarma = GestionAlarma()

        procesador = Procesador(detectorM,detectorR, self.reconocedor,
                                     gestion_alarma,self.dir_grabaciones)
        self.layout = StreamLayout(self.recorder, procesador)

        self.setTabText(0, "Stream")
        self.tab0.setLayout(self.layout)

    def tab1UI(self):
        layout = TrainLayout(self.recorder,self.data_path, self.cascade_filepath)
        self.setTabText(1, "Generador de Modelos")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout= GestionadorLayout(self.data_path)
        self.setTabText(2,"Gestion de usuarios")
        self.tab2.setLayout(layout)
    def tab3UI(self):
        layout=About()
        self.setTabText(3,"Informacion")
        self.tab3.setLayout(layout)

class CssTab(object):

    Css_tabp = '''
           QTabWidget::pane {
                top:8px;
                border-top: 2px solid #C2C7CB;
                /*border:none;*/
            }

            QTabWidget::tab-bar {
                alignment: left; 
                top:10px; 
                left:30px; 
            }

            QTabBar::tab {
                background:transparent;
                background: rgb(200,200,200);
                border: 1px solid #C4C4C3;
                /*border:none;*/
                /*border-bottom:none;*/
                border-top:none;
                border-right:none;
                border-left:none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                font-size:14px;
                border-bottom: 1px solid skyblue;
                background: darkgray;
                color:white
            }

            QTabBar::tab:selected {
                border-color: #9B9B9B;
                font-weight: bold;
                border-bottom: 1px solid skyblue;
                selection-background-color:red;
            }

            QTabBar::tab:!selected {
                margin-top: 3px; /* make non-selected tabs look smaller */
            }

            QTabBar::tab:selected {
                margin-left: -4px;
                margin-right: -4px;

            }

            QTabBar::tab:first:selected {
                margin-left: 0;
            }

            QTabBar::tab:last:selected {
                margin-right: 0;
            }

            QTabBar::tab:only-one {
                margin: 0;
            }

        '''

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

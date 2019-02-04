from PyQt4 import QtGui,QtCore
from deteccion_widget import DetectionWidget
from deteccion_reconocimiento.notificador import Notificador

class StreamLayout(QtGui.QVBoxLayout):
    def __init__(self,recorder, procesador, parent=None):
        super(StreamLayout, self).__init__()
        self.procesador = procesador
        self.detection_widget = DetectionWidget(procesador)

        #self.setGeometry(QtCore.QRect(0, 0, 20, 20))
        # TODO: set video port
        #self.record_video = RecordVideo()
        self.record_video = recorder

        image_data_slotT = self.detection_widget.image_data_slot
        self.record_video.image_dataT.connect(image_data_slotT)

        self.__anade_info_color()

        # layout.addWidget(self.detection_widget)
        #self.run_button = QtGui.QPushButton('Start Live')
        self.start = False
        #self.addWidget(self.run_button)

        self.addWidget(self.detection_widget)
        self.__anade_info_alarma()

        self.alarma = AlarmaVisual(self.mensaje_alarma)
        gestor = self.procesador.gestion_alarma
        gestor.add_alarma(self.alarma)
        #self.run_button.clicked.connect(self.start_stop)
        #self.setLayout(layout)

    def startt(self):
        self.detection_widget.start()
        if not self.record_video.is_opened:
            self.detection_widget.image_data_slot(self.record_video.outline)

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

    def __anade_info_color(self):
        some0 = QtGui.QGridLayout()
        some = QtGui.QFrame()
        some.setFixedHeight(50)
        some.setFixedWidth(700)

        self.label_colort1 = QtGui.QLabel("Deteccion movimiento ")
        self.label_color1 = QtGui.QLabel()
        r, g, b = self.procesador.colorM
        self.label_color1.setStyleSheet("background-color:rgb%s;border-radius:3px;" % str((b, g, r)))
        self.label_color1.setFixedHeight(10)

        self.label_colort2 = QtGui.QLabel("Deteccion rostro ")
        self.label_color2 = QtGui.QLabel()
        r, g, b = self.procesador.colorD
        self.label_color2.setStyleSheet("background-color:rgb%s;border-radius:3px;" % str((b, (g - 50), r)))
        self.label_color2.setFixedHeight(10)

        self.label_etiqueta1 = QtGui.QLabel("Nombre")
        self.label_etiqueta2 = QtGui.QLabel()
        r, g, b = self.procesador.colorR
        self.label_etiqueta2.setStyleSheet("background-color:rgb%s;border-radius:3px;" % str((b, g, r)))
        self.label_etiqueta2.setFixedHeight(10)

        some0.addWidget(self.label_colort1, 0, 0)
        some0.addWidget(self.label_color1, 0, 1)
        some0.addWidget(QtGui.QLabel(""), 0, 2)
        some0.addWidget(self.label_colort2, 0, 3)
        some0.addWidget(self.label_color2, 0, 4)
        some0.addWidget(QtGui.QLabel(""), 0, 5)
        some0.addWidget(self.label_etiqueta1, 0, 6)
        some0.addWidget(self.label_etiqueta2, 0, 7)

        some.setLayout(some0)
        some.setStyleSheet(Css_stream.Css_label)

        self.addWidget(some)
    def __anade_info_alarma(self):
        box1 = QtGui.QVBoxLayout()

        box = QtGui.QFrame()
        box.setFixedHeight(120)
        box.setFixedWidth(720)

        notif = QtGui.QLabel("Notificacion de alarma:")
        notif.setStyleSheet(Css_stream.Css_label)

        self.mensaje_alarma = QtGui.QTextEdit()
        self.mensaje_alarma.setReadOnly(True)
        self.mensaje_alarma.setStyleSheet(Css_stream.Css_mensaje_alarma)


        box1.addWidget(notif)
        box1.addWidget(self.mensaje_alarma)

        self.mensaje = QtGui.QLabel("")
        box1.addWidget(self.mensaje)

        box.setLayout(box1)

        self.addWidget(box)


class AlarmaVisual(Notificador):
    def __init__(self,salida):
        self.salida = salida

    def activar0(self):
        self.salida.setText("")
    def activar1(self):
        self.salida.setText("MOVIMIENTO DETECTADO")
    def activar2(self):
        self.salida.setText("PRESENCIA DE PERSONA")
    def activar3(self):
        self.salida.setText("POSIBLE PERSONA NO CONOCIDA - PRECAUCION!!!")

class Css_stream(object):
    Css_mensaje_alarma = '''
            QTextEdit {
                background-color:white;
                border-left:5px solid orange;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        '''
    Css_label = '''
            color:rgb(100,100,100);
            font-weight:bold;
            font-size:12px;
        '''
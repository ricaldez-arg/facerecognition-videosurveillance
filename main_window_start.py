#!/usr/bin/env python
import sys
from os import path
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import csv
from gui import TabWindow
from gui import RecordVideo

class Dialogo(QtGui.QDialog):
    Tomato = "(255,99,71)"
    Orange = "(255,165,0)"
    DodgerBlue = "(0,191,255)"
    MediunSeaGreen = "(60,179,113)"
    Css_cbox = '''
                    QComboBox {
                        /*border: 1px solid gray;*/
                        border-radius: 3px;
                        padding: 1px 18px 1px 3px;
                        min-width: 6em;
                        font-size:14px;

                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        /*border-style: solid;
                        border: 1px solid #1e1e1e;
                        border-radius: 5;*/
                        padding: 1px 0px 1px 20px;

                    }
                    QComboBox:hover, QPushButton:hover{
                        border: 1px solid rgb(240,240,240,50%);
                        color: white;
                        font-weight:bold;
                    }
                    QComboBox:editable {
                        background: transparent;
                    }

                    QComboBox:!editable, QComboBox::drop-down:editable {
                         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                     stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                                     stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                    }
                    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                        stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                                        stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
                    }

                    QComboBox:on { /* shift the text when the popup opens */
                        padding-top: 3px;
                        padding-left: 4px;
                        selection-background-color: DarkGray;

                    }
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 15px;
                        border-left-width: 1px;
                        border-left-color: darkgray;
                        border-left-style: solid; /* just a single line */
                        border-top-right-radius: 3px; /* same radius as the QComboBox */
                        border-bottom-right-radius: 3px;
                    }
                    QComboBox::down-arrow {
                        image: url(./util/iconos/icons8-flecha-ampliar-26.png);
                        width:14px;
                        height:14px;
                    }

                    QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                        top: 1px;
                        left: 1px;color:red;
                    }'''

    Css_boton = '''
                    QPushButton {
                        background-color:rgb(60,179,113,60%);
                        background:transparent;
                        /*border-radius:1px;*/
                        color:solid gray;
                        font-size:15px;
                        font-weight:bold;
                    }
                    QPushButton:hover{
                        /*background-color:rgb(60,179,113,70%);*/
                        text-decoration:underline;
                        /*border-radius:5px;*/
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                        border-top:3px solid rgb(255,165,0,0%);
                        border-bottom:1px solid green;
                        
                    }
                    
                    '''
    Css_cancel = '''
                    QPushButton {
                        background-color:rgb(255,165,0,30%);
                        /*border-radius:1px;*/
                        color: solid gray;
                        font-size:15px;
                        font-weight:bold;
                        background:transparent;
                        
                    }
                    QPushButton:hover{
                        /*background-color:rgb(255,165,0,40%);*/
                        text-decoration:underline;
                        /*border-radius:5px;*/
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                        border-top:4px solid rgb(255,165,0,0%);
                        border-bottom:1px solid red;
                        
                    }
        '''
    Css_label = '''
                color:rgb(100,100,100);
                font-weight:bold;
                font-size:12px;
            '''

    def __init__(self,csv_path, parent = None):
        super(Dialogo, self).__init__(parent)
        self.csv_path = csv_path
        self.acepted = False
        self.fuente = None
    def setupUi(self):
        self.resize(431, 246)
        buttonBox = QtGui.QDialogButtonBox(self)
        buttonBox.setGeometry(QtCore.QRect(60, 170, 341, 32))
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort | QtGui.QDialogButtonBox.Ok)
        buttonBox.setObjectName("buttonBox")

        color = QtCore.Qt.green
        buttonBox.button(QDialogButtonBox.Ok).setText('Iniciar')
        buttonBox.button(QDialogButtonBox.Abort).setText('Cancelar')
        icono = QIcon('./util/iconos/checked.png')
        buttonBox.button(QDialogButtonBox.Ok).setIcon(icono)
        icono = QIcon('./util/iconos/x-button.png')
        buttonBox.button(QDialogButtonBox.Abort).setIcon(icono)
        buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(self.Css_boton)
        buttonBox.button(QDialogButtonBox.Abort).setStyleSheet(self.Css_cancel)

        label = QtGui.QLabel("Seleccione la camara", self)
        label.setGeometry(QtCore.QRect(30, 20, 161, 17))
        label.setObjectName("label")
        label.setStyleSheet(self.Css_label)

        self.label2 = QtGui.QLabel("", self)
        self.label2.setGeometry(QtCore.QRect(30, 90, 300, 50))
        self.label2.setObjectName("label2")
        self.label2.setStyleSheet(self.Css_label)

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(30, 50, 371, 27))
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentIndexChanged.connect(self.mostrar)
        self.comboBox.setStyleSheet(self.Css_cbox)

        self.camaras = []
        with open(self.csv_path) as File:
            reader = csv.DictReader(File)
            for row in reader:
                self.camaras.append(row)
        nombres = [row['nombre'] for row in self.camaras]
        self.comboBox.addItems(nombres)

        QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.accept_data)
        QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.reject_data)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Seleccion de camara")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.exec_()
    def accept_data(self):
        self.acepted = True
        self.accept()
    def reject_data(self):
        self.acepted = False
        self.reject()
    def mostrar(self,cu):
        row = self.camaras[cu]
        self.fuente = row['fuente']
        mensaje = 'Nombre:   %s\nFuente:   %s\nDescripcion:%s'%(row['nombre'],row['fuente'],row['descripcion'])
        self.label2.setText(mensaje)


def main(cascade_file_path):
    app = QApplication(sys.argv)
    dialogo = Dialogo('camaras.csv')
    dialogo.setupUi()
    dialogo.show()
    if not dialogo.acepted:
        sys.exit()
    dialogo.close()

    src = str(dialogo.fuente)
    if src.isdigit():
        src = int(src)

    #src='rtsp://admin:Password@192.168.1.64/doc/page/preview.asp'
    #src = 0
    #src = 'rtsp://admin:Password@192.168.43.108/'
    recorder = RecordVideo(src)
    data_path = './util/data/'
    output_dir = './grabaciones/'
    ex = TabWindow(recorder, data_path, cascade_file_path, output_dir)
    ex.show()
    ex.setCurrentIndex(0)
    sys.exit(app.exec_())

if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))+"/util/haarcascades"
    archivo = 'haarcascade_frontalface_default.xml'
    cascade_filepath = path.join(script_dir, archivo)

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)

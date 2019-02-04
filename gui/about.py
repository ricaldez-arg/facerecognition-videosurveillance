from PyQt4 import QtGui, QtCore, Qt
import sys
class About(QtGui.QVBoxLayout):

    Css_label = "color:rgb(100,100,100);font-weight:bold;font-size:16px;"
    def __init__(self, parent = None):
        super(About,self).__init__(parent)

        mensaje = 'PROYECTO DE GRADO / INFORMATICA - UMSS\n\n' \
                  'Autor: Ariel Ricaldez Gonzales\n' \
                  'Correo: ricaldez.arg@gmail.com\n\n' \
                  'Tutor: MSc. Patricia Romero.'

        titulo = QtGui.QLabel(mensaje)
        titulo.setStyleSheet(self.Css_label)
        titulo.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        titulo.setAlignment(QtCore.Qt.AlignCenter)


        pixmap = QtGui.QPixmap('./util/iconos/umss.png')
        pixmap = pixmap.scaledToHeight(50)
        label_umss = QtGui.QLabel("")
        label_umss.setPixmap(pixmap)
        label_umss.setAlignment(QtCore.Qt.AlignCenter)

        pixmap2 = QtGui.QPixmap('./util/iconos/fcyt.png')
        pixmap2 = pixmap2.scaledToHeight(50)
        label_fcyt = QtGui.QLabel("")
        label_fcyt.setPixmap(pixmap2)
        label_fcyt.setAlignment(QtCore.Qt.AlignCenter)

        pixmap3 = QtGui.QPixmap('./util/iconos/informatica.jpg')
        pixmap3 = pixmap3.scaledToHeight(50)
        label_informatica = QtGui.QLabel("")
        label_informatica.setPixmap(pixmap3)
        label_informatica.setAlignment(QtCore.Qt.AlignCenter)

        layoutbox = QtGui.QHBoxLayout()

        layoutbox.addWidget(QtGui.QLabel())
        layoutbox.addWidget(QtGui.QLabel())
        layoutbox.addWidget(label_umss)
        layoutbox.addWidget(label_informatica)
        layoutbox.addWidget(label_fcyt)
        layoutbox.addWidget(QtGui.QLabel())
        layoutbox.addWidget(QtGui.QLabel())
        layoutbox.setAlignment(QtCore.Qt.AlignVCenter)


        #self.addWidget(label_umss,0,0)
        #self.addWidget(label_informatica,0,1)
        #self.addWidget(label_fcyt,0,2)
        self.addWidget(QtGui.QLabel(''))
        self.addWidget(titulo)
        #self.addWidget(QtGui.QLabel(''))
        self.addLayout(layoutbox)
        self.addWidget(QtGui.QLabel(''))



    def startt(self):
        pass
    def stop(self):
        pass
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    Frame.setGeometry(200, 50, 700, 400)
    Frame.setLayout(About())
    Frame.show()
    sys.exit(app.exec_())
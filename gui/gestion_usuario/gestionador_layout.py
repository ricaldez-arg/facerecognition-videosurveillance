from PyQt4 import QtGui
from gestionador import Gestionador

class GestionadorLayout(QtGui.QVBoxLayout):
    def __init__(self,ruta_data, parent=None):
        super(GestionadorLayout,self).__init__(parent)

        self.ui = Gestionador(ruta_data)
        self.ui.inicio()
        self.ui.show()
        self.addWidget(self.ui)
    def stop(self):
        self.ui.stop()
    def startt(self):
        self.ui.startt()
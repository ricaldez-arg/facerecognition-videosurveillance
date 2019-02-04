
from PyQt4 import QtCore, QtGui
import os
import shutil

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Gestionador(QtGui.QFrame):

    def __init__(self,path,parent = None):
        super(Gestionador,self).__init__(parent)
        self.path_users = path
    def inicio(self):
        Frame = self
        self.label = QtGui.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(170, 80, 111, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setStyleSheet(EstiloGestion.Css_label)

        self.nombre = QtGui.QLineEdit(Frame)
        self.nombre.setGeometry(QtCore.QRect(290, 80, 201, 27))
        self.nombre.setObjectName(_fromUtf8("nombre"))
        self.nombre.setStyleSheet(EstiloGestion.Css_edit)

        self.agregar = QtGui.QPushButton(Frame)
        self.agregar.setGeometry(QtCore.QRect(500, 80, 87, 27))
        self.agregar.setObjectName(_fromUtf8("agregar"))
        self.agregar.setStyleSheet(EstiloGestion.Css_push_add)

        delete = QtGui.QIcon("./util/iconos/add-user.png")
        self.agregar.setIcon(delete)
        self.agregar.setIconSize(QtCore.QSize(25, 25))

        self.agregar.clicked.connect(self.__nuevo_usuario)

        self.usuarios = QtGui.QListView(Frame)
        self.usuarios.setGeometry(QtCore.QRect(290, 180, 301, 261))
        self.usuarios.setObjectName(_fromUtf8("usuarios"))
        self.usuarios.setStyleSheet(EstiloGestion.Css_listView)

        self.model = QtGui.QStringListModel()
        self.lista = QtCore.QStringList()
        self.model.setStringList(self.lista)
        self.usuarios.setModel(self.model)


        QtCore.QObject.connect(self.usuarios.selectionModel(),
                               QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
                               self.currentIndex)

        QtCore.QObject.connect(self.usuarios.model(),
                                QtCore.SIGNAL('dataChanged(QModelIndex, QModelIndex)'),
                               self.changed)

        labelg = QtGui.QLabel("", Frame)
        labelg.setGeometry(QtCore.QRect(290, 160, 25, 25))
        pixmap = QtGui.QPixmap('./util/iconos/family1.png')
        pixmap = pixmap.scaled(22, 20)
        msc = pixmap.mask()
        pixmap.fill(QtCore.Qt.gray)
        labelg.setPixmap(pixmap)
        labelg.setMask(msc)

        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(315, 160, 200, 25))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setStyleSheet(EstiloGestion.Css_label)

        self.eliminar = QtGui.QPushButton(Frame)
        self.eliminar.setGeometry(QtCore.QRect(490, 470, 100, 27))
        self.eliminar.setObjectName(_fromUtf8("eliminar"))
        self.eliminar.setStyleSheet(EstiloGestion.Css_push_del)

        delete = QtGui.QIcon("./util/iconos/user.png")
        self.eliminar.setIcon(delete)
        self.eliminar.setIconSize(QtCore.QSize(25, 25))

        self.eliminar.clicked.connect(self.__eliminar_usuario)

        self.retranslateUi(Frame)
        self.__cargar_usuarios()

        QtCore.QMetaObject.connectSlotsByName(Frame)
    @QtCore.pyqtSlot("QItemSelection, QItemSelection")
    def currentIndex(self,a,b):
        index = self.usuarios.currentIndex()
        self.anterior = str(index.data().toString())

    @QtCore.pyqtSlot("QModelIndex, QModelIndex")
    def changed(self, new, old):
        nombre = str(new.data().toString())

        rutas = os.listdir(self.path_users)
        try:
            if nombre in rutas:
                reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                                   'Ya se encuentra el usuario:\n %s\n Intenta con otro nombre.' % nombre,
                                                   QtGui.QMessageBox.Ok)
                if reply == QtGui.QMessageBox.Ok:
                    self.__cargar_usuarios()
                    return
            anterior = os.path.join(self.path_users,self.anterior)
            nuevo = os.path.join(self.path_users,nombre)
            os.rename(anterior,nuevo)
            print "se ha cambiado en nombre de usuario: ["+self.anterior+"] con: [ "+nombre+"]"
        except Exception as ex:
            print "ha ocurrido un error al cambiar el nombre: " + str(ex.args)
        self.__cargar_usuarios()

    def __eliminar_usuario(self):
        index = self.usuarios.currentIndex()
        nombre = str(index.data().toString())

        try:
            if nombre == "":
                reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                                   'Primero debes seleccionar un usuario de la lista',
                                                   QtGui.QMessageBox.Ok)
                if reply == QtGui.QMessageBox.Ok:
                    return
            ruta = os.path.join(self.path_users, nombre)
            fotos = os.listdir(ruta)
            mensaje = 'Esta seguro que desea eliminar al usuario:\n%s\nque tiene %d fotos de entrenamiento?'%(nombre,len(fotos))
            reply = QtGui.QMessageBox.question(self, 'Desea continuar?',mensaje,
                      QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                #removed = os.removedirs(ruta)
                shutil.rmtree(ruta)
                print "usuario: "+nombre+" [BORRADO] "

        except Exception as ex:
            print "[NO SE PUDO BORRAR ]"+str(ex.args)
        self.__cargar_usuarios()


    def __cargar_usuarios(self):
        self.lista = QtCore.QStringList()
        rutas = os.listdir(self.path_users)
        for ruta in rutas:
            self.lista.append(ruta)
        self.lista.sort()
        self.model.setStringList(self.lista)

    def __nuevo_usuario(self):
        nombre = str(self.nombre.text())
        try:
            if nombre == "":
                reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                                   'Escribe un nombre de usuario en el cuadro de texto',
                                                   QtGui.QMessageBox.Ok)
                if reply == QtGui.QMessageBox.Ok:
                    return
            if nombre in os.listdir(self.path_users):
                reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                                   'Ya se encuentra el usuario:\n %s\n Intenta con otro nombre.'%nombre,
                                                   QtGui.QMessageBox.Ok)
                if reply == QtGui.QMessageBox.Ok:
                    self.nombre.setText("")
                    return
            ruta = os.path.join(self.path_users,nombre)
            os.mkdir(ruta)
            self.__cargar_usuarios()
            self.nombre.setText("")
            print ruta
            print "usuario: " + nombre + " [CREADO]"
        except Exception as ex:
            print "Ocurrio algo inesperado" + str(ex.args)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.label.setText(_translate("Frame", "Nombre de usuario", None))
        self.agregar.setText(_translate("Frame", "Agregar", None))
        self.label_2.setText(_translate("Frame", "Lista de usuarios", None))
        self.eliminar.setText(_translate("Frame", "Eliminar", None))

    def startt(self):
        pass
    def stop(self):
        pass

class EstiloGestion(object):
    Css_label = "color:rgb(100,100,100);font-weight:bold;font-size:12px;"
    Css_push_add = '''
        QPushButton {
            background-color:rgb(60,179,113,80%);
            border-radius:2px;
            color:rgb(255,255,255,90%);
            /*font-weight:bold;*/
            font-size:15px;
        }
        QPushButton:hover{
            background-color:rgb(60,179,113,90%);
            border-radius:3px;
            border-top:2px solid rgb(60,179,113,0%);
            color:white;
            border-bottom:1px solid green;
        }'''
    Css_push_del = '''
        QPushButton {
            background-color:rgb(255,99,71,80%);
            background:transparent;
            border-radius:5px;
            color:rgb(100,100,100);
            font-size:15px;
        }
        QPushButton:hover{
            background-color:rgb(255,99,71,0%);
            border-radius:0px;
            color:rgb(255,99,71);
            border-top:2px solid rgb(255,99,71,0%);
            border-bottom:1px solid rgb(255,99,71);
        }'''
    Css_listView = '''
        QListView::item {
            border-bottom: 1px solid qlineargradient(spread:reflect, x1:0.00454545, y1:0.971591,
             x2:0, y2:0, stop:0 rgba(255, 255, 255, 255), 
             stop:0.0772727 rgba(239, 239, 239, 150), stop:1 rgba(255, 255, 255, 255));
            padding:1px;
        }
    
        QListView::item:alternate {
            background: #EEEEEE;
        }
    
        QListView::item:selected {
            border: 1px solid #6ea1f1;
        }
    
        QListView::item:selected:!active {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #aeb1f1, stop: 1 #567dbc);
        }
    
        QListView::item:selected:active {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0  #6ea1f1, stop: 1 #567dbc);
        }
    
        QListView::item:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #e7effd, stop: 1 #cbdaf1);
        }'''
    Css_edit = '''
        QLineEdit {
            border:1px solid; border-color:gray;border-radius:2px;
        }
        QLineEdit:focus{
            border:1px solid darkgray;
        }
        QLineEdit:hover{
            border:1px solid rgb(255,255,153);/*darkgray;*/
        }'''

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    #Frame = QtGui.QFrame

    ui = Gestionador('../../util/data')
    ui.inicio()
    ui.show()
    sys.exit(app.exec_())


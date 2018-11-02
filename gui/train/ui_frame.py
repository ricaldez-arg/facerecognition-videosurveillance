
import sys
import os

from PyQt4 import QtCore, QtGui,Qt
from video_layout import VideoLayout

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

class Ui_Frame(QtGui.QFrame):

    def __init__(self,recorder,cascade_path, parent=None):
        super(Ui_Frame,self).__init__(parent)
        self.recorder = recorder
        self.cascade_path = cascade_path

    def setupUi(self, data_path):
        self.data_path = data_path
        Frame = self
        #Frame.setObjectName(_fromUtf8("Frame"))
        #Frame.resize(757+50, 527+120)
        #Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        #Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.comboBox_integrantes = QtGui.QComboBox(Frame)
        self.comboBox_integrantes.setGeometry(QtCore.QRect(20, 40, 191, 27))
        self.comboBox_integrantes.setObjectName(_fromUtf8("comboBox_integrantes"))
        self.__loadIntegrantes(data_path)

        self.comboBox_integrantes.currentIndexChanged.connect(self.actualiza)

        self.label = QtGui.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(20, 20, 151, 17))
        self.label.setObjectName(_fromUtf8("label"))

        self.pushButton_capturar = QtGui.QPushButton(Frame)
        self.pushButton_capturar.setGeometry(QtCore.QRect(240, 40, 87, 27))
        self.pushButton_capturar.setObjectName(_fromUtf8("pushButton_capturar"))
        self.pushButton_capturar.clicked.connect(self.capturar)

        #self.pushButton_capturaAutomatica = QtGui.QPushButton(Frame)
        self.pushButton_capturaAutomatica = QtGui.QPushButton()
        self.pushButton_capturaAutomatica.setGeometry(QtCore.QRect(340, 40, 121, 27))
        self.pushButton_capturaAutomatica.setObjectName(_fromUtf8("pushButton_capturaAutomatica"))

        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(510, 50, 161, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_help = QtGui.QLabel(Frame)
        self.label_help.setGeometry(QtCore.QRect(10, 460, 701, 51))
        self.label_help.setTextFormat(QtCore.Qt.PlainText)
        self.label_help.setObjectName(_fromUtf8("label_help"))

        self.groupBox = QtGui.QGroupBox(Frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 491, 381))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))

        self.widget_video = QtGui.QWidget(self.groupBox)
        self.widget_video.setGeometry(QtCore.QRect(10, 30, 480, 320))
        self.widget_video.setObjectName(_fromUtf8("widget_video"))
        self.videoLayout()


        self.treeView = QtGui.QTreeView(Frame)
        self.treeView.setGeometry(QtCore.QRect(510, 70, 241, 401))
        self.treeView.setObjectName(_fromUtf8("treeView"))

        self.model = QtGui.QDirModel()
        self.treeView.setModel(self.model)

        QtCore.QObject.connect(self.treeView.selectionModel(), QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
                               self.select)

        self.actualiza(0)

        self.label_p = QtGui.QLabel(Frame)
        self.label_p.setGeometry(QtCore.QRect(520, 480, 150, 17))
        self.label_p.setObjectName(_fromUtf8("label_p"))

        self.label_preview = QtGui.QLabel(Frame)
        self.label_preview.setGeometry(QtCore.QRect(520, 500, 140, 140))
        self.label_preview.setObjectName(_fromUtf8("label_preview"))

        self.button_delete = QtGui.QPushButton(Frame)
        self.button_delete.setGeometry(QtCore.QRect(700,500,100,30))
        self.button_delete.setObjectName(_fromUtf8("button_delete"))
        self.button_delete.clicked.connect(self.eliminar)

        self.button_delete_all = QtGui.QPushButton(Frame)
        self.button_delete_all.setGeometry(QtCore.QRect(700, 600, 100, 30))
        self.button_delete_all.setObjectName(_fromUtf8("button_delete_all"))
        self.button_delete_all.clicked.connect(self.eliminar_todo)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    @QtCore.pyqtSlot("QItemSelection, QItemSelection")
    def select(self, selected, deselected):
        #print(selected)
        #print(deselected)
        self.showPreview()

    def showPreview(self):
        currentElement = self.treeView.currentIndex()
        filepath = self.model.filePath(currentElement)
        print filepath
        pixmap = QtGui.QPixmap(filepath)
        pixmap = pixmap.scaledToHeight(140)#QtCore.Qt.KeepAspectRatio
        self.label_preview.setPixmap(pixmap)

    def eliminar(self):
        currentElement = self.treeView.currentIndex()
        filepath = self.model.filePath(currentElement)
        file =  os.path.basename(str(filepath))
        try:
            reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                         'Esta seguro que desea elminar el archivo:\n   %s'%file,
                                          QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                removed = os.remove(filepath)
                print "[BORRADO] " + file
            #else:
                #do something if no

        except Exception as ex:
            print "[NO BORRADO ]"+str(ex.args)
        self.actualiza(0)
    def eliminar_todo(self):
        user = str(self.comboBox_integrantes.currentText())
        user_path = os.path.join(self.data_path, user)
        reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                           'Esta seguro que desea elminar toda las imagenes de:\n       %s' % user,
                                           #"Continuar","Cancelar")
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            try:
                for element in os.listdir(user_path):
                    filepath = os.path.join(user_path, element)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                print "[BORRADO TODOS LOS ARCHIVOS DE: ] " + user_path
            except Exception as ex:
                print "[ERROR AL BORRAR] " + str(ex.args)

        self.actualiza(0)

    def actualiza(self,index):
        user = str(self.comboBox_integrantes.currentText())
        self.model.refresh()
        self.model.sort(2)
        self.user_path = os.path.join(self.data_path,user)
        self.treeView.setRootIndex(self.model.index(self.user_path))
        #self.model.sort(2)

    def capturar(self):
        usuario = str(self.comboBox_integrantes.currentText())
        self.layout.capturar(usuario)

        #self.treeView.repaint()
        self.actualiza(0)

    def videoLayout(self):
        #cascade_path = 'haarcascade_frontalface_default.xml'
        #self.layout = VideoLayout(self.data_path, cascade_path)
        self.layout = VideoLayout(self.recorder,self.data_path,self.cascade_path)
        self.widget_video.setLayout(self.layout)


    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.label.setText(_translate("Frame", "Nombre del integrante", None))
        self.pushButton_capturar.setText(_translate("Frame", "Capturar", None))
        self.pushButton_capturaAutomatica.setText(_translate("Frame", "CapturaAutomatica", None))
        self.label_2.setText(_translate("Frame", "Modelos Capturados", None))
        self.label_help.setText(_translate("Frame", "Con la opcion \"Capturar\" se captura imagenes de uno en uno. \n",
                                           None))
        #self.label_help.setText(_translate("Frame", "Con la opcion \"Capturar\" se captura imagenes de uno en uno. \n"
#"Con la opcion \"CapturaAutomatica\" se captura 100 imagenes de manera automatica", None))
        self.groupBox.setTitle(_translate("Frame", "Video", None))
        self.label_p.setText(_translate("Frame","Previsualizacion",None))
        self.button_delete.setText(_translate("Frame","Eliminar",None))
        self.button_delete_all.setText(_translate("Frame","Eliminar todo",None))

    def __loadIntegrantes(self,ruta):
        integrantes = os.listdir(ruta)
        try:
            integrantes = os.listdir(ruta)
        except:
            print "no se ha podido cargar los integrantes"
        self.comboBox_integrantes.addItems(integrantes)
    def start(self):
        self.layout.start()
    def stop(self):
        self.layout.stop()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    translator = QtCore.QTranslator(app)
    locale = QtCore.QLocale.system().name()
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)

    Frame = QtGui.QFrame()
    data_path = os.path.join(os.getcwd(), 'data')
    ui = Ui_Frame()
    ui.setupUi(data_path, Frame)
    Frame.show()
    sys.exit(app.exec_())


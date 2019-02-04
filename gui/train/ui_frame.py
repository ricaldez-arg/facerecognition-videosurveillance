
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

        self.comboBox_integrantes = QtGui.QComboBox(Frame)
        self.comboBox_integrantes.setGeometry(QtCore.QRect(20, 40, 191, 27))
        self.comboBox_integrantes.setObjectName(_fromUtf8("comboBox_integrantes"))
        self.comboBox_integrantes.setStyleSheet(Util.Css_combobox)

        self.__loadIntegrantes(data_path)
        self.comboBox_integrantes.currentIndexChanged.connect(self.actualiza)

        self.treeView = QtGui.QTreeView(Frame)
        self.treeView.setGeometry(QtCore.QRect(510, 70, 321, 401))
        self.treeView.setObjectName(_fromUtf8("treeView"))

        self.treeView.setStyleSheet(Util.Css_treeview)
        self.treeView.header().setStyleSheet(Util.Css_header_treeview)
        #self.model = QtGui.QDirModel()
        self.models = QtGui.QFileSystemModel()
        self.models.setRootPath(self.data_path)
        self.treeView.setModel(self.models)
        self.treeView.setSortingEnabled(True)
        self.treeView.resizeColumnToContents(0)
        self.treeView.resizeColumnToContents(1)
        self.treeView.hideColumn(2)

        QtCore.QObject.connect(self.treeView.selectionModel(),
                               QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
                               self.select)

        self.label = QtGui.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(20, 20, 141, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setStyleSheet(Util.Css_seleccion_usuario)

        line_label = QtGui.QLabel(Frame)
        line_label.setObjectName("line_label")
        line_label.setGeometry(QtCore.QRect(20, 70, 480, 5))
        line_label.setStyleSheet(Util.Css_line_label)

        self.label_2 = QtGui.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(510, 54, 161, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_2.setStyleSheet(Util.Css_label_lista)

        self.label_help = QtGui.QLabel(Frame)
        self.label_help.setGeometry(QtCore.QRect(10, 500, 480, 120))
        self.label_help.setTextFormat(QtCore.Qt.PlainText)
        self.label_help.setObjectName(_fromUtf8("label_help"))
        self.label_help.setStyleSheet(Util.Css_label_help)

        self.groupBox = QtGui.QGroupBox(Frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 491, 450))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))

        self.widget_video = QtGui.QWidget(self.groupBox)
        self.widget_video.setGeometry(QtCore.QRect(10, 30, 480, 350))
        self.widget_video.setObjectName(_fromUtf8("widget_video"))
        self.videoLayout()

        self.label_p = QtGui.QLabel(Frame)
        self.label_p.setGeometry(QtCore.QRect(520, 480, 150, 17))
        self.label_p.setObjectName(_fromUtf8("label_p"))
        self.label_p.setStyleSheet(Util.Css_seleccion_usuario)

        self.label_preview = QtGui.QLabel(Frame)
        self.label_preview.setGeometry(QtCore.QRect(520, 500, 140, 140))
        self.label_preview.setObjectName(_fromUtf8("label_preview"))
        self.label_preview.setStyleSheet(Util.Css_preview)

        self.pushButton_capturar = QtGui.QPushButton(Frame)
        self.pushButton_capturar.setGeometry(QtCore.QRect(380, 75, 120, 30))
        self.pushButton_capturar.setObjectName(_fromUtf8("pushButton_capturar"))

        capturar = QtGui.QIcon("./util/iconos/photo-camera.png")
        self.pushButton_capturar.setText("Capturar")
        self.pushButton_capturar.setIcon(capturar)
        self.pushButton_capturar.setIconSize(QtCore.QSize(26, 26))
        self.pushButton_capturar.setToolTip("Capturar")  # rgb(10, 173, 45)
        self.pushButton_capturar.setStyleSheet(Util.Css_pushbutom)

        self.pushButton_capturar.clicked.connect(self.capturar)
        self.pushButton_capturar.enterEvent = self.enter_push
        self.pushButton_capturar.leaveEvent = self.leave_push

        self.button_delete = QtGui.QPushButton(Frame)
        self.button_delete.setGeometry(QtCore.QRect(690,500,90,27))
        self.button_delete.setObjectName(_fromUtf8("button_delete"))
        self.button_delete.clicked.connect(self.eliminar)

        delete = QtGui.QIcon("./util/iconos/file.png")
        self.button_delete.setIcon(delete)
        self.button_delete.setIconSize(QtCore.QSize(25, 25))
        self.button_delete.setStyleSheet(Util.Css_push_del)

        self.button_delete_all = QtGui.QPushButton(Frame)
        self.button_delete_all.setGeometry(QtCore.QRect(690, 600, 120, 27))
        self.button_delete_all.setObjectName(_fromUtf8("button_delete_all"))
        self.button_delete_all.clicked.connect(self.eliminar_todo)

        deletea = QtGui.QIcon("./util/iconos/file_all.png")
        self.button_delete_all.setIcon(deletea)
        self.button_delete_all.setIconSize(QtCore.QSize(25, 25))
        self.button_delete_all.setStyleSheet(Util.Css_push_del_all)

        self.actualiza(0)
        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def inicializa_modelo(self):
        #self.model = QtGui.QDirModel()
        #self.treeView.setModel(self.model)
        #self.model.refresh()
        #self.model.reset()
        self.actualiza(0)

    @QtCore.pyqtSlot("QItemSelection, QItemSelection")
    def select(self, selected, deselected):
        self.showPreview()

    def showPreview(self):
        currentElement = self.treeView.currentIndex()
        filepath = self.models.filePath(currentElement)
        #filepath = self.model.filePath(currentElement)
        #print filepath
        pixmap = QtGui.QPixmap(filepath)
        pixmap = pixmap.scaledToHeight(140)
        self.label_preview.setPixmap(pixmap)

    def eliminar(self):
        currentElement = self.treeView.currentIndex()
        #filepath = self.model.filePath(currentElement)
        filepath = self.models.filePath(currentElement)
        file = os.path.basename(str(filepath))

        if file == "":
            reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                               'Primero debes seleccionar un archivo de la lista.',
                                               QtGui.QMessageBox.Ok)
            if reply == QtGui.QMessageBox.Yes:
                return
            return
        try:
            reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                         'Esta seguro que desea elminar el archivo:\n   %s'%file,
                                          QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                removed = os.remove(filepath)
                print "[BORRADO] " + file

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
        #self.model.refresh()
        #self.model.sort(2)
        #self.models.sort(2)
        self.user_path = os.path.join(self.data_path,user)
        #self.treeView.setRootIndex(self.model.index(self.user_path))
        self.treeView.setRootIndex(self.models.index(self.user_path))


        if not self.recorder.is_opened:
            self.layout.capture_widget.image_data_slot(self.recorder.outline)
            #self.detection_widget.image_data_slot(self.record_video.outline)

    def capturar(self):
        usuario = str(self.comboBox_integrantes.currentText())
        try:
            if usuario != "":
                self.layout.capturar(usuario)
                self.actualiza(0)
                return
            m = 'Debe existir un usuario\nvaya a la seccion de Gestion de usuario para crear uno.'
            reply = QtGui.QMessageBox.question(self, 'Desea continuar?',
                                               m, QtGui.QMessageBox.Ok)
            if reply == QtGui.QMessageBox.Ok:
                pass
        except Exception as ex:
            pass
            #print "Error: "+ str(ex.args)


    def videoLayout(self):
        self.layout = VideoLayout(self.recorder,self.data_path,self.cascade_path)
        self.widget_video.setLayout(self.layout)


    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.label.setText(_translate("Frame", "Nombre del integrante", None))
        self.pushButton_capturar.setText(_translate("Frame", "Capturar", None))
        #self.pushButton_capturaAutomatica.setText(_translate("Frame", "CapturaAutomatica", None))
        self.label_2.setText(_translate("Frame", "Modelos Capturados", None))
        ayuda = "Ayuda:\n" \
                "1. Debe aparecer el rostro de una sola persona en la pantalla\n" \
                "   enmarcada dentro de un rectangulo color verde.\n" \
                "2. Se debe presionar el boton <<Capturar>>, con esto debe \n" \
                "   aparecer un archivo en formato .pgm de la imagen capturado\n" \
                "   en la seccion Modelos capturados.\n"
        self.label_help.setText(_translate("Frame", ayuda,
                                           None))
        #self.groupBox.setTitle(_translate("Frame", "Video", None))
        self.label_p.setText(_translate("Frame","Previsualizacion",None))
        self.button_delete.setText(_translate("Frame","Eliminar",None))
        self.button_delete_all.setText(_translate("Frame","Eliminar todo",None))

    def __loadIntegrantes(self,ruta):
        try:
            integrantes = os.listdir(ruta)
            integrantes.sort()
            self.comboBox_integrantes.clear()
            self.comboBox_integrantes.addItems(integrantes)
        except Exception as ex:
            print "no se ha podido cargar los integrantes"
    def start(self):
        self.__loadIntegrantes(self.data_path)
        self.layout.start()
        self.actualiza(0)
    def stop(self):
        self.layout.stop()

    def enter_push(self,event):
        self.pushButton_capturar.setIconSize(QtCore.QSize(26, 26))
        self.pushButton_capturar.setGeometry(QtCore.QRect(379, 75, 121, 31))
    def leave_push(self,event):
        self.pushButton_capturar.setIconSize(QtCore.QSize(26, 26))
        self.pushButton_capturar.setGeometry(QtCore.QRect(380, 75, 120, 30))

class Util(object):
    Css_treeview = '''
                QTreeView {
                    alternate-background-color: #fafafa; /*qlineargradient(spread:reflect, x1:0, 
                    y1:1, x2:0, y2:0, stop:0 rgba(174, 174, 174, 255), 
                    stop:0.0772727 rgba(229, 229, 229, 255), stop:1 rgba(255, 255, 255, 255));*/
                    background:white;
                    show-decoration-selected: 1;
                    color:solid LightGray;
                }
                QTreeView::item {
                border: 1px solid #d9d9d9;
                border-top-color: transparent;
                border-bottom-color: transparent;
                }

                QTreeView::item:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                    border: 1px solid #bfcde4;
                }

                QTreeView::item:selected {
                    border: 1px solid #567dbc;
                }

                QTreeView::item:selected:active{
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
                }

                QTreeView::item:selected:!active {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
                }
                QTreeView::branch {
                    background: palette(base);
                }
                QTreeView::header{
                    color:green;
                }
                '''
    Css_combobox = '''
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

    Css_pushbutom = '''
                QPushButton {
                    background-color:rgb(60,179,113,80%);
                    border-radius:3px;
                    color:solid gray;
                    font-size:15px;
                    color: rgb(245,245,245);
                }
                QPushButton:hover{
                    background-color:rgb(60,179,113,90%);
                    text-decoration:underline;
                    border-radius:5px;
                    color:white;
                    font-size:20px;
                    font-weight:bold;
                    border-top:2px solid rgb(255,165,0,0%);
                    border-bottom:1px solid green;
                }'''
    Css_seleccion_usuario = "color:rgb(0,0,0,30%);font-weight:bold;font-size:12px;"
    Css_label_help = "border:1px solid LightGray;border-left: 2px solid orange;\
                            border-radius:5px;;font-weight:normal;\
                            background-color:rgb(230,230,230);"
    Css_line_label = "border-bottom:1px solid darkgray;background-color:transparent;"
    Css_label_lista = "color:rgb(0,0,0,60%);font-weight:bold;font-size:12px;"
    Css_header_treeview = "QWidget {font-weight:bold;color:DarkGray;background:transparent;}"
    Css_preview = "background-color:rgb(240,240,240,50%);border-radius:5px;border:2px solid rgb(255,255,255,70%);"

    Css_push_del = '''
                    QPushButton {
                        background-color:rgb(255,165,0,50%);
                        background:transparent;
                        border-radius:5px;
                        color:solid gray;
                        font-size:15px;
                    }
                    QPushButton:hover{
                        background-color:rgb(255,165,0,0%);
                        border-radius:5px;
                        color: rgb(255,100,0);
                        font-size:20px;
                        font-weight:bold;
                        border-top:2px solid rgb(255,165,0,0%);
                        border-bottom:1px solid rgb(255,165,0);
                    }'''
    Css_push_del_all = '''
                    QPushButton {
                        background-color:rgb(255,99,71,50%);
                        background:transparent;
                        border-radius:5px;
                        color:solid gray;
                        font-size:15px;
                    }
                    QPushButton:hover{
                        background-color:rgb(255,99,71,0%);
                        text-decoration:underline;
                        border-radius:5px;
                        color:red;
                        font-size:20px;
                        font-weight:bold;
                        border-top:2px solid rgb(255,99,71,0%);
                        border-bottom:1px solid rgb(255,99,71,80%);
                    }'''


if __name__ == "__main__":
    sys.path.append("..")
    from record_video import RecordVideo

    app = QtGui.QApplication(sys.argv)

    translator = QtCore.QTranslator(app)
    locale = QtCore.QLocale.system().name()
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)

    recorder = RecordVideo(0)
    cascade_path = "../../util/haarcascades/haarcascade_frontalface_default.xml"

    Frame = QtGui.QFrame()
    #data_path = os.path.join(os.getcwd(), 'data')
    data_path = "../../util/data/"
    ui = Ui_Frame(recorder, cascade_path)
    ui.setupUi(data_path)
    Frame.show()
    sys.exit(app.exec_())


import sys
from os import path
from PyQt4.QtGui import *
from gui import TabWindow
from gui import RecordVideo

def main(cascade_file_path):
    app = QApplication(sys.argv)
    recorder = RecordVideo(0)
    data_path = './util/data/'
    ex = TabWindow(recorder, data_path, cascade_file_path)
    #ex.setCentralWidget(main_widget)
    ex.setGeometry(200, 50, 850, 700)
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))+"/util/haarcascades"
    archivo = 'haarcascade_frontalface_default.xml'
    cascade_filepath = path.join(script_dir, archivo)

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)
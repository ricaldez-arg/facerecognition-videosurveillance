from imutils.video import VideoStream
import imutils
import cv2

class DetectorRostro(object):
    #ruta del archivo modelo entrenado
    #'./haarcascades/haarcascade_frontalface_default.xml'
    def __init__(self, rutaModelo='./util/haarcascades/haarcascade_frontalface_default.xml'):
        self.modeloRostro = cv2.CascadeClassifier(rutaModelo)

    def detectar(self,imagen):
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        rostrosp = self.modeloRostro.detectMultiScale(grises,1.3,5)
        #rostrosp, num = self.modeloRostro.detectMultiScale2(grises, 1.3,5)
        rostrosp, a,b = self.modeloRostro.detectMultiScale3(grises,scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE,outputRejectLevels = True)
        rostrosc = [imagen[y:y+h, x:x+w] for (x,y,w,h) in rostrosp]
        return rostrosp, rostrosc
def ini(camera, detector):
    while True:
        #ret, img = camera.read()
        img = camera.read()
        img = imutils.resize(img, width=750)
        #img = cv2.resize(img, (0, 0), None, .25, .25)
        pts, cds = detector.detectar(img)

        for (x,y,w,h) in pts:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

        cv2.imshow("rec",img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


if __name__ == '__main__':

    #camera = cv2.VideoCapture()
    #camera.open('rtsp://admin:Password@192.168.1.64/Streaming/channels/2')
    #camera.open('rtsp://admin:Password@192.168.1.64/doc/page/preview.asp')
    #src = 'rtsp://admin:Password@192.168.1.64/Streaming/channels/2'
    src = 'rtsp://admin:Password@192.168.1.64/doc/page/preview.asp'
    camera = VideoStream(src).start()
    detector = DetectorRostro('./haarcascades/haarcascade_frontalface_default.xml')
    ini(camera,detector)
    #camera.release()
    cv2.destroyAllWindows()



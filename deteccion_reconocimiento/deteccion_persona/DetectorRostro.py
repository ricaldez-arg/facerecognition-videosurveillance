
import face_recognition
import cv2

class DetectorRostro(object):
    def __init__(self, rutaModelo='./util/haarcascades/haarcascade_frontalface_default.xml', method = "cascade"):
        if method != "cascade":
            #hog o cnn
            self.method = method
        else:
            self.method = None
            self.modeloRostro = cv2.CascadeClassifier(rutaModelo)

    def detectar(self,imagen):

        if self.method:
            rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model=self.method)
            rostrosp = [(le, to, ri, bo) for (to, ri, bo, le) in boxes]
        else:
            grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            grises = cv2.equalizeHist(grises)

            rostrosp = self.modeloRostro.detectMultiScale(grises,1.1,3)# ,minSize=(30,30))
            rostrosp = [(x,y,x+w,y+h) for (x,y,w,h) in rostrosp]

        rostrosc = [imagen[y:yf, x:xf] for (x, y, xf, yf) in rostrosp]
        return rostrosp, rostrosc

def main(camara, detectorc,detectorh,detectorcnn):
    '''import os
    imagenes = os.listdir('./original_hog/')
    for imgr in imagenes:
        img = cv2.imread(os.path.join('./original_hog',imgr))
        imgc = img.copy()
        imgcn = img.copy()
        ps,rs = detectorc.detectar(imgc)
        for (x,y,xf,yf) in ps:
            cv2.rectangle(imgc,(x,y),(xf,yf),(0,255,0),2)
        ps, rs = detectorh.detectar(img)
        for (x,y,xf,yf) in ps:
            cv2.rectangle(img,(x,y),(xf,yf),(0,255,0),2)
            cv2.rectangle(imgcn, (x-3, y-3), (xf+3, yf+3), (0, 255, 0), 2)
        filetaphc = './cnn-hog/c'+imgr
        filetaphh = './cnn-hog/h' + imgr
        filetaphcn = './cnn-hog/cn' + imgr
        cv2.imwrite(filetaphc,imgc)
        cv2.imwrite(filetaphh, img)
        cv2.imwrite(filetaphcn, imgcn)'''
    contador = 65
    '''while True:
        img = camara.read()

        if img is None:
            return
        img = imutils.resize(img, width=720)
        imgc = img.copy()
        imgh = img.copy()
        imgcnn = img.copy()
        puntos, rostros = detectorc.detectar(imgc)

        for (x,y,xf,yf) in puntos:
            cv2.rectangle(imgc,(x,y),(xf,yf),(0,255,0),2)

        puntos, rostros = detectorh.detectar(imgh)
        for (x,y,xf,yf) in puntos:
            cv2.rectangle(imgh,(x,y),(xf,yf),(0,255,0),2)

        puntos, rostros = detectorcnn.detectar(imgcnn)
        for (x, y, xf, yf) in puntos:
            cv2.rectangle(imgcnn, (x, y), (xf, yf), (0, 255, 0), 2)
        fc = './ambos/'+ str(contador) + 'c.jpg'
        fh = './ambos/' + str(contador) + 'h.jpg'
        fcn = './ambos/' + str(contador) + 'cn.jpg'
        contador +=1
        cv2.imwrite(fc,imgc)
        cv2.imwrite(fh,imgh)
        cv2.imwrite(fcn,imgcnn)
        cv2.imshow('cas', imgc)
        cv2.imshow('hog', imgh)
        cv2.imshow('cnn', imgcnn)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break'''
    '''while True:
        img = camara.read()

        if img is None:
            return
        img = imutils.resize(img, width=720)
        imgco = img.copy()
        imgc = img.copy()
        puntos, rostros = detectorc.detectar(imgc)

        for (x,y,xf,yf) in puntos:
            cv2.rectangle(imgc,(x,y),(xf,yf),(0,255,0),2)

        puntos, rostros = detectorh.detectar(img)
        for (x,y,xf,yf) in puntos:
            cv2.rectangle(img,(x,y),(xf,yf),(0,255,0),2)

        fc = './ambos/'+ str(contador) + 'c.jpg'
        fh = './ambos/' + str(contador) + 'h.jpg'
        ft = './original_hog/' + str(contador) + '.jpg'
        contador +=1
        #cv2.imwrite(fc,imgc)
        #cv2.imwrite(fh,imgh)
        cv2.imwrite(ft,imgco)
        cv2.imshow('cas', imgc)
        cv2.imshow('hog', img)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    camara.stop()'''


    while True:
        img = camara.read()

        if img is None:
            return
        img = imutils.resize(img, width=720)
        puntos, rostros = detectorc.detectar(img)

        for (x, y, xf, yf) in puntos:

            cv2.rectangle(img, (x, y), (xf, yf), (0, 255, 0), 2)
        cv2.imshow('live', img)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    camara.stop()

def main2(imgs, detector):
    detecciones = 0
    falsas = 0
    for imgr in imgs:
        im = '../../../operaciones_video/images/im'
        imgr = os.path.join(im,imgr)
        print imgr
        img = cv2.imread(imgr)
        puntos, rostros = detector.detectar(img)
        if len(puntos) > 1:
            falsas += len(puntos)-1
        for (x, y, xf, yf) in puntos:
            detecciones += 1
            cv2.rectangle(img, (x, y), (xf, yf), (0, 255, 0), 2)
        cv2.imshow('live', img)

        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    print detecciones
    print falsas


if __name__ == '__main__':
    from imutils.video import VideoStream
    import imutils
    import os
    src = 'rtsp://admin:Password@192.168.43.108/'
    #src = 0

    #camara = VideoStream(src).start()
    ruta = '../../util/haarcascades/haarcascade_frontalface_default.xml'
    detectorc = DetectorRostro(ruta)
    detectorh = DetectorRostro(ruta, 'hog')
    detectorcnn = DetectorRostro(ruta, 'cnn')
    #main(camara, detectorc,detectorh,detectorcnn)
    main2(os.listdir('../../../operaciones_video/images/im/'),detectorcnn)


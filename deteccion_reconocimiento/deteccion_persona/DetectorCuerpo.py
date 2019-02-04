import cv2

class DetectorCuerpo(object):

    def __init__(self,rutaModelo = './deteccion_persona/haarcascades/fullbody.xml'):
        self.modeloCuerpo = cv2.CascadeClassifier(rutaModelo)

    def detectar(self, imagen):
        grises = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        cuerposp = self.modeloCuerpo.detectMultiScale(grises,1.3,5)
        cuerposc = [imagen[y:y+h,x:x+w] for (x,y,w,h) in cuerposp]

        return cuerposp, cuerposc
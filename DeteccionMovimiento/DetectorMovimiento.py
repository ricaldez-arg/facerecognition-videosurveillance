import cv2
class DetectorMovimiento(object):
    def __init__(self,sustractor=None, metodo='GSOC'):
        if sustractor:
            self.sustractor = sustractor
        elif metodo:
            self.sustractor = self.crearSustractor(metodo)
    def crearSustractor(self, metodo):
        sustractor = cv2.bgsegm.createBackgroundSubtractorGSOC()
        if metodo == 'CNT':
            sustractor = cv2.bgsegm.createBackgroundSubtractorCNT()
        elif metodo == 'LSBP':
            sustractor = cv2.bgsegm.createBackgroundSubtractorLSBP()
        elif metodo == 'MOG2':
            sustractor = cv2.createBackgroundSubtractorMOG2()

        return sustractor
        
    def detectar(self, image):
        self.imagen = image
        mascaraPrimerPlano = self.sustractor.apply(image)
        contornos = mascaraPrimerPlano.copy()
        im2, contornos, h = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        """for contorno in contornos:
            if cv2.contourArea(contorno) < 500:
                continue
            (x,y,w,h) = cv2.boundingRect(contorno)
            cv2.rectangle(image,x,y,(0,0,255),2)"""
        #ret = [contorno for contorno in contornos if cv2.contourArea(contorno) >= 500
        puntosRecta = [cv2.boundingRect(contorno) for contorno in contornos if cv2.contourArea(contorno) >= 500]
        #cortar = lambda (x,y,w,h):image[y:y+h,x:x+w]
        #cuadros = map(cortar,puntosRecta)
        cuadros = [image[y:y+h,x:x+w] for (x,y,w,h) in puntosRecta]
        return (puntosRecta, cuadros)
        """for r in ret:
            (x,y,w,h) = cv2.boundingRect(r)
            ret2 = image[y:y+h,x:x+w]
            cv2.imshow("cut",ret2)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)"""

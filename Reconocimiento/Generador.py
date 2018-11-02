import os
import cv2

class Generador(object):
    def __init__(self,ruta_datos):
        self.ruta_modelos =ruta_datos
    def guardar(self,nombre,imagen):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        ds = os.path.join(self.ruta_modelos, nombre)
        data = os.listdir(ds)
        numero = 0
        if len(data) > 0:
            data = map(lambda x: int((x.split("."))[0]), data)
            data.sort(reverse=True)
            numero = data[0]+1
        archivo = str(numero) +'.pgm'
        ruta_archivo = os.path.join(ds,archivo)

        cv2.imwrite(ruta_archivo,imagen)

    

'''data = os.listdir('./data/ar')
data = map(lambda x: int((x.split("."))[0]),data)
data.sort(reverse=True)
print data[0]'''

import os
import cv2

class Generador(object):

    def __init__(self,ruta_datos):
        self.ruta_modelos =ruta_datos

    def guardar(self,nombre,imagen):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        imagen = cv2.resize(imagen, (200, 200), interpolation=cv2.INTER_LINEAR)

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

    def crear_usuario(self,usuario):
        try:
            if self.existe(usuario):
                return False
            else:
                ruta = os.path.join(self.ruta_modelos,usuario)
                os.mkdir(ruta)
                return True
        except:
            print "No se pudo crear el usuario."
            return False


    def existe(self,usuario):
        usuarios = os.listdir(self.ruta_modelos)
        if usuario not in usuarios:
            return False
        else:
            return True

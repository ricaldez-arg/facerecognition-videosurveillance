from alarma_consola import AlarmaConsola

class GestionAlarma():

    def __init__(self, alarmas=[]):
        alarmas.append(AlarmaConsola())
        self.alarmas = alarmas
    def add_alarma(self,alarma):
        self.alarmas.append(alarma)
    def activar(self, nivel=0):
        if nivel == 0:
            return self.activar0()
        elif nivel == 1:
            return self.activar1()
        elif nivel == 2:
            return self.activar2()
        else:
            return self.activar3()

    def activar0(self):
        for alarma in self.alarmas:
            alarma.activar0()

    def activar1(self):
        for alarma in self.alarmas:
            alarma.activar1()

    def activar2(self):
        for alarma in self.alarmas:
            alarma.activar2()

    def activar3(self):
        for alarma in self.alarmas:
            alarma.activar3()

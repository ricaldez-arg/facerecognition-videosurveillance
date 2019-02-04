import abc

class Notificador(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def activar0(self):
        raise NotImplementedError("Se debe implementar la funcion activar.")

    @abc.abstractmethod
    def activar1(self):
        raise NotImplementedError("Se debe implementar la funcion activar.")

    @abc.abstractmethod
    def activar2(self):
        raise NotImplementedError("Se debe implementar la funcion activar.")

    @abc.abstractmethod
    def activar3(self):
        raise NotImplementedError("Se debe implementar la funcion activar.")
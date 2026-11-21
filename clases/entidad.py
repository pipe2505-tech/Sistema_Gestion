
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: entidad.py
# DESCRIPCION: Clase abstracta general
# =====================================================

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta para las entidades del sistema."""

    def __init__(self, identificacion, nombre):
        self._identificacion = identificacion
        self._nombre = nombre
        self._activo = True

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @property
    def activo(self):
        return self._activo

    def cambiar_estado(self, estado):
        self._activo = bool(estado)

    @abstractmethod
    def validar(self):
        """Cada clase hija debe implementar sus validaciones."""
        pass

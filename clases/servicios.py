
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: servicio.py
# DESCRIPCION: Gestion de servicios especializados
# =====================================================

from abc import ABC, abstractmethod

from clases.entidad import Entidad
from excepciones.errores import ErrorServicio


class Servicio(Entidad, ABC):
    """Clase abstracta que representa los servicios."""

    def __init__(self, identificacion, nombre, precio_base):
        super().__init__(identificacion, nombre)

        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)):
            raise ErrorServicio("El precio debe ser numerico.")

        if precio_base <= 0:
            raise ErrorServicio("El precio debe ser mayor que cero.")

        self._precio_base = precio_base

    @property
    def precio_base(self):
        return self._precio_base

    def validar_duracion(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ErrorServicio("La duracion debe ser numerica.")

        if duracion <= 0:
            raise ErrorServicio("La duracion debe ser positiva.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0.19):
        """Calcula costos con parametros opcionales."""

        self.validar_duracion(duracion)

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ErrorServicio("Descuento no valido.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ErrorServicio("Impuesto no valido.")

        if not 0 <= descuento <= 1:
            raise ErrorServicio("Descuento fuera del rango permitido.")

        if not 0 <= impuesto <= 1:
            raise ErrorServicio("Impuesto fuera del rango permitido.")

        subtotal = self._precio_base * duracion
        valor_descuento = subtotal * descuento

        total = (subtotal - valor_descuento) * (1 + impuesto)

        return round(total, 2)

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar(self):
        pass


class ReservaSala(Servicio):
    """Servicio para reservar salas."""

    def __init__(self, identificacion, nombre, precio_base, capacidad):
        super().__init__(identificacion, nombre, precio_base)
        self._capacidad = capacidad
        self.validar()

    def validar(self):
        if not isinstance(self._capacidad, int) or isinstance(self._capacidad, bool) or self._capacidad <= 0:
            raise ErrorServicio("Capacidad de sala no valida.")

    def validar_asistentes(self, asistentes):
        if not isinstance(asistentes, int) or isinstance(asistentes, bool) or asistentes <= 0:
            raise ErrorServicio("Numero de asistentes no valido.")

        if asistentes > self._capacidad:
            raise ErrorServicio("Se supera la capacidad de la sala.")

    def describir(self):
        return (
            f"Sala: {self.nombre}. "
            f"Capacidad: {self._capacidad} personas."
        )


class AlquilerEquipo(Servicio):
    """Servicio para alquilar equipos."""

    def __init__(self, identificacion, nombre, precio_base, cantidad_disponible):
        super().__init__(identificacion, nombre, precio_base)

        self._cantidad_disponible = cantidad_disponible
        self.validar()

    def validar(self):
        if not isinstance(self._cantidad_disponible, int) or isinstance(self._cantidad_disponible, bool) or self._cantidad_disponible < 0:
            raise ErrorServicio("Cantidad de equipos no valida.")

    def validar_cantidad(self, cantidad):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise ErrorServicio("La cantidad debe ser positiva.")

        if cantidad > self._cantidad_disponible:
            raise ErrorServicio("No hay equipos suficientes.")

    def describir(self):
        return (
            f"Alquiler de equipos: {self.nombre}. "
            f"Disponibles: {self._cantidad_disponible}."
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria especializada."""

    def __init__(self, identificacion, nombre, precio_base, especialidad):
        super().__init__(identificacion, nombre, precio_base)

        self._especialidad = especialidad
        self.validar()

    def validar(self):
        if not isinstance(self._especialidad, str) or not self._especialidad.strip():
            raise ErrorServicio("La especialidad es obligatoria.")

    def describir(self):
        return (
            f"Asesoria: {self.nombre}. "
            f"Especialidad: {self._especialidad}."
        )

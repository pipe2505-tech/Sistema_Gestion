
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: reservas.py
# DESCRIPCION: Gestion de reservas 
# =====================================================


from datetime import datetime
from enum import Enum
from typing import Optional

from entidades import Cliente
from excepciones import (
    CalculoInconsistenteError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
    ValidacionError,
)
from logger_config import obtener_logger
from servicios import Servicio

logger = obtener_logger()


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:
    """Reserva de un servicio hecha por un cliente."""

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int,
        fecha_inicio: Optional[datetime] = None,
    ) -> None:
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.fecha_inicio = fecha_inicio
        self.estado: EstadoReserva = EstadoReserva.PENDIENTE
        self.total_calculado: Optional[float] = None

        self._validar_datos_iniciales()
        self._verificar_disponibilidad_servicio()
        logger.info(
            f"Reserva creada | ID={self.id_reserva} | Estado={self.estado.value} | "
            f"Duracion={self.duracion_horas}h"
        )
      
    def _validar_datos_iniciales(self) -> None:
        if not self.id_reserva or not str(self.id_reserva).strip():
            raise ReservaInvalidaError("El ID de la reserva es obligatorio.")
        if not isinstance(self.cliente, Cliente):
            raise ReservaInvalidaError(f"Reserva {self.id_reserva}: falta asociar un cliente válido.")
        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError(f"Reserva {self.id_reserva}: falta asociar un servicio válido.")
        if not isinstance(self.duracion_horas, (int, float)) or isinstance(self.duracion_horas, bool):
            raise ReservaInvalidaError(f"Reserva {self.id_reserva}: la duración debe ser numérica.")
        if self.duracion_horas <= 0:
            raise ReservaInvalidaError(f"Reserva {self.id_reserva}: la duración debe ser mayor que 0.")

    def _verificar_disponibilidad_servicio(self) -> None:
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' no está disponible."
            )
        try:
           
            self.servicio.validar_parametros(self.duracion_horas)
        except ValidacionError as exc:
            
            raise ReservaInvalidaError(
                f"Parámetros no válidos en reserva {self.id_reserva}: {exc}"
            ) from exc


  
    def confirmar(self) -> None:
        if self.estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar {self.id_reserva}: está '{self.estado.value}'."
            )
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.servicio.nombre}' ya no está disponible."
            )
        self.estado = EstadoReserva.CONFIRMADA
        logger.info(f"Reserva {self.id_reserva} confirmada")

    def cancelar(self, motivo: str = "Sin motivo") -> None:
        if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar {self.id_reserva}: está '{self.estado.value}'."
            )
        self.estado = EstadoReserva.CANCELADA
        logger.info(f"Reserva {self.id_reserva} cancelada. Motivo: {motivo}")

    def procesar(self, impuesto: Optional[float] = None, descuento: Optional[float] = None) -> float:
        try:
            if self.estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas confirmadas ({self.id_reserva} está "
                    f"'{self.estado.value}')."
                )
            total = self.servicio.calcular_costo(self.duracion_horas, impuesto, descuento)
        except SoftwareFJError:
            logger.error(f"Fallo al procesar la reserva {self.id_reserva}")
            raise
        except (TypeError, ValueError, ArithmeticError) as exc:
            raise CalculoInconsistenteError(
                f"Error calculando {self.id_reserva}: {exc}"
            ) from exc
        else:
            self.estado = EstadoReserva.PROCESADA
            self.total_calculado = total
            logger.info(f"Reserva {self.id_reserva} procesada. Total: ${total:,.2f}")
            return total
        finally:
            logger.info(f"Intento de procesar {self.id_reserva} terminado (estado: {self.estado.value})")

    def describir(self) -> str:
        total = f" | Total: ${self.total_calculado:,.2f}" if self.total_calculado is not None else ""
        return (f"Reserva {self.id_reserva} | {self.cliente.nombre} -> {self.servicio.nombre} "
                f"| {self.duracion_horas}h | {self.estado.value}{total}")

    def __str__(self) -> str:
        return self.describir()

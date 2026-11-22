
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: reserva.py
# DESCRIPCION: Administracion y gestion de reservas
# =====================================================

import logging
import math

from datetime import datetime
from enum import Enum
from typing import Optional

from clases.servicio import Servicio
from excepciones.errores import ErrorReserva, OperacionNoPermitida

logger = logging.getLogger("SoftwareFJ")


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:
    """Representa una reserva de un servicio realizada por un cliente."""

    def __init__(
        self,
        identificacion,
        cliente,
        servicio,
        duracion,
        fecha_inicio: Optional[datetime] = None
    ):

        # Validacion de identificacion
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ErrorReserva(
                "La identificacion de la reserva es obligatoria."
            )

        # Validacion del cliente
        if cliente is None or not hasattr(cliente, "activo"):
            raise ErrorReserva(
                "El cliente no es valido."
            )

        if not cliente.activo:
            raise ErrorReserva(
                "El cliente esta inactivo."
            )

        # Validacion del servicio
        if not isinstance(servicio, Servicio):
            raise ErrorReserva(
                "El servicio no es valido."
            )

        if not servicio.activo:
            raise ErrorReserva(
                "El servicio esta inactivo."
            )

        # Validacion de duracion
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise ErrorReserva(
                "La duracion debe ser un numero positivo y valido."
            )

        servicio.validar_duracion(duracion)

        # Validacion de fecha
        if fecha_inicio is not None and not isinstance(fecha_inicio, datetime):
            raise ErrorReserva(
                "La fecha de inicio no es valida."
            )

        # Atributos encapsulados
        self._identificacion = identificacion
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._fecha_inicio = fecha_inicio
        self._estado = EstadoReserva.PENDIENTE
        self._costo = None

        logger.info(
            "Reserva %s creada correctamente.",
            self._identificacion
        )

    # ================================================
    # PROPIEDADES
    # ================================================

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    # ================================================
    # VALIDACION DE DISPONIBILIDAD
    # ================================================

    def verificar_disponibilidad(self):

        if not self._cliente.activo:
            raise ErrorReserva(
                "El cliente esta inactivo."
            )

        if not self._servicio.activo:
            raise ErrorReserva(
                "El servicio no esta disponible."
            )

        self._servicio.validar_duracion(self._duracion)

    # ================================================
    # CONFIRMAR RESERVA
    # ================================================

    def confirmar(self):
        """Confirma una reserva pendiente."""

        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitida(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.verificar_disponibilidad()

        self._estado = EstadoReserva.CONFIRMADA

        logger.info(
            "Reserva %s confirmada.",
            self._identificacion
        )

    # ================================================
    # CANCELAR RESERVA
    # ================================================

    def cancelar(self, motivo="Sin motivo"):
        """Cancela una reserva pendiente o confirmada."""

        if self._estado in (
            EstadoReserva.CANCELADA,
            EstadoReserva.PROCESADA
        ):
            raise OperacionNoPermitida(
                "No se puede cancelar una reserva cancelada o procesada."
            )

        self._estado = EstadoReserva.CANCELADA

        logger.info(
            "Reserva %s cancelada. Motivo: %s",
            self._identificacion,
            motivo
        )

    # ================================================
    # PROCESAR RESERVA
    # ================================================

    def procesar(self, descuento=0, impuesto=0.19):
        """Calcula el costo y procesa una reserva confirmada."""

        try:

            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitida(
                    "Solo se pueden procesar reservas confirmadas."
                )

            self.verificar_disponibilidad()

            # Se utilizan argumentos con nombre para evitar
            # confusiones entre descuento e impuesto.
            total = self._servicio.calcular_costo(
                self._duracion,
                descuento=descuento,
                impuesto=impuesto
            )

            if (
                isinstance(total, bool)
                or not isinstance(total, (int, float))
                or not math.isfinite(total)
                or total <= 0
            ):
                raise ErrorReserva(
                    "El costo calculado no es valido."
                )

        except (ErrorReserva, OperacionNoPermitida):

            logger.exception(
                "Error procesando reserva %s.",
                self._identificacion
            )

            raise

        except (TypeError, ValueError, ArithmeticError) as error:

            logger.exception(
                "Error de calculo en reserva %s.",
                self._identificacion
            )

            raise ErrorReserva(
                "No fue posible calcular el costo de la reserva."
            ) from error

        else:

            self._costo = total
            self._estado = EstadoReserva.PROCESADA

            logger.info(
                "Reserva %s procesada. Costo: %.2f",
                self._identificacion,
                self._costo
            )

            return self._costo

        finally:

            logger.info(
                "Finalizo el intento de procesamiento de reserva %s.",
                self._identificacion
            )

    # ================================================
    # DESCRIPCION DE LA RESERVA
    # ================================================

    def describir(self):

        costo = (
            f"${self._costo:,.2f}"
            if self._costo is not None
            else "Pendiente de calcular"
        )

        return (
            f"Reserva: {self._identificacion} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duracion: {self._duracion} horas | "
            f"Estado: {self._estado.value} | "
            f"Costo: {costo}"
        )

    def __str__(self):
        return self.describir()


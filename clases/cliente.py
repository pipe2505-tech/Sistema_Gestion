
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: cliente.py
# DESCRIPCION: Gestion de clientes
# =====================================================

import re

from clases.entidad import Entidad
from excepciones.errores import ErrorCliente


class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)

        self._correo = correo
        self._telefono = telefono

        self.validar()

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def validar(self):
        """Valida la informacion personal del cliente."""

        if not self._identificacion or not str(self._identificacion).strip():
            raise ErrorCliente("La identificacion es obligatoria.")

        if not isinstance(self._nombre, str) or not self._nombre.strip():
            raise ErrorCliente("El nombre es obligatorio.")

        if not isinstance(self._correo, str):
            raise ErrorCliente("El correo debe ser texto.")

        patron = r"^[\w.-]+@[\w.-]+\.\w+$"

        if not re.match(patron, self._correo):
            raise ErrorCliente("El correo electronico no es valido.")

        telefono = str(self._telefono)

        if not telefono.isdigit() or len(telefono) < 7:
            raise ErrorCliente("El telefono debe tener al menos 7 digitos.")

        return True

    def __str__(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Identificacion: {self.identificacion} | "
            f"Correo: {self.correo}"
        )

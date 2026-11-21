
# =====================================================
# PROYECTO: SOFTWARE FJ
# ARCHIVO: test_sistema.py
# DESCRIPCION: Pruebas automaticas
# =====================================================

import unittest

from clases.cliente import Cliente
from clases.servicio import ReservaSala, AlquilerEquipo
from clases.reserva import Reserva

from excepciones.errores import ErrorCliente, ErrorServicio, ErrorReserva


class PruebasSoftwareFJ(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente(
            "1001",
            "Andres Castro",
            "andres@gmail.com",
            "3001234567"
        )

        self.sala = ReservaSala(
            "S001",
            "Sala principal",
            50000,
            20
        )

    def test_cliente_valido(self):
        self.assertEqual(self.cliente.nombre, "Andres Castro")

    def test_cliente_correo_invalido(self):
        with self.assertRaises(ErrorCliente):
            Cliente("1002", "Carlos", "correo", "3001234567")

    def test_servicio_valido(self):
        self.assertEqual(self.sala.precio_base, 50000)

    def test_precio_negativo(self):
        with self.assertRaises(ErrorServicio):
            AlquilerEquipo("E001", "Computador", -5000, 5)

    def test_calculo_costo(self):
        self.assertEqual(self.sala.calcular_costo(2), 119000)

    def test_creacion_reserva(self):
        reserva = Reserva("R001", self.cliente, self.sala, 2)
        self.assertEqual(reserva.estado, "Pendiente")

    def test_procesar_reserva(self):
        reserva = Reserva("R002", self.cliente, self.sala, 2)

        costo = reserva.procesar()

        self.assertEqual(costo, 119000)
        self.assertEqual(reserva.estado, "Confirmada")

    def test_descuento_invalido(self):
        reserva = Reserva("R003", self.cliente, self.sala, 2)

        with self.assertRaises(ErrorReserva):
            reserva.procesar(descuento=2)

    def test_cancelar_reserva(self):
        reserva = Reserva("R004", self.cliente, self.sala, 2)
        reserva.cancelar()

        self.assertEqual(reserva.estado, "Cancelada")


if __name__ == "__main__":
    unittest.main(verbosity=2)

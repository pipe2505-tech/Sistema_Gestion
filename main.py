
# =====================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: Programación 213023
# Fase 4 - Prácticas simuladas
# Proyecto: Sistema Integral de Gestión Software FJ
# =====================================================

from datetime import datetime


def mostrar_bienvenida():
    """Muestra la información inicial del sistema."""
    print("=" * 55)
    print(" SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print(" Gestion de clientes, servicios y reservas")
    print("=" * 55)
    print("Fecha de ejecucion:", datetime.now())
    print("Sistema iniciado correctamente.")


if __name__ == "__main__":
    mostrar_bienvenida()

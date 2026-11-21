
# =====================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# PROYECTO: SOFTWARE FJ
# ARCHIVO: errores.py
# DESCRIPCION: Excepciones personalizadas
# =====================================================

# Clase general para los errores del sistema
class ErrorSistema(Exception):
    """Representa un error general del sistema."""
    pass


# Error relacionado con los clientes
class ErrorCliente(ErrorSistema):
    """Controla errores en el registro de clientes."""
    pass


# Error relacionado con los servicios
class ErrorServicio(ErrorSistema):
    """Controla errores en los servicios."""
    pass


# Error relacionado con las reservas
class ErrorReserva(ErrorSistema):
    """Controla errores en las reservas."""
    pass


# Error para operaciones no permitidas
class OperacionNoPermitida(ErrorSistema):
    """Controla operaciones que no se pueden realizar."""
    pass

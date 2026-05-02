"""
Punto de exportación único para todos los modelos SQLAlchemy.
Importar modelos siempre desde aquí, no desde los archivos individuales.
"""
from .base_models import Bodega, Cliente, Producto, Puerto, Usuario
from .envio_models import Envio, EnvioMaritimo, EnvioTerrestre

__all__ = [
    "Usuario",
    "Cliente",
    "Producto",
    "Bodega",
    "Puerto",
    "Envio",
    "EnvioTerrestre",
    "EnvioMaritimo",
]
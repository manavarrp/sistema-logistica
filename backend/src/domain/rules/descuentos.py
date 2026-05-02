"""
Reglas de negocio de descuento por volumen.

Terrestre: > 10 unidades → 5% de descuento sobre el subtotal
Marítimo:  > 10 unidades → 3% de descuento sobre el subtotal
"""
from decimal import Decimal

_UMBRAL = 10
_DESCUENTO_TERRESTRE = Decimal("0.05")
_DESCUENTO_MARITIMO = Decimal("0.03")


def calcular_descuento_terrestre(cantidad: int, subtotal: Decimal) -> Decimal:
    """Retorna el monto de descuento para un envío terrestre."""
    return subtotal * _DESCUENTO_TERRESTRE if cantidad > _UMBRAL else Decimal("0")


def calcular_descuento_maritimo(cantidad: int, subtotal: Decimal) -> Decimal:
    """Retorna el monto de descuento para un envío marítimo."""
    return subtotal * _DESCUENTO_MARITIMO if cantidad > _UMBRAL else Decimal("0")
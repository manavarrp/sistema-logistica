"""
DTOs (Data Transfer Objects) de la capa de aplicación.

Los DTOs son estructuras de datos planas que viajan entre capas.
Separan el contrato interno de la aplicación del contrato HTTP (schemas Pydantic).

Regla: los use_cases reciben y retornan DTOs, nunca modelos SQLAlchemy ni schemas HTTP.
"""
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal



# ── ENVÍOS TERRESTRES ────────────────────────────────────────
@dataclass
class CrearEnvioTerrestreDTO:
    cliente_id: int
    producto_id: int
    cantidad_producto: int
    fecha_entrega: date
    placa: str
    numero_guia: str
    bodega_id: int


@dataclass
class EnvioTerrestreDTO:
    id: int
    cliente_id: int
    producto_id: int
    cantidad_producto: int
    fecha_registro: datetime
    fecha_entrega: date
    precio_unitario: Decimal
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    estado: str
    placa: str
    numero_guia: str
    bodega_id: int


# ── ENVÍOS MARÍTIMOS ─────────────────────────────────────────
@dataclass
class CrearEnvioMaritimoDTO:
    cliente_id: int
    producto_id: int
    cantidad_producto: int
    fecha_entrega: date
    numero_flota: str
    numero_guia: str
    puerto_id: int


@dataclass
class EnvioMaritimoDTO:
    id: int
    cliente_id: int
    producto_id: int
    cantidad_producto: int
    fecha_registro: datetime
    fecha_entrega: date
    precio_unitario: Decimal
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    estado: str
    numero_flota: str
    numero_guia: str
    puerto_id: int


# ── ESTADO ───────────────────────────────────────────────────
@dataclass
class CambiarEstadoDTO:
    envio_id: int
    nuevo_estado: str

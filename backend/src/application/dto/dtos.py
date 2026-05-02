"""
DTOs (Data Transfer Objects) de la capa de aplicación.

Los DTOs son estructuras de datos planas que viajan entre capas.
Separan el contrato interno de la aplicación del contrato HTTP (schemas Pydantic).

Regla: los use_cases reciben y retornan DTOs, nunca modelos SQLAlchemy ni schemas HTTP.
"""
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


# ── AUTH ─────────────────────────────────────────────────────
@dataclass
class RegistrarUsuarioDTO:
    email: str
    password: str
    nombre_completo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None


@dataclass
class RegistroConTokenDTO:
    cliente: "ClienteDTO"
    token: "TokenDTO"


@dataclass
class LoginDTO:
    email: str
    password: str


@dataclass
class TokenDTO:
    access_token: str
    token_type: str = "bearer"
    cliente_id: Optional[int] = None


# ── CLIENTES ─────────────────────────────────────────────────
@dataclass
class CrearClienteDTO:
    nombre_completo: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None


@dataclass
class ActualizarClienteDTO:
    nombre_completo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


@dataclass
class ClienteDTO:
    id: int
    nombre_completo: str
    email: str
    telefono: Optional[str]
    direccion: Optional[str]


# ── PRODUCTOS ────────────────────────────────────────────────
@dataclass
class CrearProductoDTO:
    tipo_producto: str
    precio_unitario: Decimal
    tipo_logistica: str  # terrestre | maritimo
    descripcion: Optional[str] = None


@dataclass
class ProductoDTO:
    id: int
    tipo_producto: str
    precio_unitario: Decimal
    tipo_logistica: str
    descripcion: Optional[str]


# ── BODEGAS ──────────────────────────────────────────────────
@dataclass
class CrearBodegaDTO:
    nombre: str
    ubicacion: str
    ciudad: Optional[str] = None
    pais: str = "Colombia"


@dataclass
class BodegaDTO:
    id: int
    nombre: str
    ubicacion: str
    ciudad: Optional[str]
    pais: str


# ── PUERTOS ──────────────────────────────────────────────────
@dataclass
class CrearPuertoDTO:
    nombre: str
    ubicacion: str
    pais: str
    ciudad: Optional[str] = None


@dataclass
class PuertoDTO:
    id: int
    nombre: str
    ubicacion: str
    ciudad: Optional[str]
    pais: str


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

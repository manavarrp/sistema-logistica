"""
Schemas Pydantic para validación de request/response.

Separados de los modelos SQLAlchemy intencionalmente:
- Los modelos representan la BD
- Los schemas representan el contrato de la API
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── AUTH ─────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    """
    El registro crea usuario + cliente en una sola operación atómica.
    nombre_completo es requerido porque el perfil de cliente
    se crea al mismo tiempo que el usuario.
    """
    email: EmailStr
    password: str = Field(..., min_length=6)
    nombre_completo: str = Field(..., min_length=3, max_length=200)
    telefono: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Incluye cliente_id para que el frontend pueda asociar
    envíos al cliente autenticado sin petición adicional.
    """
    access_token: str
    token_type: str = "bearer"
    cliente_id: int


class UsuarioResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


# ── CLIENTES ─────────────────────────────────────────────────
class ClienteCreate(BaseModel):
    nombre_completo: str = Field(..., min_length=3, max_length=200)
    email: EmailStr
    telefono: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = None


class ClienteUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=200)
    telefono: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = None


class ClienteResponse(BaseModel):
    id: int
    nombre_completo: str
    email: str
    telefono: Optional[str]
    direccion: Optional[str]

    model_config = {"from_attributes": True}


class RegisterResponse(BaseModel):
    cliente: ClienteResponse
    token: TokenResponse


# ── PRODUCTOS ────────────────────────────────────────────────
class ProductoCreate(BaseModel):
    tipo_producto: str = Field(..., max_length=100)
    precio_unitario: Decimal = Field(..., gt=0)
    tipo_logistica: Literal["terrestre", "maritimo"]
    descripcion: Optional[str] = None


class ProductoUpdate(BaseModel):
    tipo_producto: Optional[str] = Field(None, max_length=100)
    precio_unitario: Optional[Decimal] = Field(None, gt=0)
    descripcion: Optional[str] = None


class ProductoResponse(BaseModel):
    id: int
    tipo_producto: str
    precio_unitario: Decimal
    tipo_logistica: str
    descripcion: Optional[str]

    model_config = {"from_attributes": True}


# ── BODEGAS ──────────────────────────────────────────────────
class BodegaCreate(BaseModel):
    nombre: str = Field(..., max_length=200)
    ubicacion: str
    ciudad: Optional[str] = Field(None, max_length=100)
    pais: str = Field(default="Colombia", max_length=100)


class BodegaResponse(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    ciudad: Optional[str]
    pais: str

    model_config = {"from_attributes": True}


# ── PUERTOS ──────────────────────────────────────────────────
class PuertoCreate(BaseModel):
    nombre: str = Field(..., max_length=200)
    ubicacion: str
    ciudad: Optional[str] = Field(None, max_length=100)
    pais: str = Field(..., max_length=100)


class PuertoResponse(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    ciudad: Optional[str]
    pais: str

    model_config = {"from_attributes": True}


# ── ENVÍOS TERRESTRES ────────────────────────────────────────
class EnvioTerrestreCreate(BaseModel):
    cliente_id: int
    producto_id: int
    cantidad_producto: int = Field(..., gt=0)
    fecha_entrega: date
    placa: str = Field(..., pattern=r'^[A-Za-z]{3}[0-9]{3}$')
    numero_guia: str = Field(..., min_length=10, max_length=10)
    bodega_id: int

    @field_validator("placa", "numero_guia")
    @classmethod
    def uppercase(cls, v: str) -> str:
        return v.upper()


class EnvioTerrestreResponse(BaseModel):
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

    model_config = {"from_attributes": True}


# ── ENVÍOS MARÍTIMOS ─────────────────────────────────────────
class EnvioMaritimoCreate(BaseModel):
    cliente_id: int
    producto_id: int
    cantidad_producto: int = Field(..., gt=0)
    fecha_entrega: date
    numero_flota: str = Field(..., pattern=r'^[A-Za-z]{3}[0-9]{4}[A-Za-z]$')
    numero_guia: str = Field(..., min_length=10, max_length=10)
    puerto_id: int

    @field_validator("numero_flota", "numero_guia")
    @classmethod
    def uppercase(cls, v: str) -> str:
        return v.upper()


class EnvioMaritimoResponse(BaseModel):
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

    model_config = {"from_attributes": True}


# ── ESTADO ───────────────────────────────────────────────────
class EstadoUpdate(BaseModel):
    estado: Literal["registrado", "en_transito", "entregado", "cancelado"]
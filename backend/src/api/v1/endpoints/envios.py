"""
Endpoints para envíos terrestres y marítimos.

Flujo clave:
  El email del usuario autenticado (extraído del JWT via get_current_user)
  se pasa al use case como email_usuario.
  El repositorio hace get_or_create_cliente con ese email —
  si el cliente no existe lo crea, si ya existe lo reutiliza.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies.db import get_db
from src.api.security.jwt_handler import get_current_user, get_current_cliente_id
from src.api.v1.schemas.schemas import (
    EnvioMaritimoCreate, EnvioMaritimoResponse,
    EnvioTerrestreCreate, EnvioTerrestreResponse,
    EstadoUpdate,
)
from src.application.dto import (
    CambiarEstadoDTO, CrearEnvioMaritimoDTO, CrearEnvioTerrestreDTO,
)
from src.application.use_cases.envio_use_cases import (
    uc_cambiar_estado_maritimo, uc_cambiar_estado_terrestre,
    uc_crear_envio_maritimo, uc_crear_envio_terrestre,
    uc_listar_envios_maritimos, uc_listar_envios_terrestres,
    uc_obtener_envio_maritimo, uc_obtener_envio_terrestre,
)
from src.infrastructure.database.models import Usuario
from src.shared.exceptions import DomainException, NotFoundError

_auth = Depends(get_current_user)


def _map_terrestre(dto) -> EnvioTerrestreResponse:
    return EnvioTerrestreResponse(
        id=dto.id,
        cliente_id=dto.cliente_id,
        producto_id=dto.producto_id,
        cantidad_producto=dto.cantidad_producto,
        fecha_registro=dto.fecha_registro,
        fecha_entrega=dto.fecha_entrega,
        precio_unitario=dto.precio_unitario,
        subtotal=dto.subtotal,
        descuento=dto.descuento,
        total=dto.total,
        estado=dto.estado,
        placa=dto.placa,
        numero_guia=dto.numero_guia,
        bodega_id=dto.bodega_id,
    )


def _map_maritimo(dto) -> EnvioMaritimoResponse:
    return EnvioMaritimoResponse(
        id=dto.id,
        cliente_id=dto.cliente_id,
        producto_id=dto.producto_id,
        cantidad_producto=dto.cantidad_producto,
        fecha_registro=dto.fecha_registro,
        fecha_entrega=dto.fecha_entrega,
        precio_unitario=dto.precio_unitario,
        subtotal=dto.subtotal,
        descuento=dto.descuento,
        total=dto.total,
        estado=dto.estado,
        numero_flota=dto.numero_flota,
        numero_guia=dto.numero_guia,
        puerto_id=dto.puerto_id,
    )


# ── TERRESTRES ───────────────────────────────────────────────
router_terrestres = APIRouter(prefix="/envios-terrestres", tags=["Envíos Terrestres"])


@router_terrestres.post("/", response_model=EnvioTerrestreResponse, status_code=201)
def crear_terrestre(
    body: EnvioTerrestreCreate,
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id),
):
    """
    Crea un envío terrestre.
    - Si el cliente no existe (primer envío), lo crea automáticamente.
    - Aplica 5% de descuento si cantidad > 10.
    """
    try:
        dto = uc_crear_envio_terrestre(db, CrearEnvioTerrestreDTO(
            cliente_id=cliente_id,
            producto_id=body.producto_id,
            cantidad_producto=body.cantidad_producto,
            fecha_entrega=body.fecha_entrega,
            placa=body.placa,
            numero_guia=body.numero_guia,
            bodega_id=body.bodega_id,
        ))
        return _map_terrestre(dto)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router_terrestres.get("/", response_model=list[EnvioTerrestreResponse])
def listar_terrestres(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id)
):
    return [_map_terrestre(dto) for dto in uc_listar_envios_terrestres(db, cliente_id, skip, limit)]


@router_terrestres.get("/{envio_id}", response_model=EnvioTerrestreResponse, dependencies=[_auth])
def obtener_terrestre(envio_id: int, db: Session = Depends(get_db)):
    try:
        return _map_terrestre(uc_obtener_envio_terrestre(db, envio_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router_terrestres.patch("/{envio_id}/estado", response_model=EnvioTerrestreResponse, dependencies=[_auth])
def cambiar_estado_terrestre(envio_id: int, body: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        return _map_terrestre(
            uc_cambiar_estado_terrestre(db, CambiarEstadoDTO(envio_id=envio_id, nuevo_estado=body.estado))
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


# ── MARÍTIMOS ────────────────────────────────────────────────
router_maritimos = APIRouter(prefix="/envios-maritimos", tags=["Envíos Marítimos"])


@router_maritimos.post("/", response_model=EnvioMaritimoResponse, status_code=201)
def crear_maritimo(
    body: EnvioMaritimoCreate,
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id),
):
    """
    Crea un envío marítimo.
    - Si el cliente no existe (primer envío), lo crea automáticamente.
    - Aplica 3% de descuento si cantidad > 10.
    """
    try:
        dto = uc_crear_envio_maritimo(db, CrearEnvioMaritimoDTO(
            cliente_id=cliente_id,
            producto_id=body.producto_id,
            cantidad_producto=body.cantidad_producto,
            fecha_entrega=body.fecha_entrega,
            numero_flota=body.numero_flota,
            numero_guia=body.numero_guia,
            puerto_id=body.puerto_id,
        ))
        return _map_maritimo(dto)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router_maritimos.get("/", response_model=list[EnvioMaritimoResponse])
def listar_maritimos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id)
):
    return [_map_maritimo(dto) for dto in uc_listar_envios_maritimos(db, cliente_id, skip, limit)]


@router_maritimos.get("/{envio_id}", response_model=EnvioMaritimoResponse, dependencies=[_auth])
def obtener_maritimo(envio_id: int, db: Session = Depends(get_db)):
    try:
        return _map_maritimo(uc_obtener_envio_maritimo(db, envio_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router_maritimos.patch("/{envio_id}/estado", response_model=EnvioMaritimoResponse, dependencies=[_auth])
def cambiar_estado_maritimo(envio_id: int, body: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        return _map_maritimo(
            uc_cambiar_estado_maritimo(db, CambiarEstadoDTO(envio_id=envio_id, nuevo_estado=body.estado))
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)
"""
Endpoints CRUD para entidades base.

Flujo por endpoint:
  HTTP Request
    → schema (ClienteCreate)
    → DTO (CrearClienteDTO)
    → use_case
    → DTO (ClienteDTO)
    → schema (ClienteResponse)
  → HTTP Response
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies.db import get_db
from src.api.security.jwt_handler import get_current_user
from src.api.v1.schemas.schemas import (
    BodegaCreate, BodegaResponse,
    ClienteCreate, ClienteResponse, ClienteUpdate,
    ProductoCreate, ProductoResponse,
    PuertoCreate, PuertoResponse,
)
from src.application.dto import (
    ActualizarClienteDTO, BodegaDTO, ClienteDTO,
    CrearBodegaDTO, CrearClienteDTO, CrearProductoDTO,
    CrearPuertoDTO, ProductoDTO, PuertoDTO,
)
from src.application.use_cases.base_use_cases import (
    uc_actualizar_cliente,
    uc_crear_bodega, uc_crear_cliente, uc_crear_producto, uc_crear_puerto,
    uc_eliminar_bodega, uc_eliminar_cliente, uc_eliminar_producto, uc_eliminar_puerto,
    uc_listar_bodegas, uc_listar_clientes, uc_listar_productos, uc_listar_puertos,
    uc_obtener_bodega, uc_obtener_cliente, uc_obtener_producto, uc_obtener_puerto,
)
from src.shared.exceptions import DomainException

_auth = Depends(get_current_user)


# ── Mappers DTO → Schema ──────────────────────────────────────
def _cliente_schema(dto: ClienteDTO) -> ClienteResponse:
    return ClienteResponse(
        id=dto.id,
        nombre_completo=dto.nombre_completo,
        email=dto.email,
        telefono=dto.telefono,
        direccion=dto.direccion,
    )


def _producto_schema(dto: ProductoDTO) -> ProductoResponse:
    return ProductoResponse(
        id=dto.id,
        tipo_producto=dto.tipo_producto,
        precio_unitario=dto.precio_unitario,
        tipo_logistica=dto.tipo_logistica,
        descripcion=dto.descripcion,
    )


def _bodega_schema(dto: BodegaDTO) -> BodegaResponse:
    return BodegaResponse(
        id=dto.id,
        nombre=dto.nombre,
        ubicacion=dto.ubicacion,
        ciudad=dto.ciudad,
        pais=dto.pais,
    )


def _puerto_schema(dto: PuertoDTO) -> PuertoResponse:
    return PuertoResponse(
        id=dto.id,
        nombre=dto.nombre,
        ubicacion=dto.ubicacion,
        ciudad=dto.ciudad,
        pais=dto.pais,
    )


# ── CLIENTES ─────────────────────────────────────────────────
router_clientes = APIRouter(prefix="/clientes", tags=["Clientes"])


@router_clientes.post("/", response_model=ClienteResponse, status_code=201, dependencies=[_auth])
def crear(body: ClienteCreate, db: Session = Depends(get_db)):
    try:
        dto = uc_crear_cliente(db, CrearClienteDTO(**body.model_dump()))
        return _cliente_schema(dto)
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router_clientes.get("/", response_model=list[ClienteResponse], dependencies=[_auth])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [_cliente_schema(dto) for dto in uc_listar_clientes(db, skip, limit)]


@router_clientes.get("/{cliente_id}", response_model=ClienteResponse, dependencies=[_auth])
def obtener(cliente_id: int, db: Session = Depends(get_db)):
    try:
        return _cliente_schema(uc_obtener_cliente(db, cliente_id))
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router_clientes.patch("/{cliente_id}", response_model=ClienteResponse, dependencies=[_auth])
def actualizar(cliente_id: int, body: ClienteUpdate, db: Session = Depends(get_db)):
    try:
        dto = uc_actualizar_cliente(db, cliente_id, ActualizarClienteDTO(**body.model_dump()))
        return _cliente_schema(dto)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router_clientes.delete("/{cliente_id}", status_code=204, dependencies=[_auth])
def eliminar(cliente_id: int, db: Session = Depends(get_db)):
    try:
        uc_eliminar_cliente(db, cliente_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


# ── PRODUCTOS ────────────────────────────────────────────────
router_productos = APIRouter(prefix="/productos", tags=["Productos"])


@router_productos.post("/", response_model=ProductoResponse, status_code=201, dependencies=[_auth])
def crear_prod(body: ProductoCreate, db: Session = Depends(get_db)):
    dto = uc_crear_producto(db, CrearProductoDTO(**body.model_dump()))
    return _producto_schema(dto)


@router_productos.get("/", response_model=list[ProductoResponse], dependencies=[_auth])
def listar_prod(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [_producto_schema(dto) for dto in uc_listar_productos(db, skip, limit)]


@router_productos.get("/{producto_id}", response_model=ProductoResponse, dependencies=[_auth])
def obtener_prod(producto_id: int, db: Session = Depends(get_db)):
    try:
        return _producto_schema(uc_obtener_producto(db, producto_id))
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router_productos.delete("/{producto_id}", status_code=204, dependencies=[_auth])
def eliminar_prod(producto_id: int, db: Session = Depends(get_db)):
    try:
        uc_eliminar_producto(db, producto_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


# ── BODEGAS ──────────────────────────────────────────────────
router_bodegas = APIRouter(prefix="/bodegas", tags=["Bodegas"])


@router_bodegas.post("/", response_model=BodegaResponse, status_code=201, dependencies=[_auth])
def crear_bod(body: BodegaCreate, db: Session = Depends(get_db)):
    return _bodega_schema(uc_crear_bodega(db, CrearBodegaDTO(**body.model_dump())))


@router_bodegas.get("/", response_model=list[BodegaResponse], dependencies=[_auth])
def listar_bod(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [_bodega_schema(dto) for dto in uc_listar_bodegas(db, skip, limit)]


@router_bodegas.get("/{bodega_id}", response_model=BodegaResponse, dependencies=[_auth])
def obtener_bod(bodega_id: int, db: Session = Depends(get_db)):
    try:
        return _bodega_schema(uc_obtener_bodega(db, bodega_id))
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router_bodegas.delete("/{bodega_id}", status_code=204, dependencies=[_auth])
def eliminar_bod(bodega_id: int, db: Session = Depends(get_db)):
    try:
        uc_eliminar_bodega(db, bodega_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


# ── PUERTOS ──────────────────────────────────────────────────
router_puertos = APIRouter(prefix="/puertos", tags=["Puertos"])


@router_puertos.post("/", response_model=PuertoResponse, status_code=201, dependencies=[_auth])
def crear_pue(body: PuertoCreate, db: Session = Depends(get_db)):
    return _puerto_schema(uc_crear_puerto(db, CrearPuertoDTO(**body.model_dump())))


@router_puertos.get("/", response_model=list[PuertoResponse], dependencies=[_auth])
def listar_pue(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return [_puerto_schema(dto) for dto in uc_listar_puertos(db, skip, limit)]


@router_puertos.get("/{puerto_id}", response_model=PuertoResponse, dependencies=[_auth])
def obtener_pue(puerto_id: int, db: Session = Depends(get_db)):
    try:
        return _puerto_schema(uc_obtener_puerto(db, puerto_id))
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router_puertos.delete("/{puerto_id}", status_code=204, dependencies=[_auth])
def eliminar_pue(puerto_id: int, db: Session = Depends(get_db)):
    try:
        uc_eliminar_puerto(db, puerto_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)
"""
Use Cases: Entidades base (Cliente, Producto, Bodega, Puerto)

Cada función representa un caso de uso concreto.
Recibe un DTO de entrada, llama al repositorio y retorna un DTO de salida.
Los endpoints no conocen los repositorios directamente.
"""
from sqlalchemy.orm import Session

from src.application.dto import (
    ActualizarClienteDTO,
    BodegaDTO,
    ClienteDTO,
    CrearBodegaDTO,
    CrearClienteDTO,
    CrearProductoDTO,
    CrearPuertoDTO,
    ProductoDTO,
    PuertoDTO,
)
from src.infrastructure.database.models import Bodega, Cliente, Producto, Puerto
from src.infrastructure.database.repositories.base_repo import (
    actualizar_cliente,
    crear_bodega,
    crear_cliente,
    crear_producto,
    crear_puerto,
    eliminar_bodega,
    eliminar_cliente,
    eliminar_producto,
    eliminar_puerto,
    listar_bodegas,
    listar_clientes,
    listar_productos,
    listar_puertos,
    obtener_bodega,
    obtener_cliente,
    obtener_producto,
    obtener_puerto,
)


# ── Helpers de mapeo ─────────────────────────────────────────
def _to_cliente_dto(c: Cliente) -> ClienteDTO:
    return ClienteDTO(
        id=c.id,
        nombre_completo=c.nombre_completo,
        email=c.email,
        telefono=c.telefono,
        direccion=c.direccion,
    )


def _to_producto_dto(p: Producto) -> ProductoDTO:
    return ProductoDTO(
        id=p.id,
        tipo_producto=p.tipo_producto,
        precio_unitario=p.precio_unitario,
        tipo_logistica=p.tipo_logistica,
        descripcion=p.descripcion,
    )


def _to_bodega_dto(b: Bodega) -> BodegaDTO:
    return BodegaDTO(
        id=b.id,
        nombre=b.nombre,
        ubicacion=b.ubicacion,
        ciudad=b.ciudad,
        pais=b.pais,
    )


def _to_puerto_dto(p: Puerto) -> PuertoDTO:
    return PuertoDTO(
        id=p.id,
        nombre=p.nombre,
        ubicacion=p.ubicacion,
        ciudad=p.ciudad,
        pais=p.pais,
    )


# ── CLIENTES ─────────────────────────────────────────────────
def uc_crear_cliente(db: Session, dto: CrearClienteDTO) -> ClienteDTO:
    cliente = crear_cliente(db, **dto.__dict__)
    return _to_cliente_dto(cliente)


def uc_listar_clientes(db: Session, skip: int, limit: int) -> list[ClienteDTO]:
    return [_to_cliente_dto(c) for c in listar_clientes(db, skip, limit)]


def uc_obtener_cliente(db: Session, cliente_id: int) -> ClienteDTO:
    return _to_cliente_dto(obtener_cliente(db, cliente_id))


def uc_actualizar_cliente(db: Session, cliente_id: int, dto: ActualizarClienteDTO) -> ClienteDTO:
    datos = {k: v for k, v in dto.__dict__.items() if v is not None}
    return _to_cliente_dto(actualizar_cliente(db, cliente_id, datos))


def uc_eliminar_cliente(db: Session, cliente_id: int) -> None:
    eliminar_cliente(db, cliente_id)


# ── PRODUCTOS ────────────────────────────────────────────────
def uc_crear_producto(db: Session, dto: CrearProductoDTO) -> ProductoDTO:
    return _to_producto_dto(crear_producto(db, **dto.__dict__))


def uc_listar_productos(db: Session, skip: int, limit: int) -> list[ProductoDTO]:
    return [_to_producto_dto(p) for p in listar_productos(db, skip, limit)]


def uc_obtener_producto(db: Session, producto_id: int) -> ProductoDTO:
    return _to_producto_dto(obtener_producto(db, producto_id))


def uc_eliminar_producto(db: Session, producto_id: int) -> None:
    eliminar_producto(db, producto_id)


# ── BODEGAS ──────────────────────────────────────────────────
def uc_crear_bodega(db: Session, dto: CrearBodegaDTO) -> BodegaDTO:
    return _to_bodega_dto(crear_bodega(db, **dto.__dict__))


def uc_listar_bodegas(db: Session, skip: int, limit: int) -> list[BodegaDTO]:
    return [_to_bodega_dto(b) for b in listar_bodegas(db, skip, limit)]


def uc_obtener_bodega(db: Session, bodega_id: int) -> BodegaDTO:
    return _to_bodega_dto(obtener_bodega(db, bodega_id))


def uc_eliminar_bodega(db: Session, bodega_id: int) -> None:
    eliminar_bodega(db, bodega_id)


# ── PUERTOS ──────────────────────────────────────────────────
def uc_crear_puerto(db: Session, dto: CrearPuertoDTO) -> PuertoDTO:
    return _to_puerto_dto(crear_puerto(db, **dto.__dict__))


def uc_listar_puertos(db: Session, skip: int, limit: int) -> list[PuertoDTO]:
    return [_to_puerto_dto(p) for p in listar_puertos(db, skip, limit)]


def uc_obtener_puerto(db: Session, puerto_id: int) -> PuertoDTO:
    return _to_puerto_dto(obtener_puerto(db, puerto_id))


def uc_eliminar_puerto(db: Session, puerto_id: int) -> None:
    eliminar_puerto(db, puerto_id)

"""
Use Cases: Envíos Terrestres y Marítimos

Orquesta la creación, consulta y cambio de estado de envíos.
Es el único punto que conoce tanto las reglas del dominio
como los repositorios de infraestructura.
"""
from sqlalchemy.orm import Session

from src.application.dto import (
    CambiarEstadoDTO,
    CrearEnvioMaritimoDTO,
    CrearEnvioTerrestreDTO,
    EnvioMaritimoDTO,
    EnvioTerrestreDTO,
)
from src.infrastructure.database.models import Envio, EnvioMaritimo, EnvioTerrestre
from src.infrastructure.database.repositories.envio_repo import (
    actualizar_estado_envio,
    crear_envio_maritimo,
    crear_envio_terrestre,
    listar_envios_maritimos,
    listar_envios_terrestres,
    obtener_envio_maritimo,
    obtener_envio_terrestre,
)


# ── Helpers de mapeo ─────────────────────────────────────────
def _to_terrestre_dto(envio: Envio, det: EnvioTerrestre) -> EnvioTerrestreDTO:
    return EnvioTerrestreDTO(
        id=envio.id,
        cliente_id=envio.cliente_id,
        producto_id=envio.producto_id,
        cantidad_producto=envio.cantidad_producto,
        fecha_registro=envio.fecha_registro,
        fecha_entrega=envio.fecha_entrega,
        precio_unitario=envio.precio_unitario,
        subtotal=envio.subtotal,
        descuento=envio.descuento,
        total=envio.total,
        estado=envio.estado,
        placa=det.placa,
        numero_guia=det.numero_guia,
        bodega_id=det.bodega_id,
    )


def _to_maritimo_dto(envio: Envio, det: EnvioMaritimo) -> EnvioMaritimoDTO:
    return EnvioMaritimoDTO(
        id=envio.id,
        cliente_id=envio.cliente_id,
        producto_id=envio.producto_id,
        cantidad_producto=envio.cantidad_producto,
        fecha_registro=envio.fecha_registro,
        fecha_entrega=envio.fecha_entrega,
        precio_unitario=envio.precio_unitario,
        subtotal=envio.subtotal,
        descuento=envio.descuento,
        total=envio.total,
        estado=envio.estado,
        numero_flota=det.numero_flota,
        numero_guia=det.numero_guia,
        puerto_id=det.puerto_id,
    )


# ── ENVÍOS TERRESTRES ────────────────────────────────────────
def uc_crear_envio_terrestre(db: Session, dto: CrearEnvioTerrestreDTO) -> EnvioTerrestreDTO:
    """
    Crea un envío terrestre.
    El repositorio valida value objects y aplica el descuento del 5%.
    """
    envio, det = crear_envio_terrestre(
        db,
        cliente_id=dto.cliente_id,
        producto_id=dto.producto_id,
        cantidad=dto.cantidad_producto,
        fecha_entrega=dto.fecha_entrega,
        placa=dto.placa,
        numero_guia=dto.numero_guia,
        bodega_id=dto.bodega_id,
    )
    return _to_terrestre_dto(envio, det)


def uc_listar_envios_terrestres(
    db: Session, cliente_id: int, skip: int, limit: int
) -> list[EnvioTerrestreDTO]:
    rows = listar_envios_terrestres(db, cliente_id, skip, limit)
    return [_to_terrestre_dto(e, d) for e, d in rows]


def uc_obtener_envio_terrestre(db: Session, envio_id: int) -> EnvioTerrestreDTO:
    envio, det = obtener_envio_terrestre(db, envio_id)
    return _to_terrestre_dto(envio, det)


def uc_cambiar_estado_terrestre(db: Session, dto: CambiarEstadoDTO) -> EnvioTerrestreDTO:
    actualizar_estado_envio(db, dto.envio_id, dto.nuevo_estado)
    envio, det = obtener_envio_terrestre(db, dto.envio_id)
    return _to_terrestre_dto(envio, det)


# ── ENVÍOS MARÍTIMOS ─────────────────────────────────────────
def uc_crear_envio_maritimo(db: Session, dto: CrearEnvioMaritimoDTO) -> EnvioMaritimoDTO:
    """
    Crea un envío marítimo.
    El repositorio valida value objects y aplica el descuento del 3%.
    """
    envio, det = crear_envio_maritimo(
        db,
        cliente_id=dto.cliente_id,
        producto_id=dto.producto_id,
        cantidad=dto.cantidad_producto,
        fecha_entrega=dto.fecha_entrega,
        numero_flota=dto.numero_flota,
        numero_guia=dto.numero_guia,
        puerto_id=dto.puerto_id,
    )
    return _to_maritimo_dto(envio, det)


def uc_listar_envios_maritimos(
    db: Session, cliente_id: int, skip: int, limit: int
) -> list[EnvioMaritimoDTO]:
    rows = listar_envios_maritimos(db, cliente_id, skip, limit)
    return [_to_maritimo_dto(e, d) for e, d in rows]


def uc_obtener_envio_maritimo(db: Session, envio_id: int) -> EnvioMaritimoDTO:
    envio, det = obtener_envio_maritimo(db, envio_id)
    return _to_maritimo_dto(envio, det)


def uc_cambiar_estado_maritimo(db: Session, dto: CambiarEstadoDTO) -> EnvioMaritimoDTO:
    actualizar_estado_envio(db, dto.envio_id, dto.nuevo_estado)
    envio, det = obtener_envio_maritimo(db, dto.envio_id)
    return _to_maritimo_dto(envio, det)
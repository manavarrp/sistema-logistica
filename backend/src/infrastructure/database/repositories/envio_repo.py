"""
Repositorios para envíos terrestres y marítimos.

Cada función de creación orquesta la transacción completa:
1. Valida que el producto exista y sea del tipo correcto
2. Calcula precios y descuentos usando las reglas del dominio
3. Persiste el registro base (envios) y el específico en una sola transacción
"""
from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain.rules.descuentos import (
    calcular_descuento_maritimo,
    calcular_descuento_terrestre,
)
from src.domain.value_objects import NumeroFlota, NumeroGuia, Placa
from src.infrastructure.database.models import (
    Envio,
    EnvioMaritimo,
    EnvioTerrestre,
    Producto,
)
from src.shared.exceptions import DuplicateError, NotFoundError, ValidationError


# ── ENVÍOS TERRESTRES ────────────────────────────────────────
def crear_envio_terrestre(
    db: Session,
    cliente_id: int,
    producto_id: int,
    cantidad: int,
    fecha_entrega,
    placa: str,
    numero_guia: str,
    bodega_id: int,
) -> tuple[Envio, EnvioTerrestre]:
    """
    Crea un envío terrestre en una transacción atómica.
    Valida value objects, aplica descuento y persiste ambas tablas.
    """
    # Validar value objects — lanzan ValidationError si el formato es incorrecto
    Placa(placa)
    NumeroGuia(numero_guia)

    # Obtener y validar producto
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise NotFoundError(f"Producto {producto_id} no encontrado")
    if producto.tipo_logistica != "terrestre":
        raise ValidationError("El producto no pertenece a logística terrestre")

    # Calcular precios
    precio_unitario = Decimal(str(producto.precio_unitario))
    subtotal = precio_unitario * Decimal(str(cantidad))
    descuento = calcular_descuento_terrestre(cantidad, subtotal)
    total = subtotal - descuento

    # Persistir tabla base
    envio = Envio(
        cliente_id=cliente_id,
        producto_id=producto_id,
        cantidad_producto=cantidad,
        fecha_entrega=fecha_entrega,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
        descuento=descuento,
        total=total,
        estado="registrado",
    )
    db.add(envio)
    db.flush()  # Obtiene el id sin cerrar la transacción

    # Persistir tabla específica
    detalle = EnvioTerrestre(
        envio_id=envio.id,
        placa=placa.upper(),
        numero_guia=numero_guia.upper(),
        bodega_id=bodega_id,
    )
    db.add(detalle)

    try:
        db.commit()
        db.refresh(envio)
        db.refresh(detalle)
        return envio, detalle
    except IntegrityError as e:
        db.rollback()
        if "numero_guia" in str(e.orig):
            raise DuplicateError(f"El número de guía '{numero_guia}' ya existe")
        raise


def listar_envios_terrestres(
    db: Session, skip: int = 0, limit: int = 100
) -> list[tuple[Envio, EnvioTerrestre]]:
    """Retorna envíos terrestres con su detalle en una sola query (JOIN)."""
    rows = (
        db.query(Envio, EnvioTerrestre)
        .join(EnvioTerrestre, Envio.id == EnvioTerrestre.envio_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return rows


def obtener_envio_terrestre(db: Session, envio_id: int) -> tuple[Envio, EnvioTerrestre]:
    row = (
        db.query(Envio, EnvioTerrestre)
        .join(EnvioTerrestre, Envio.id == EnvioTerrestre.envio_id)
        .filter(Envio.id == envio_id)
        .first()
    )
    if not row:
        raise NotFoundError(f"Envío terrestre {envio_id} no encontrado")
    return row


def actualizar_estado_envio(db: Session, envio_id: int, nuevo_estado: str) -> Envio:
    """Actualiza el estado de cualquier envío (terrestre o marítimo)."""
    ESTADOS_VALIDOS = {"registrado", "en_transito", "entregado", "cancelado"}
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise ValidationError(f"Estado inválido '{nuevo_estado}'. Válidos: {ESTADOS_VALIDOS}")

    envio = db.query(Envio).filter(Envio.id == envio_id).first()
    if not envio:
        raise NotFoundError(f"Envío {envio_id} no encontrado")

    envio.estado = nuevo_estado
    db.commit()
    db.refresh(envio)
    return envio


# ── ENVÍOS MARÍTIMOS ─────────────────────────────────────────
def crear_envio_maritimo(
    db: Session,
    cliente_id: int,
    producto_id: int,
    cantidad: int,
    fecha_entrega,
    numero_flota: str,
    numero_guia: str,
    puerto_id: int,
) -> tuple[Envio, EnvioMaritimo]:
    """
    Crea un envío marítimo en una transacción atómica.
    Valida value objects, aplica descuento y persiste ambas tablas.
    """
    # Validar value objects
    NumeroFlota(numero_flota)
    NumeroGuia(numero_guia)

    # Obtener y validar producto
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise NotFoundError(f"Producto {producto_id} no encontrado")
    if producto.tipo_logistica != "maritimo":
        raise ValidationError("El producto no pertenece a logística marítima")

    # Calcular precios
    precio_unitario = Decimal(str(producto.precio_unitario))
    subtotal = precio_unitario * Decimal(str(cantidad))
    descuento = calcular_descuento_maritimo(cantidad, subtotal)
    total = subtotal - descuento

    # Persistir tabla base
    envio = Envio(
        cliente_id=cliente_id,
        producto_id=producto_id,
        cantidad_producto=cantidad,
        fecha_entrega=fecha_entrega,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
        descuento=descuento,
        total=total,
        estado="registrado",
    )
    db.add(envio)
    db.flush()

    # Persistir tabla específica
    detalle = EnvioMaritimo(
        envio_id=envio.id,
        numero_flota=numero_flota.upper(),
        numero_guia=numero_guia.upper(),
        puerto_id=puerto_id,
    )
    db.add(detalle)

    try:
        db.commit()
        db.refresh(envio)
        db.refresh(detalle)
        return envio, detalle
    except IntegrityError as e:
        db.rollback()
        if "numero_guia" in str(e.orig):
            raise DuplicateError(f"El número de guía '{numero_guia}' ya existe")
        raise


def listar_envios_maritimos(
    db: Session, skip: int = 0, limit: int = 100
) -> list[tuple[Envio, EnvioMaritimo]]:
    """Retorna envíos marítimos con su detalle en una sola query (JOIN)."""
    rows = (
        db.query(Envio, EnvioMaritimo)
        .join(EnvioMaritimo, Envio.id == EnvioMaritimo.envio_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return rows


def obtener_envio_maritimo(db: Session, envio_id: int) -> tuple[Envio, EnvioMaritimo]:
    row = (
        db.query(Envio, EnvioMaritimo)
        .join(EnvioMaritimo, Envio.id == EnvioMaritimo.envio_id)
        .filter(Envio.id == envio_id)
        .first()
    )
    if not row:
        raise NotFoundError(f"Envío marítimo {envio_id} no encontrado")
    return row
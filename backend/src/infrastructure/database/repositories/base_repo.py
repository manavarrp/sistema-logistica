"""
Repositorios para entidades base.
Encapsulan todo acceso a base de datos, manteniendo
los endpoints y use_cases libres de lógica de persistencia.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.database.models import Bodega, Cliente, Producto, Puerto, Usuario
from src.shared.exceptions import DuplicateError, NotFoundError


# ── USUARIOS ────────────────────────────────────────────────
def crear_usuario(db: Session, email: str, password_hash: str) -> Usuario:
    usuario = Usuario(email=email, password_hash=password_hash)
    db.add(usuario)
    try:
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise DuplicateError(f"El email '{email}' ya está registrado")


def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


# ── CLIENTES ────────────────────────────────────────────────
def crear_cliente(
    db: Session,
    nombre_completo: str,
    email: str,
    telefono: str | None = None,
    direccion: str | None = None,
    usuario_id: int | None = None,
) -> Cliente:
    cliente = Cliente(
        nombre_completo=nombre_completo,
        email=email,
        telefono=telefono,
        direccion=direccion,
        usuario_id=usuario_id,
    )
    db.add(cliente)
    try:
        db.commit()
        db.refresh(cliente)
        return cliente
    except IntegrityError:
        db.rollback()
        raise DuplicateError(f"El email '{email}' ya está registrado")


def obtener_cliente_por_usuario_id(db: Session, usuario_id: int) -> Cliente | None:
    """Busca un cliente por usuario_id. Retorna None si no existe."""
    return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()


def get_or_create_cliente(db: Session, usuario_id: int, email: str) -> Cliente:
    """
    Obtiene el cliente por usuario_id o lo crea si no existe.

    Regla de negocio:
      - El usuario se registra solo en tabla usuarios (sin cliente aún).
      - La primera vez que crea un envío, este método crea el registro
        en clientes automáticamente y lo vincula por usuario_id.
      - Si ya existe, lo retorna directamente.

    El nombre_completo es provisional (derivado del email).
    El cliente puede actualizarlo después desde su perfil.

    Nota: usa flush() para no hacer commit — la transacción
    la cierra el repositorio de envíos al final.
    """
    cliente = obtener_cliente_por_usuario_id(db, usuario_id)
    if cliente:
        return cliente

    nombre_provisional = email.split("@")[0].replace(".", " ").title()
    cliente = Cliente(
        usuario_id=usuario_id,
        nombre_completo=nombre_provisional,
        email=email,
    )
    db.add(cliente)
    db.flush()
    return cliente


def listar_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()


def obtener_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise NotFoundError(f"Cliente {cliente_id} no encontrado")
    return cliente


def actualizar_cliente(db: Session, cliente_id: int, datos: dict) -> Cliente:
    cliente = obtener_cliente(db, cliente_id)
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


def eliminar_cliente(db: Session, cliente_id: int) -> None:
    cliente = obtener_cliente(db, cliente_id)
    db.delete(cliente)
    db.commit()


# ── PRODUCTOS ───────────────────────────────────────────────
def crear_producto(
    db: Session,
    tipo_producto: str,
    precio_unitario,
    tipo_logistica: str,
    descripcion: str | None = None,
) -> Producto:
    producto = Producto(
        tipo_producto=tipo_producto,
        precio_unitario=precio_unitario,
        tipo_logistica=tipo_logistica,
        descripcion=descripcion,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def listar_productos(db: Session, skip: int = 0, limit: int = 100) -> list[Producto]:
    return db.query(Producto).offset(skip).limit(limit).all()


def obtener_producto(db: Session, producto_id: int) -> Producto:
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise NotFoundError(f"Producto {producto_id} no encontrado")
    return producto


def actualizar_producto(db: Session, producto_id: int, datos: dict) -> Producto:
    producto = obtener_producto(db, producto_id)
    for campo, valor in datos.items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


def eliminar_producto(db: Session, producto_id: int) -> None:
    producto = obtener_producto(db, producto_id)
    db.delete(producto)
    db.commit()


# ── BODEGAS ─────────────────────────────────────────────────
def crear_bodega(
    db: Session,
    nombre: str,
    ubicacion: str,
    ciudad: str | None = None,
    pais: str = "Colombia",
) -> Bodega:
    bodega = Bodega(nombre=nombre, ubicacion=ubicacion, ciudad=ciudad, pais=pais)
    db.add(bodega)
    db.commit()
    db.refresh(bodega)
    return bodega


def listar_bodegas(db: Session, skip: int = 0, limit: int = 100) -> list[Bodega]:
    return db.query(Bodega).offset(skip).limit(limit).all()


def obtener_bodega(db: Session, bodega_id: int) -> Bodega:
    bodega = db.query(Bodega).filter(Bodega.id == bodega_id).first()
    if not bodega:
        raise NotFoundError(f"Bodega {bodega_id} no encontrada")
    return bodega


def eliminar_bodega(db: Session, bodega_id: int) -> None:
    bodega = obtener_bodega(db, bodega_id)
    db.delete(bodega)
    db.commit()


# ── PUERTOS ─────────────────────────────────────────────────
def crear_puerto(
    db: Session,
    nombre: str,
    ubicacion: str,
    ciudad: str | None = None,
    pais: str = "Colombia",
) -> Puerto:
    puerto = Puerto(nombre=nombre, ubicacion=ubicacion, ciudad=ciudad, pais=pais)
    db.add(puerto)
    db.commit()
    db.refresh(puerto)
    return puerto


def listar_puertos(db: Session, skip: int = 0, limit: int = 100) -> list[Puerto]:
    return db.query(Puerto).offset(skip).limit(limit).all()


def obtener_puerto(db: Session, puerto_id: int) -> Puerto:
    puerto = db.query(Puerto).filter(Puerto.id == puerto_id).first()
    if not puerto:
        raise NotFoundError(f"Puerto {puerto_id} no encontrado")
    return puerto


def eliminar_puerto(db: Session, puerto_id: int) -> None:
    puerto = obtener_puerto(db, puerto_id)
    db.delete(puerto)
    db.commit()
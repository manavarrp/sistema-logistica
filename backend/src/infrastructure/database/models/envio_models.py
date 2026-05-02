"""
Modelos SQLAlchemy - Envíos con herencia.

Patrón: Joined Table Inheritance
- Envio: tabla base con campos comunes
- EnvioTerrestre: extiende Envio con campos específicos terrestres
- EnvioMaritimo: extiende Envio con campos específicos marítimos

Cada envío específico tiene una relación 1:1 con la tabla base
a través de envio_id como PK y FK al mismo tiempo.
"""
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database.session import Base


class Envio(Base):
    """
    Tabla base para todos los envíos.
    Contiene únicamente los campos comunes a terrestre y marítimo.
    """
    __tablename__ = "envios"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="RESTRICT"), nullable=False, index=True)
    cantidad_producto = Column(Integer, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_entrega = Column(Date, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(50), default="registrado", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cliente = relationship("Cliente", backref="envios")
    producto = relationship("Producto", backref="envios")


class EnvioTerrestre(Base):
    """
    Extensión de Envio para logística terrestre.
    envio_id es PK y FK a envios al mismo tiempo (herencia 1:1).
    """
    __tablename__ = "envios_terrestres"

    envio_id = Column(Integer, ForeignKey("envios.id", ondelete="CASCADE"), primary_key=True)
    placa = Column(String(6), nullable=False, index=True)
    numero_guia = Column(String(10), unique=True, nullable=False, index=True)
    bodega_id = Column(Integer, ForeignKey("bodegas.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # uselist=False fuerza relación 1:1
    envio = relationship("Envio", backref="detalle_terrestre", uselist=False)
    bodega = relationship("Bodega", backref="envios_terrestres")


class EnvioMaritimo(Base):
    """
    Extensión de Envio para logística marítima.
    envio_id es PK y FK a envios al mismo tiempo (herencia 1:1).
    """
    __tablename__ = "envios_maritimos"

    envio_id = Column(Integer, ForeignKey("envios.id", ondelete="CASCADE"), primary_key=True)
    numero_flota = Column(String(8), nullable=False, index=True)
    numero_guia = Column(String(10), unique=True, nullable=False, index=True)
    puerto_id = Column(Integer, ForeignKey("puertos.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # uselist=False fuerza relación 1:1
    envio = relationship("Envio", backref="detalle_maritimo", uselist=False)
    puerto = relationship("Puerto", backref="envios_maritimos")
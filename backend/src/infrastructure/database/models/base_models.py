"""
Modelos SQLAlchemy - Entidades base.
Mapean directamente las tablas de PostgreSQL.
"""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.infrastructure.database.session import Base


class Usuario(Base):
    """Tabla de autenticación. Separada del cliente intencionalmente."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), unique=True)
    nombre_completo = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(50))
    direccion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Producto(Base):
    """
    tipo_logistica define si el producto viaja
    por vía terrestre o marítima.
    """
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_producto = Column(String(100), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    tipo_logistica = Column(String(20), nullable=False, index=True)  # terrestre | maritimo
    descripcion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Bodega(Base):
    """Bodega de almacenamiento terrestre."""
    __tablename__ = "bodegas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(Text, nullable=False)
    ciudad = Column(String(100))
    pais = Column(String(100), default="Colombia")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Puerto(Base):
    """Puerto marítimo nacional o internacional."""
    __tablename__ = "puertos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(Text, nullable=False)
    ciudad = Column(String(100))
    pais = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
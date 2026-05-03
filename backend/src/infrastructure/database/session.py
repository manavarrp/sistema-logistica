"""
Sesión de base de datos con SQLAlchemy.

Responsabilidades:
- Crear el engine de conexión a PostgreSQL
- Proveer la SessionLocal para transacciones
- Exponer la Base declarativa para los modelos
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.shared.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    connect_args={"options": "-c client_encoding=utf8"} # ✅ Fuerza UTF-8
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
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
    pool_pre_ping=True,   # Detecta conexiones caídas antes de usarlas
    echo=settings.DEBUG,  # Loguea SQL generado solo en desarrollo
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
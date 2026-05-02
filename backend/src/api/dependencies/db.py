"""
Dependency de base de datos para FastAPI.
 
Separa la responsabilidad de proveer la sesión
de los endpoints, facilitando el testing y el reuso.
"""
from typing import Generator
from sqlalchemy.orm import Session
from src.infrastructure.database.session import SessionLocal
 
 
def get_db() -> Generator[Session, None, None]:
    """
    Crea una sesión por request y la cierra automáticamente al terminar.
    Se usa como Depends(get_db) en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
conftest.py — Fixtures globales para tests.
"""
import os

# Setear variables de entorno ANTES de cualquier import del proyecto
# Esto permite que pydantic-settings las lea sin necesitar archivo .env
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-para-pruebas-unitarias")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

# ── Patch bcrypt para tests ───────────────────────────────────────────────────
# El entorno de CI usa Python 3.12 con bcrypt incompatible con passlib.
# Reemplazamos la implementación real por una versión simple que funciona
# en tests sin afectar el comportamiento de producción.
from unittest.mock import patch, MagicMock
import hashlib

def _fake_hash(password: str) -> str:
    return "hash:" + hashlib.sha256(password.encode()).hexdigest()

def _fake_verify(plain: str, hashed: str) -> bool:
    return hashed == _fake_hash(plain)

# Parchear antes de que cualquier módulo importe jwt_handler
patch("src.api.security.jwt_handler.pwd_context.hash", side_effect=_fake_hash).start()
patch("src.api.security.jwt_handler.pwd_context.verify", side_effect=_fake_verify).start()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.database.session import Base
from src.api.dependencies.db import get_db
from src.main import app

# ── Base de datos en memoria para tests ──────────────────────
# StaticPool garantiza que todos los hilos usen la misma conexión
# (necesario para SQLite en memoria con FastAPI TestClient)
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


@pytest.fixture(scope="function", autouse=False)
def db():
    """
    Sesión de BD limpia por cada test.
    Crea todas las tablas al inicio y las elimina al final.
    """
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db):
    """
    TestClient de FastAPI con la BD de test inyectada.
    Sobreescribe la dependency get_db para usar SQLite en memoria.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_registrado(client):
    """
    Registra un usuario de prueba y retorna sus datos.
    Usado como base para otros fixtures que necesitan autenticación.
    """
    payload = {
        "email": "test@logistica.com",
        "password": "Test123!",
        "nombre_completo": "Usuario Test",
        "telefono": "3001234567",
        "direccion": "Calle Test #1-23",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201, response.json()
    return payload


@pytest.fixture
def usuario_token(client, usuario_registrado):
    """
    Retorna el token JWT + cliente_id de un usuario autenticado.
    Fixture principal para tests de endpoints protegidos.
    """
    response = client.post("/api/v1/auth/login", json={
        "email": usuario_registrado["email"],
        "password": usuario_registrado["password"],
    })
    assert response.status_code == 200, response.json()
    data = response.json()
    return {
        "token": data["access_token"],
        "cliente_id": data["cliente_id"],
        "headers": {"Authorization": f"Bearer {data['access_token']}"},
    }


@pytest.fixture
def datos_semilla(client, usuario_token):
    """
    Crea datos base necesarios para tests de envíos:
    - 1 producto terrestre
    - 1 producto marítimo
    - 1 bodega
    - 1 puerto
    """
    headers = usuario_token["headers"]

    # Producto terrestre
    prod_terre = client.post("/api/v1/productos/", headers=headers, json={
        "tipo_producto": "Electrodomésticos",
        "precio_unitario": 50000.00,
        "tipo_logistica": "terrestre",
        "descripcion": "Producto de prueba terrestre",
    }).json()

    # Producto marítimo
    prod_mari = client.post("/api/v1/productos/", headers=headers, json={
        "tipo_producto": "Contenedor",
        "precio_unitario": 850000.00,
        "tipo_logistica": "maritimo",
        "descripcion": "Producto de prueba marítimo",
    }).json()

    # Bodega
    bodega = client.post("/api/v1/bodegas/", headers=headers, json={
        "nombre": "Bodega Central",
        "ubicacion": "Zona Industrial",
        "ciudad": "Medellín",
        "pais": "Colombia",
    }).json()

    # Puerto
    puerto = client.post("/api/v1/puertos/", headers=headers, json={
        "nombre": "Puerto de Buenaventura",
        "ubicacion": "Costa Pacífica",
        "ciudad": "Buenaventura",
        "pais": "Colombia",
    }).json()

    return {
        "producto_terrestre": prod_terre,
        "producto_maritimo": prod_mari,
        "bodega": bodega,
        "puerto": puerto,
    }
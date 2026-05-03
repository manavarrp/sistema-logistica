"""
Tests de integración — Endpoints de autenticación.

Prueba el flujo completo HTTP → use_case → BD (SQLite en memoria).
"""
import pytest


class TestRegister:

    def test_registro_exitoso(self, client):
        """Registro con datos válidos retorna 201 y el perfil del cliente."""
        response = client.post("/api/v1/auth/register", json={
            "email": "nuevo@test.com",
            "password": "Pass123!",
            "nombre_completo": "Juan Pérez",
            "telefono": "3001234567",
            "direccion": "Calle 50 #23",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["cliente"]["email"] == "nuevo@test.com"
        assert data["cliente"]["nombre_completo"] == "Juan Pérez"
        assert "id" in data["cliente"]
        assert "password" not in data["cliente"]    # nunca exponer la contraseña
        assert "token" in data

    def test_registro_sin_telefono_ni_direccion(self, client):
        """Los campos opcionales no deben impedir el registro."""
        response = client.post("/api/v1/auth/register", json={
            "email": "minimo@test.com",
            "password": "Pass123!",
            "nombre_completo": "Solo Nombre",
        })
        assert response.status_code == 201

    def test_registro_email_duplicado_retorna_400(self, client):
        """Registrar el mismo email dos veces debe retornar 400."""
        payload = {
            "email": "duplicado@test.com",
            "password": "Pass123!",
            "nombre_completo": "Primera Vez",
        }
        client.post("/api/v1/auth/register", json=payload)

        response = client.post("/api/v1/auth/register", json={**payload, "nombre_completo": "Segunda Vez"})
        assert response.status_code == 400
        assert "registrado" in response.json()["detail"].lower()

    def test_registro_email_invalido_retorna_422(self, client):
        """Email con formato inválido debe retornar 422 (validación Pydantic)."""
        response = client.post("/api/v1/auth/register", json={
            "email": "no-es-un-email",
            "password": "Pass123!",
            "nombre_completo": "Test",
        })
        assert response.status_code == 422

    def test_registro_password_muy_corto_retorna_422(self, client):
        """Password menor a 6 caracteres debe retornar 422."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@test.com",
            "password": "123",
            "nombre_completo": "Test",
        })
        assert response.status_code == 422

    def test_registro_sin_nombre_completo_retorna_422(self, client):
        """nombre_completo es requerido."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@test.com",
            "password": "Pass123!",
        })
        assert response.status_code == 422


class TestLogin:

    def test_login_exitoso_retorna_token_y_cliente_id(self, client, usuario_registrado):
        """Login correcto retorna access_token + cliente_id."""
        response = client.post("/api/v1/auth/login", json={
            "email": usuario_registrado["email"],
            "password": usuario_registrado["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["cliente_id"], int)
        assert data["cliente_id"] > 0

    def test_login_password_incorrecto_retorna_401(self, client, usuario_registrado):
        response = client.post("/api/v1/auth/login", json={
            "email": usuario_registrado["email"],
            "password": "contraseña_incorrecta",
        })
        assert response.status_code == 401

    def test_login_email_inexistente_retorna_401(self, client):
        response = client.post("/api/v1/auth/login", json={
            "email": "noexiste@test.com",
            "password": "Pass123!",
        })
        assert response.status_code == 401

    def test_token_permite_acceder_a_endpoint_protegido(self, client, usuario_token):
        """El token retornado debe funcionar para endpoints protegidos."""
        response = client.get(
            "/api/v1/clientes/",
            headers=usuario_token["headers"],
        )
        assert response.status_code == 200

    def test_sin_token_retorna_403(self, client):
        """Sin Authorization header, los endpoints protegidos retornan 403."""
        response = client.get("/api/v1/clientes/")
        assert response.status_code in (401, 403)

    def test_token_invalido_retorna_401(self, client):
        """Token malformado debe retornar 401."""
        response = client.get(
            "/api/v1/clientes/",
            headers={"Authorization": "Bearer token.invalido.aqui"},
        )
        assert response.status_code == 401
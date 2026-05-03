"""
Tests unitarios para los use cases de autenticación.

Usa mocks para aislar la lógica de negocio
de la base de datos real.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.application.use_cases.auth_use_cases import uc_registrar_usuario, uc_login
from src.application.dto import RegistrarUsuarioDTO, LoginDTO
from src.shared.exceptions import DuplicateError, BusinessRuleError
from sqlalchemy.exc import IntegrityError


class TestUcRegistrarUsuario:

    def test_registro_exitoso_crea_usuario_y_cliente(self):
        """
        El use case debe hacer flush + crear cliente + commit
        en esa secuencia exacta.
        """
        db = MagicMock()

        def simular_flush():
            db.add.call_args_list[0][0][0].id = 1
        db.flush.side_effect = simular_flush

        def simular_refresh(obj):
            obj.id = 1
        db.refresh.side_effect = simular_refresh

        dto = RegistrarUsuarioDTO(
            email="nuevo@test.com",
            password="Pass123!",
            nombre_completo="Usuario Nuevo",
        )

        # Mockear hash_password para aislar del bcrypt del entorno
        with patch("src.application.use_cases.auth_use_cases.hash_password", return_value="hashed"):
            resultado = uc_registrar_usuario(db, dto)

        assert db.add.call_count == 2    # usuario + cliente
        assert db.flush.call_count == 2
        assert db.commit.call_count == 1
        assert resultado.cliente.email == "nuevo@test.com"

    def test_registro_falla_si_email_duplicado(self):
        """Si el email ya existe, debe lanzar DuplicateError."""
        db = MagicMock()
        db.flush.side_effect = IntegrityError("", {}, Exception())

        dto = RegistrarUsuarioDTO(
            email="existente@test.com",
            password="Pass123!",
            nombre_completo="Ya Existe",
        )

        with patch("src.application.use_cases.auth_use_cases.hash_password", return_value="hashed"):
            with pytest.raises(DuplicateError) as exc_info:
                uc_registrar_usuario(db, dto)

        assert "existente@test.com" in exc_info.value.message
        db.rollback.assert_called_once()


class TestUcLogin:

    def test_login_exitoso_retorna_token_y_cliente_id(self):
        """Login correcto debe retornar token + cliente_id."""
        db = MagicMock()

        # Mock del usuario y cliente
        usuario_mock = MagicMock()
        usuario_mock.id = 1
        usuario_mock.email = "test@test.com"

        cliente_mock = MagicMock()
        cliente_mock.id = 5

        with patch(
            "src.application.use_cases.auth_use_cases.authenticate_user",
            return_value=usuario_mock,
        ), patch(
            "src.application.use_cases.auth_use_cases.create_access_token",
            return_value="fake.jwt.token",
        ):
            db.query.return_value.filter.return_value.first.return_value = cliente_mock

            resultado = uc_login(db, LoginDTO(email="test@test.com", password="Pass123!"))

        assert resultado.access_token == "fake.jwt.token"
        assert resultado.cliente_id == 5
        assert resultado.token_type == "bearer"

    def test_login_falla_con_credenciales_incorrectas(self):
        """Si las credenciales son inválidas, debe lanzar BusinessRuleError."""
        db = MagicMock()

        with patch(
            "src.application.use_cases.auth_use_cases.authenticate_user",
            return_value=None,
        ):
            with pytest.raises(BusinessRuleError) as exc_info:
                uc_login(db, LoginDTO(email="mal@test.com", password="incorrecta"))

        assert "Credenciales" in exc_info.value.message

    def test_login_falla_si_cliente_no_existe(self):
        """Si el usuario existe pero no tiene cliente, debe lanzar BusinessRuleError."""
        db = MagicMock()
        usuario_mock = MagicMock()
        usuario_mock.id = 99
        usuario_mock.email = "sincliente@test.com"

        with patch(
            "src.application.use_cases.auth_use_cases.authenticate_user",
            return_value=usuario_mock,
        ):
            db.query.return_value.filter.return_value.first.return_value = None

            with pytest.raises(BusinessRuleError) as exc_info:
                uc_login(db, LoginDTO(email="sincliente@test.com", password="Pass123!"))

        assert "perfil" in exc_info.value.message.lower()
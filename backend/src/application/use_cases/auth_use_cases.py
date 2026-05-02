"""
Use Cases: Autenticación

Orquesta el flujo de registro y login entre
la seguridad JWT y el repositorio de usuarios.
"""
from sqlalchemy.orm import Session

from src.api.security.jwt_handler import (
    authenticate_user,
    create_access_token,
    hash_password,
)
from src.application.dto import LoginDTO, RegistrarUsuarioDTO, TokenDTO, RegistroConTokenDTO, ClienteDTO
from src.infrastructure.database.repositories.base_repo import crear_usuario, crear_cliente, obtener_cliente_por_usuario_id
from src.shared.exceptions import BusinessRuleError


def uc_registrar_usuario(db: Session, dto: RegistrarUsuarioDTO) -> RegistroConTokenDTO:
    """Registra un nuevo usuario y su perfil de cliente de forma atómica."""
    # 1. Crear usuario
    usuario = crear_usuario(db, email=dto.email, password_hash=hash_password(dto.password))
    
    # 2. Crear cliente asociado
    cliente = crear_cliente(
        db,
        nombre_completo=dto.nombre_completo,
        email=dto.email,
        telefono=dto.telefono,
        direccion=dto.direccion,
        usuario_id=usuario.id
    )
    
    # 3. Generar token
    access_token = create_access_token(
        email=usuario.email,
        usuario_id=usuario.id,
        cliente_id=cliente.id
    )
    
    # 4. Construir DTO de respuesta combinada
    cliente_dto = ClienteDTO(
        id=cliente.id,
        nombre_completo=cliente.nombre_completo,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )
    token_dto = TokenDTO(access_token=access_token, cliente_id=cliente.id)
    
    return RegistroConTokenDTO(cliente=cliente_dto, token=token_dto)


def uc_login(db: Session, dto: LoginDTO) -> TokenDTO:
    """Autentica credenciales y retorna un token JWT inyectando el cliente_id."""
    user = authenticate_user(db, dto.email, dto.password)
    if not user:
        raise BusinessRuleError("Credenciales incorrectas")
        
    cliente = obtener_cliente_por_usuario_id(db, user.id)
    cliente_id = cliente.id if cliente else 0  # En caso de que falle o no exista
    
    token = create_access_token(
        email=user.email,
        usuario_id=user.id,
        cliente_id=cliente_id
    )
    return TokenDTO(access_token=token, cliente_id=cliente_id)

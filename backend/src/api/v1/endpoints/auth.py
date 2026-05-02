"""
Endpoints de autenticación.

Flujo de registro:
  HTTP Request (email, password, nombre_completo)
    → RegisterRequest schema
    → RegistrarUsuarioDTO
    → uc_registrar_usuario  ← crea usuario + cliente atómicamente
    → ClienteDTO
    → ClienteResponse
  → HTTP Response

Flujo de login:
  HTTP Request (email, password)
    → LoginRequest schema
    → LoginDTO
    → uc_login  ← retorna token + cliente_id
    → TokenConClienteDTO
    → TokenResponse (con cliente_id)
  → HTTP Response
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies.db import get_db
from src.api.v1.schemas.schemas import (
    LoginRequest, RegisterRequest, TokenResponse, ClienteResponse, RegisterResponse
)
from src.application.dto import LoginDTO, RegistrarUsuarioDTO
from src.application.use_cases.auth_use_cases import uc_login, uc_registrar_usuario
from src.shared.exceptions import DomainException

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario y crea su perfil de cliente en una sola transacción.
    Retorna el perfil del cliente creado y un token de autenticación (Auto-login).
    """
    try:
        resultado = uc_registrar_usuario(db, RegistrarUsuarioDTO(
            email=body.email,
            password=body.password,
            nombre_completo=body.nombre_completo,
            telefono=body.telefono,
            direccion=body.direccion,
        ))
        return RegisterResponse(
            cliente=ClienteResponse(
                id=resultado.cliente.id,
                nombre_completo=resultado.cliente.nombre_completo,
                email=resultado.cliente.email,
                telefono=resultado.cliente.telefono,
                direccion=resultado.cliente.direccion,
            ),
            token=TokenResponse(
                access_token=resultado.token.access_token,
                token_type=resultado.token.token_type,
                cliente_id=resultado.token.cliente_id,
            )
        )
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica credenciales y retorna JWT + cliente_id.
    El cliente_id se usa en el frontend para asociar envíos directamente.
    """
    try:
        result = uc_login(db, LoginDTO(email=body.email, password=body.password))
        return TokenResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            cliente_id=result.cliente_id,
        )
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
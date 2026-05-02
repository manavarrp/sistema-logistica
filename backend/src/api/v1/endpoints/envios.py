"""Endpoints para envíos terrestres y marítimos. Delegan a use cases."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.dependencies.db import get_db

from src.api.v1.schemas.schemas import (
    EnvioMaritimoCreate, EnvioMaritimoResponse,
    EnvioTerrestreCreate, EnvioTerrestreResponse,
    EstadoUpdate,
)
from src.application.dto import (
    CambiarEstadoDTO, CrearEnvioMaritimoDTO, CrearEnvioTerrestreDTO,
)
from src.application.use_cases.envio_use_cases import (
    uc_cambiar_estado_maritimo, uc_cambiar_estado_terrestre,
    uc_crear_envio_maritimo, uc_crear_envio_terrestre,
    uc_listar_envios_maritimos, uc_listar_envios_terrestres,
    uc_obtener_envio_maritimo, uc_obtener_envio_terrestre,
)
from src.shared.exceptions import DomainException


# ── TERRESTRES ───────────────────────────────────────────────
router_terrestres = APIRouter(prefix="/envios-terrestres", tags=["Envíos Terrestres"])

@router_terrestres.post("/", response_model=EnvioTerrestreResponse, status_code=201)
def crear_terrestre(body: EnvioTerrestreCreate, db: Session = Depends(get_db)):
    """Crea un envío terrestre. Aplica 5% de descuento si cantidad > 10."""
    try:
        return uc_crear_envio_terrestre(db, CrearEnvioTerrestreDTO(**body.model_dump()))
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router_terrestres.get("/", response_model=list[EnvioTerrestreResponse])
def listar_terrestres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return uc_listar_envios_terrestres(db, skip, limit)

@router_terrestres.get("/{envio_id}", response_model=EnvioTerrestreResponse)
def obtener_terrestre(envio_id: int, db: Session = Depends(get_db)):
    try:
        return uc_obtener_envio_terrestre(db, envio_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)

@router_terrestres.patch("/{envio_id}/estado", response_model=EnvioTerrestreResponse)
def cambiar_estado_terrestre(envio_id: int, body: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        return uc_cambiar_estado_terrestre(db, CambiarEstadoDTO(envio_id=envio_id, nuevo_estado=body.estado))
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)

# ── MARÍTIMOS ────────────────────────────────────────────────
router_maritimos = APIRouter(prefix="/envios-maritimos", tags=["Envíos Marítimos"])

@router_maritimos.post("/", response_model=EnvioMaritimoResponse, status_code=201)
def crear_maritimo(body: EnvioMaritimoCreate, db: Session = Depends(get_db)):
    """Crea un envío marítimo. Aplica 3% de descuento si cantidad > 10."""
    try:
        return uc_crear_envio_maritimo(db, CrearEnvioMaritimoDTO(**body.model_dump()))
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router_maritimos.get("/", response_model=list[EnvioMaritimoResponse])
def listar_maritimos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return uc_listar_envios_maritimos(db, skip, limit)

@router_maritimos.get("/{envio_id}", response_model=EnvioMaritimoResponse)
def obtener_maritimo(envio_id: int, db: Session = Depends(get_db)):
    try:
        return uc_obtener_envio_maritimo(db, envio_id)
    except DomainException as e:
        raise HTTPException(status_code=404, detail=e.message)

@router_maritimos.patch("/{envio_id}/estado", response_model=EnvioMaritimoResponse)
def cambiar_estado_maritimo(envio_id: int, body: EstadoUpdate, db: Session = Depends(get_db)):
    try:
        return uc_cambiar_estado_maritimo(db, CambiarEstadoDTO(envio_id=envio_id, nuevo_estado=body.estado))
    except DomainException as e:
        raise HTTPException(status_code=400, detail=e.message)
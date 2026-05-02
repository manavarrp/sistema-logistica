"""
Punto de entrada de la aplicación.
Registra todos los routers y middlewares.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from src.api.v1.endpoints.envios import router_maritimos, router_terrestres
from src.shared.config import settings
from src.shared.exceptions import DomainException

app = FastAPI(
    title="Sistema de Gestión Logística",
    description="API REST para gestión de envíos terrestres y marítimos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── MANEJADOR GLOBAL DE EXCEPCIONES DEL DOMINIO ──────────────
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(status_code=400, content={"detail": exc.message})


# ── ROUTERS ──────────────────────────────────────────────────
PREFIX = "/api/v1"


app.include_router(router_terrestres, prefix=PREFIX)
app.include_router(router_maritimos,  prefix=PREFIX)


# ── HEALTH ───────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "running", "docs": "/docs", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


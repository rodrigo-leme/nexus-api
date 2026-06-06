"""NEXUS API — Sistema Operacional para Ambientes Extremos.

Ponto de entrada da aplicação FastAPI.
Inspirado nos protocolos de resiliência da NASA/ISS.
"""

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routers import ambiente_router, operador_router, sensor_router, telemetria_router
from app.infrastructure.database.connection import create_tables

app = FastAPI(
    title="NEXUS API",
    description=(
        "Sistema Operacional para Ambientes Extremos — "
        "Plataforma SOA de telemetria, sensores IoT e alertas preditivos "
        "para bases offshore, antárticas, militares e espaciais."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.include_router(ambiente_router.router, prefix="/api/v1")
app.include_router(sensor_router.router, prefix="/api/v1")
app.include_router(telemetria_router.router, prefix="/api/v1")
app.include_router(operador_router.router, prefix="/api/v1")


@app.on_event("startup")
def startup_event() -> None:
    create_tables()


@app.get("/", tags=["Health"])
def root():
    return {
        "sistema": "NEXUS",
        "versao": "1.0.0",
        "descricao": "Sistema Operacional para Ambientes Extremos",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "nexus-api"}

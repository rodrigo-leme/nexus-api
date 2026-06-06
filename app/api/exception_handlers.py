"""Handlers globais de exceção — captura erros de domínio e retorna respostas HTTP padronizadas."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.domain_exceptions import (
    AlertaJaResolvidoError,
    DatabaseError,
    EntityNotFoundError,
    LimiteOperadoresError,
    NexusBaseException,
    SensorOfflineError,
    ValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Registra handlers de exceção específicos do domínio NEXUS."""

    @app.exception_handler(ValidationError)
    async def validation_error_handler(_request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(EntityNotFoundError)
    async def not_found_handler(_request: Request, exc: EntityNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(SensorOfflineError)
    async def sensor_offline_handler(_request: Request, exc: SensorOfflineError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(LimiteOperadoresError)
    async def limite_operadores_handler(_request: Request, exc: LimiteOperadoresError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(AlertaJaResolvidoError)
    async def alerta_resolvido_handler(_request: Request, exc: AlertaJaResolvidoError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(_request: Request, exc: DatabaseError) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": exc.code, "message": "Erro interno de banco de dados."},
        )

    @app.exception_handler(NexusBaseException)
    async def nexus_generic_handler(_request: Request, exc: NexusBaseException) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": exc.code, "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def generic_handler(_request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "INTERNAL_ERROR", "message": "Erro interno inesperado no servidor NEXUS."},
        )

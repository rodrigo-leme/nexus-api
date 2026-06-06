"""Router de Telemetria — ingestão de leituras e consulta de alertas."""

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.deps import get_telemetria_service
from app.dtos.request.leitura_dto import RegistrarLeituraRequest
from app.dtos.response.alerta_dto import AlertaResponse
from app.dtos.response.leitura_dto import LeituraResponse
from app.services.telemetria_service import TelemetriaService

router = APIRouter(prefix="/telemetria", tags=["Telemetria"])


@router.post("/leituras", response_model=LeituraResponse, status_code=status.HTTP_201_CREATED)
def registrar_leitura(
    dto: RegistrarLeituraRequest,
    service: TelemetriaService = Depends(get_telemetria_service),
):
    return service.registrar_leitura(dto)


@router.get("/leituras", response_model=list[LeituraResponse])
def listar_leituras(
    sensor_id: int | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    service: TelemetriaService = Depends(get_telemetria_service),
):
    return service.listar_leituras(sensor_id, limit)


@router.get("/alertas", response_model=list[AlertaResponse])
def listar_alertas(
    apenas_abertos: bool = Query(False),
    service: TelemetriaService = Depends(get_telemetria_service),
):
    return service.listar_alertas(apenas_abertos)


@router.patch("/alertas/{alerta_id}/resolver", response_model=AlertaResponse)
def resolver_alerta(
    alerta_id: int,
    service: TelemetriaService = Depends(get_telemetria_service),
):
    return service.resolver_alerta(alerta_id)

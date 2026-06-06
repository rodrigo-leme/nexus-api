"""Router de Ambientes — endpoints REST/WebService."""

from fastapi import APIRouter, Depends, status

from app.api.dependencies.deps import get_ambiente_service
from app.dtos.request.ambiente_dto import AtualizarAmbienteRequest, CriarAmbienteRequest
from app.dtos.response.ambiente_dto import AmbienteResumoResponse, AmbienteResponse
from app.services.ambiente_service import AmbienteService

router = APIRouter(prefix="/ambientes", tags=["Ambientes"])


@router.get("/", response_model=list[AmbienteResponse])
def listar_ambientes(service: AmbienteService = Depends(get_ambiente_service)):
    return service.listar_todos()


@router.get("/{ambiente_id}", response_model=AmbienteResponse)
def buscar_ambiente(ambiente_id: int, service: AmbienteService = Depends(get_ambiente_service)):
    return service.buscar_por_id(ambiente_id)


@router.get("/{ambiente_id}/resumo", response_model=AmbienteResumoResponse)
def resumo_ambiente(ambiente_id: int, service: AmbienteService = Depends(get_ambiente_service)):
    return service.obter_resumo(ambiente_id)


@router.post("/", response_model=AmbienteResponse, status_code=status.HTTP_201_CREATED)
def criar_ambiente(dto: CriarAmbienteRequest, service: AmbienteService = Depends(get_ambiente_service)):
    return service.criar(dto)


@router.put("/{ambiente_id}", response_model=AmbienteResponse)
def atualizar_ambiente(
    ambiente_id: int,
    dto: AtualizarAmbienteRequest,
    service: AmbienteService = Depends(get_ambiente_service),
):
    return service.atualizar(ambiente_id, dto)


@router.delete("/{ambiente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_ambiente(ambiente_id: int, service: AmbienteService = Depends(get_ambiente_service)):
    service.deletar(ambiente_id)


@router.get("/tipo/{tipo}", response_model=list[AmbienteResponse])
def listar_por_tipo(tipo: str, service: AmbienteService = Depends(get_ambiente_service)):
    return service.buscar_por_tipo(tipo)

"""Router de Operadores — endpoints REST/WebService."""

from fastapi import APIRouter, Depends, status

from app.api.dependencies.deps import get_operador_service
from app.dtos.request.operador_dto import AtualizarOperadorRequest, CriarOperadorRequest
from app.dtos.response.operador_dto import OperadorResponse
from app.services.operador_service import OperadorService

router = APIRouter(prefix="/operadores", tags=["Operadores"])


@router.get("/", response_model=list[OperadorResponse])
def listar_operadores(service: OperadorService = Depends(get_operador_service)):
    return service.listar_todos()


@router.get("/{operador_id}", response_model=OperadorResponse)
def buscar_operador(operador_id: int, service: OperadorService = Depends(get_operador_service)):
    return service.buscar_por_id(operador_id)


@router.post("/", response_model=OperadorResponse, status_code=status.HTTP_201_CREATED)
def criar_operador(dto: CriarOperadorRequest, service: OperadorService = Depends(get_operador_service)):
    return service.criar(dto)


@router.put("/{operador_id}", response_model=OperadorResponse)
def atualizar_operador(
    operador_id: int,
    dto: AtualizarOperadorRequest,
    service: OperadorService = Depends(get_operador_service),
):
    return service.atualizar(operador_id, dto)


@router.delete("/{operador_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_operador(operador_id: int, service: OperadorService = Depends(get_operador_service)):
    service.deletar(operador_id)


@router.get("/ambiente/{ambiente_id}", response_model=list[OperadorResponse])
def listar_por_ambiente(ambiente_id: int, service: OperadorService = Depends(get_operador_service)):
    return service.listar_por_ambiente(ambiente_id)

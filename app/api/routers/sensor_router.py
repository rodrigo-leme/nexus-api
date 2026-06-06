"""Router de Sensores — endpoints REST/WebService."""

from fastapi import APIRouter, Depends, status

from app.api.dependencies.deps import get_sensor_service
from app.dtos.request.sensor_dto import AtualizarSensorRequest, CriarSensorRequest
from app.dtos.response.sensor_dto import SensorResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensores", tags=["Sensores"])


@router.get("/", response_model=list[SensorResponse])
def listar_sensores(service: SensorService = Depends(get_sensor_service)):
    return service.listar_todos()


@router.get("/{sensor_id}", response_model=SensorResponse)
def buscar_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    return service.buscar_por_id(sensor_id)


@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def criar_sensor(dto: CriarSensorRequest, service: SensorService = Depends(get_sensor_service)):
    return service.criar(dto)


@router.put("/{sensor_id}", response_model=SensorResponse)
def atualizar_sensor(
    sensor_id: int,
    dto: AtualizarSensorRequest,
    service: SensorService = Depends(get_sensor_service),
):
    return service.atualizar(sensor_id, dto)


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    service.deletar(sensor_id)


@router.get("/ambiente/{ambiente_id}", response_model=list[SensorResponse])
def listar_por_ambiente(ambiente_id: int, service: SensorService = Depends(get_sensor_service)):
    return service.listar_por_ambiente(ambiente_id)

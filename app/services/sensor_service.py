"""Serviço de Sensores — lógica de negócio SOA."""

from app.domain.exceptions.domain_exceptions import EntityNotFoundError, ValidationError
from app.dtos.request.sensor_dto import AtualizarSensorRequest, CriarSensorRequest
from app.dtos.response.sensor_dto import SensorResponse
from app.infrastructure.database.models import SensorModel
from app.infrastructure.repositories.sensor_repository import SensorRepository
from app.infrastructure.repositories.ambiente_repository import AmbienteRepository
from app.services.base_service import BaseService


TIPOS_SENSOR_VALIDOS = {"temperatura", "pressao", "energia", "radiacao", "qualidade_ar"}
STATUS_SENSOR_VALIDOS = {"ativo", "inativo", "manutencao", "falha"}


class SensorService(BaseService):
    def __init__(self, repo: SensorRepository, ambiente_repo: AmbienteRepository) -> None:
        self._repo = repo
        self._ambiente_repo = ambiente_repo

    def listar_todos(self) -> list[SensorResponse]:
        return [SensorResponse.model_validate(m) for m in self._repo.get_all()]

    def buscar_por_id(self, sensor_id: int) -> SensorResponse:
        modelo = self._repo.get_by_id(sensor_id)
        if modelo is None:
            raise EntityNotFoundError("Sensor", sensor_id)
        return SensorResponse.model_validate(modelo)

    def criar(self, dto: CriarSensorRequest) -> SensorResponse:
        if dto.tipo not in TIPOS_SENSOR_VALIDOS:
            raise ValidationError(f"Tipo de sensor inválido: {dto.tipo}")
        if self._ambiente_repo.get_by_id(dto.ambiente_id) is None:
            raise EntityNotFoundError("Ambiente", dto.ambiente_id)
        if dto.valor_min >= dto.valor_max:
            raise ValidationError("valor_min deve ser menor que valor_max.")
        existente = self._repo.get_by_codigo(dto.codigo)
        if existente is not None:
            raise ValidationError(f"Sensor com código '{dto.codigo}' já existe.")
        modelo = SensorModel(
            codigo=dto.codigo,
            tipo=dto.tipo,
            ambiente_id=dto.ambiente_id,
            unidade_medida=dto.unidade_medida,
            valor_min=dto.valor_min,
            valor_max=dto.valor_max,
        )
        criado = self._repo.create(modelo)
        return SensorResponse.model_validate(criado)

    def atualizar(self, sensor_id: int, dto: AtualizarSensorRequest) -> SensorResponse:
        modelo = self._repo.get_by_id(sensor_id)
        if modelo is None:
            raise EntityNotFoundError("Sensor", sensor_id)
        if dto.status is not None:
            if dto.status not in STATUS_SENSOR_VALIDOS:
                raise ValidationError(f"Status inválido: {dto.status}")
            modelo.status = dto.status
        if dto.valor_min is not None:
            modelo.valor_min = dto.valor_min
        if dto.valor_max is not None:
            modelo.valor_max = dto.valor_max
        atualizado = self._repo.update(modelo)
        return SensorResponse.model_validate(atualizado)

    def deletar(self, sensor_id: int) -> bool:
        if not self._repo.delete(sensor_id):
            raise EntityNotFoundError("Sensor", sensor_id)
        return True

    def listar_por_ambiente(self, ambiente_id: int) -> list[SensorResponse]:
        return [SensorResponse.model_validate(m) for m in self._repo.get_by_ambiente(ambiente_id)]

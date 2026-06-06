"""Serviço de Ambientes — lógica de negócio SOA."""

from app.domain.exceptions.domain_exceptions import EntityNotFoundError, ValidationError
from app.dtos.request.ambiente_dto import AtualizarAmbienteRequest, CriarAmbienteRequest
from app.dtos.response.ambiente_dto import AmbienteResumoResponse, AmbienteResponse
from app.infrastructure.database.models import AmbienteModel
from app.infrastructure.repositories.ambiente_repository import AmbienteRepository
from app.infrastructure.repositories.alerta_repository import AlertaRepository
from app.services.base_service import BaseService


TIPOS_VALIDOS = {"offshore", "antartica", "militar", "espacial"}
STATUS_VALIDOS = {"operacional", "alerta", "critico", "offline"}


class AmbienteService(BaseService):
    def __init__(self, repo: AmbienteRepository, alerta_repo: AlertaRepository) -> None:
        self._repo = repo
        self._alerta_repo = alerta_repo

    def listar_todos(self) -> list[AmbienteResponse]:
        modelos = self._repo.get_all()
        return [AmbienteResponse.model_validate(m) for m in modelos]

    def buscar_por_id(self, ambiente_id: int) -> AmbienteResponse:
        modelo = self._repo.get_by_id(ambiente_id)
        if modelo is None:
            raise EntityNotFoundError("Ambiente", ambiente_id)
        return AmbienteResponse.model_validate(modelo)

    def criar(self, dto: CriarAmbienteRequest) -> AmbienteResponse:
        if dto.tipo not in TIPOS_VALIDOS:
            raise ValidationError(f"Tipo inválido: {dto.tipo}. Válidos: {TIPOS_VALIDOS}")
        modelo = AmbienteModel(
            nome=dto.nome,
            tipo=dto.tipo,
            localizacao=dto.localizacao,
            capacidade_operadores=dto.capacidade_operadores,
        )
        criado = self._repo.create(modelo)
        return AmbienteResponse.model_validate(criado)

    def atualizar(self, ambiente_id: int, dto: AtualizarAmbienteRequest) -> AmbienteResponse:
        modelo = self._repo.get_by_id(ambiente_id)
        if modelo is None:
            raise EntityNotFoundError("Ambiente", ambiente_id)
        if dto.nome is not None:
            modelo.nome = dto.nome
        if dto.localizacao is not None:
            modelo.localizacao = dto.localizacao
        if dto.capacidade_operadores is not None:
            modelo.capacidade_operadores = dto.capacidade_operadores
        if dto.status is not None:
            if dto.status not in STATUS_VALIDOS:
                raise ValidationError(f"Status inválido: {dto.status}. Válidos: {STATUS_VALIDOS}")
            modelo.status = dto.status
        atualizado = self._repo.update(modelo)
        return AmbienteResponse.model_validate(atualizado)

    def deletar(self, ambiente_id: int) -> bool:
        if not self._repo.delete(ambiente_id):
            raise EntityNotFoundError("Ambiente", ambiente_id)
        return True

    def buscar_por_tipo(self, tipo: str) -> list[AmbienteResponse]:
        modelos = self._repo.get_by_tipo(tipo)
        return [AmbienteResponse.model_validate(m) for m in modelos]

    def obter_resumo(self, ambiente_id: int) -> AmbienteResumoResponse:
        modelo = self._repo.get_by_id(ambiente_id)
        if modelo is None:
            raise EntityNotFoundError("Ambiente", ambiente_id)
        alertas_abertos = len([a for a in self._alerta_repo.get_by_ambiente(ambiente_id) if a.status == "aberto"])
        return AmbienteResumoResponse(
            id=modelo.id,
            nome=modelo.nome,
            tipo=modelo.tipo,
            status=modelo.status,
            total_sensores=len(modelo.sensores),
            total_operadores=len(modelo.operadores),
            alertas_abertos=alertas_abertos,
        )

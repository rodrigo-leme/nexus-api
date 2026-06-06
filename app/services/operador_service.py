"""Serviço de Operadores — lógica de negócio SOA."""

from app.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    LimiteOperadoresError,
    ValidationError,
)
from app.dtos.request.operador_dto import AtualizarOperadorRequest, CriarOperadorRequest
from app.dtos.response.operador_dto import OperadorResponse
from app.infrastructure.database.models import OperadorModel
from app.infrastructure.repositories.operador_repository import OperadorRepository
from app.infrastructure.repositories.ambiente_repository import AmbienteRepository
from app.services.base_service import BaseService


CARGOS_VALIDOS = {"engenheiro", "tecnico", "medico", "comandante", "pesquisador"}


class OperadorService(BaseService):
    def __init__(self, repo: OperadorRepository, ambiente_repo: AmbienteRepository) -> None:
        self._repo = repo
        self._ambiente_repo = ambiente_repo

    def listar_todos(self) -> list[OperadorResponse]:
        return [OperadorResponse.model_validate(m) for m in self._repo.get_all()]

    def buscar_por_id(self, operador_id: int) -> OperadorResponse:
        modelo = self._repo.get_by_id(operador_id)
        if modelo is None:
            raise EntityNotFoundError("Operador", operador_id)
        return OperadorResponse.model_validate(modelo)

    def criar(self, dto: CriarOperadorRequest) -> OperadorResponse:
        if dto.cargo not in CARGOS_VALIDOS:
            raise ValidationError(f"Cargo inválido: {dto.cargo}. Válidos: {CARGOS_VALIDOS}")
        ambiente = self._ambiente_repo.get_by_id(dto.ambiente_id)
        if ambiente is None:
            raise EntityNotFoundError("Ambiente", dto.ambiente_id)
        existente = self._repo.get_by_matricula(dto.matricula)
        if existente is not None:
            raise ValidationError(f"Matrícula '{dto.matricula}' já cadastrada.")
        operadores_ativos = [o for o in self._repo.get_by_ambiente(dto.ambiente_id) if o.ativo]
        if len(operadores_ativos) >= ambiente.capacidade_operadores:
            raise LimiteOperadoresError(ambiente.nome, ambiente.capacidade_operadores)
        modelo = OperadorModel(
            nome=dto.nome,
            cargo=dto.cargo,
            ambiente_id=dto.ambiente_id,
            matricula=dto.matricula,
        )
        criado = self._repo.create(modelo)
        return OperadorResponse.model_validate(criado)

    def atualizar(self, operador_id: int, dto: AtualizarOperadorRequest) -> OperadorResponse:
        modelo = self._repo.get_by_id(operador_id)
        if modelo is None:
            raise EntityNotFoundError("Operador", operador_id)
        if dto.nome is not None:
            modelo.nome = dto.nome
        if dto.cargo is not None:
            if dto.cargo not in CARGOS_VALIDOS:
                raise ValidationError(f"Cargo inválido: {dto.cargo}")
            modelo.cargo = dto.cargo
        if dto.ativo is not None:
            modelo.ativo = dto.ativo
        atualizado = self._repo.update(modelo)
        return OperadorResponse.model_validate(atualizado)

    def deletar(self, operador_id: int) -> bool:
        if not self._repo.delete(operador_id):
            raise EntityNotFoundError("Operador", operador_id)
        return True

    def listar_por_ambiente(self, ambiente_id: int) -> list[OperadorResponse]:
        return [OperadorResponse.model_validate(m) for m in self._repo.get_by_ambiente(ambiente_id)]

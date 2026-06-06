"""Entidade Operador — pessoa alocada em uma base de ambiente extremo."""

from __future__ import annotations

from enum import Enum

from app.domain.entities.base_entity import BaseEntity
from app.domain.exceptions.domain_exceptions import ValidationError


class CargoOperador(str, Enum):
    ENGENHEIRO = "engenheiro"
    TECNICO = "tecnico"
    MEDICO = "medico"
    COMANDANTE = "comandante"
    PESQUISADOR = "pesquisador"


class Operador(BaseEntity):
    """Operador alocado em uma base operacional."""

    def __init__(
        self,
        nome: str,
        cargo: CargoOperador,
        ambiente_id: int,
        matricula: str,
        entity_id: int | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.nome = nome
        self.cargo = cargo
        self.ambiente_id = ambiente_id
        self.matricula = matricula
        self.ativo: bool = True
        self.validate()

    def validate(self) -> None:
        if not self.nome or len(self.nome.strip()) < 2:
            raise ValidationError("Nome do operador deve ter ao menos 2 caracteres.")
        if not self.matricula or len(self.matricula.strip()) < 3:
            raise ValidationError("Matrícula deve ter ao menos 3 caracteres.")

    def desativar(self) -> None:
        self.ativo = False
        self.touch()

    def __repr__(self) -> str:
        return f"Operador(nome={self.nome!r}, cargo={self.cargo.value})"

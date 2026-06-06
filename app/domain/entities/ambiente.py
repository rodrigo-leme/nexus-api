"""Entidade Ambiente — representa uma base operacional em ambiente extremo."""

from __future__ import annotations

from enum import Enum

from app.domain.entities.base_entity import BaseEntity
from app.domain.exceptions.domain_exceptions import ValidationError


class TipoAmbiente(str, Enum):
    OFFSHORE = "offshore"
    ANTARTICA = "antartica"
    MILITAR = "militar"
    ESPACIAL = "espacial"


class StatusAmbiente(str, Enum):
    OPERACIONAL = "operacional"
    ALERTA = "alerta"
    CRITICO = "critico"
    OFFLINE = "offline"


class Ambiente(BaseEntity):
    """Base operacional em ambiente extremo (offshore, antártica, militar, espacial)."""

    def __init__(
        self,
        nome: str,
        tipo: TipoAmbiente,
        localizacao: str,
        capacidade_operadores: int,
        entity_id: int | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.nome = nome
        self.tipo = tipo
        self.localizacao = localizacao
        self.capacidade_operadores = capacidade_operadores
        self.status: StatusAmbiente = StatusAmbiente.OPERACIONAL
        self.validate()

    def validate(self) -> None:
        if not self.nome or len(self.nome.strip()) < 2:
            raise ValidationError("Nome do ambiente deve ter ao menos 2 caracteres.")
        if self.capacidade_operadores <= 0:
            raise ValidationError("Capacidade de operadores deve ser maior que zero.")

    def atualizar_status(self, novo_status: StatusAmbiente) -> None:
        self.status = novo_status
        self.touch()

    def __repr__(self) -> str:
        return f"Ambiente(nome={self.nome!r}, tipo={self.tipo.value}, status={self.status.value})"

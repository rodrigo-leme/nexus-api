"""Entidade Alerta — gerado automaticamente quando uma leitura excede limites."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from app.domain.entities.base_entity import BaseEntity
from app.domain.exceptions.domain_exceptions import ValidationError


class NivelAlerta(str, Enum):
    INFORMATIVO = "informativo"
    ALERTA = "alerta"
    CRITICO = "critico"
    EMERGENCIA = "emergencia"


class StatusAlerta(str, Enum):
    ABERTO = "aberto"
    RECONHECIDO = "reconhecido"
    RESOLVIDO = "resolvido"


class Alerta(BaseEntity):
    """Alerta gerado a partir de uma anomalia detectada por um sensor."""

    def __init__(
        self,
        sensor_id: int,
        ambiente_id: int,
        nivel: NivelAlerta,
        mensagem: str,
        valor_detectado: float,
        entity_id: int | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.sensor_id = sensor_id
        self.ambiente_id = ambiente_id
        self.nivel = nivel
        self.mensagem = mensagem
        self.valor_detectado = valor_detectado
        self.status: StatusAlerta = StatusAlerta.ABERTO
        self.resolvido_em: datetime | None = None
        self.validate()

    def validate(self) -> None:
        if not self.mensagem or len(self.mensagem.strip()) < 5:
            raise ValidationError("Mensagem do alerta deve ter ao menos 5 caracteres.")

    def reconhecer(self) -> None:
        if self.status != StatusAlerta.ABERTO:
            raise ValidationError("Apenas alertas abertos podem ser reconhecidos.")
        self.status = StatusAlerta.RECONHECIDO
        self.touch()

    def resolver(self) -> None:
        if self.status == StatusAlerta.RESOLVIDO:
            raise ValidationError("Alerta já foi resolvido.")
        self.status = StatusAlerta.RESOLVIDO
        self.resolvido_em = datetime.now(timezone.utc)
        self.touch()

    def __repr__(self) -> str:
        return f"Alerta(nivel={self.nivel.value}, status={self.status.value}, msg={self.mensagem!r})"

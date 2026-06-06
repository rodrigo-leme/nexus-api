"""Entidade Leitura — registro de telemetria de um sensor."""

from __future__ import annotations

from datetime import datetime, timezone

from app.domain.entities.base_entity import BaseEntity
from app.domain.exceptions.domain_exceptions import ValidationError


class Leitura(BaseEntity):
    """Registro individual de telemetria capturado por um sensor."""

    def __init__(
        self,
        sensor_id: int,
        valor: float,
        interpretacao: str,
        timestamp: datetime | None = None,
        entity_id: int | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.sensor_id = sensor_id
        self.valor = valor
        self.interpretacao = interpretacao
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.validate()

    def validate(self) -> None:
        if self.sensor_id is None or self.sensor_id <= 0:
            raise ValidationError("sensor_id deve ser um inteiro positivo.")

    def __repr__(self) -> str:
        return f"Leitura(sensor={self.sensor_id}, valor={self.valor}, interpretacao={self.interpretacao!r})"

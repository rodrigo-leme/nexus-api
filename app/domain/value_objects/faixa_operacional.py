"""Value Object — Faixa operacional de um sensor (imutável)."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import ValidationError


@dataclass(frozen=True)
class FaixaOperacional:
    """Define os limites operacionais de um sensor (VO imutável)."""

    minimo: float
    maximo: float
    alerta_inferior: float
    alerta_superior: float

    def __post_init__(self) -> None:
        if self.minimo >= self.maximo:
            raise ValidationError("Mínimo deve ser menor que máximo na faixa operacional.")
        if not (self.minimo <= self.alerta_inferior <= self.alerta_superior <= self.maximo):
            raise ValidationError("Faixas de alerta devem estar dentro dos limites operacionais.")

    def classificar(self, valor: float) -> str:
        if valor < self.minimo or valor > self.maximo:
            return "FORA_DE_FAIXA"
        if valor < self.alerta_inferior or valor > self.alerta_superior:
            return "ALERTA"
        return "NORMAL"

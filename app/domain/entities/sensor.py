"""Hierarquia de Sensores — demonstra herança e polimorfismo."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum

from app.domain.entities.base_entity import BaseEntity
from app.domain.exceptions.domain_exceptions import ValidationError


class TipoSensor(str, Enum):
    TEMPERATURA = "temperatura"
    PRESSAO = "pressao"
    ENERGIA = "energia"
    RADIACAO = "radiacao"
    QUALIDADE_AR = "qualidade_ar"


class StatusSensor(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    MANUTENCAO = "manutencao"
    FALHA = "falha"


class Sensor(BaseEntity):
    """Classe base abstrata para todos os sensores IoT da plataforma NEXUS."""

    def __init__(
        self,
        codigo: str,
        tipo: TipoSensor,
        ambiente_id: int,
        unidade_medida: str,
        valor_min: float,
        valor_max: float,
        entity_id: int | None = None,
    ) -> None:
        super().__init__(entity_id)
        self.codigo = codigo
        self.tipo = tipo
        self.ambiente_id = ambiente_id
        self.unidade_medida = unidade_medida
        self.valor_min = valor_min
        self.valor_max = valor_max
        self.status: StatusSensor = StatusSensor.ATIVO
        self.validate()

    def validate(self) -> None:
        if not self.codigo or len(self.codigo.strip()) < 3:
            raise ValidationError("Código do sensor deve ter ao menos 3 caracteres.")
        if self.valor_min >= self.valor_max:
            raise ValidationError("valor_min deve ser menor que valor_max.")

    @abstractmethod
    def interpretar_leitura(self, valor: float) -> str:
        """Cada tipo de sensor interpreta a leitura de forma diferente (polimorfismo)."""

    def esta_dentro_faixa(self, valor: float) -> bool:
        return self.valor_min <= valor <= self.valor_max

    def desativar(self) -> None:
        self.status = StatusSensor.INATIVO
        self.touch()

    def __repr__(self) -> str:
        return f"Sensor(codigo={self.codigo!r}, tipo={self.tipo.value})"


# ---------------------------------------------------------------------------
# Subclasses concretas — polimorfismo em interpretar_leitura
# ---------------------------------------------------------------------------

class SensorTemperatura(Sensor):
    """Sensor de temperatura (°C)."""

    def __init__(self, codigo: str, ambiente_id: int, entity_id: int | None = None) -> None:
        super().__init__(
            codigo=codigo,
            tipo=TipoSensor.TEMPERATURA,
            ambiente_id=ambiente_id,
            unidade_medida="°C",
            valor_min=-60.0,
            valor_max=80.0,
            entity_id=entity_id,
        )

    def interpretar_leitura(self, valor: float) -> str:
        if valor < -40:
            return "CRITICO_BAIXO"
        if valor > 60:
            return "CRITICO_ALTO"
        if valor < -20 or valor > 45:
            return "ALERTA"
        return "NORMAL"


class SensorPressao(Sensor):
    """Sensor de pressão atmosférica (hPa)."""

    def __init__(self, codigo: str, ambiente_id: int, entity_id: int | None = None) -> None:
        super().__init__(
            codigo=codigo,
            tipo=TipoSensor.PRESSAO,
            ambiente_id=ambiente_id,
            unidade_medida="hPa",
            valor_min=800.0,
            valor_max=1200.0,
            entity_id=entity_id,
        )

    def interpretar_leitura(self, valor: float) -> str:
        if valor < 900 or valor > 1100:
            return "CRITICO"
        if valor < 950 or valor > 1050:
            return "ALERTA"
        return "NORMAL"


class SensorEnergia(Sensor):
    """Sensor de nível de energia (kW)."""

    def __init__(self, codigo: str, ambiente_id: int, entity_id: int | None = None) -> None:
        super().__init__(
            codigo=codigo,
            tipo=TipoSensor.ENERGIA,
            ambiente_id=ambiente_id,
            unidade_medida="kW",
            valor_min=0.0,
            valor_max=5000.0,
            entity_id=entity_id,
        )

    def interpretar_leitura(self, valor: float) -> str:
        if valor < 100:
            return "CRITICO_BAIXO"
        if valor < 500:
            return "ALERTA"
        return "NORMAL"


class SensorRadiacao(Sensor):
    """Sensor de radiação solar/geomagnética (μSv/h)."""

    def __init__(self, codigo: str, ambiente_id: int, entity_id: int | None = None) -> None:
        super().__init__(
            codigo=codigo,
            tipo=TipoSensor.RADIACAO,
            ambiente_id=ambiente_id,
            unidade_medida="μSv/h",
            valor_min=0.0,
            valor_max=1000.0,
            entity_id=entity_id,
        )

    def interpretar_leitura(self, valor: float) -> str:
        if valor > 500:
            return "CRITICO_ALTO"
        if valor > 100:
            return "ALERTA"
        return "NORMAL"

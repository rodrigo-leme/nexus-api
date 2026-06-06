"""Interfaces (protocolos) de repositório — garante desacoplamento e testabilidade."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """Interface genérica de repositório (padrão Repository)."""

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def create(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...


class IAmbienteRepository(IRepository["AmbienteModel"]):
    """Interface específica para repositório de Ambientes."""

    @abstractmethod
    def get_by_tipo(self, tipo: str) -> list["AmbienteModel"]: ...


class ISensorRepository(IRepository["SensorModel"]):
    """Interface específica para repositório de Sensores."""

    @abstractmethod
    def get_by_ambiente(self, ambiente_id: int) -> list["SensorModel"]: ...

    @abstractmethod
    def get_by_codigo(self, codigo: str) -> "SensorModel | None": ...


class ILeituraRepository(IRepository["LeituraModel"]):
    """Interface específica para repositório de Leituras."""

    @abstractmethod
    def get_by_sensor(self, sensor_id: int, limit: int = 50) -> list["LeituraModel"]: ...


class IAlertaRepository(IRepository["AlertaModel"]):
    """Interface específica para repositório de Alertas."""

    @abstractmethod
    def get_by_ambiente(self, ambiente_id: int) -> list["AlertaModel"]: ...

    @abstractmethod
    def get_abertos(self) -> list["AlertaModel"]: ...


class IOperadorRepository(IRepository["OperadorModel"]):
    """Interface específica para repositório de Operadores."""

    @abstractmethod
    def get_by_ambiente(self, ambiente_id: int) -> list["OperadorModel"]: ...

    @abstractmethod
    def get_by_matricula(self, matricula: str) -> "OperadorModel | None": ...

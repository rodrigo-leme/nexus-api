"""Entidade abstrata base — fornece id e timestamps para todas as entidades do domínio."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone


class BaseEntity(ABC):
    """Classe abstrata raiz de todas as entidades persistidas."""

    def __init__(self, entity_id: int | None = None) -> None:
        self._id = entity_id
        self._created_at: datetime = datetime.now(timezone.utc)
        self._updated_at: datetime = datetime.now(timezone.utc)

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def touch(self) -> None:
        self._updated_at = datetime.now(timezone.utc)

    @abstractmethod
    def validate(self) -> None:
        """Cada entidade deve implementar suas regras de validação."""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self._id is not None and self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

"""Serviço base abstrato — padrão SOA com lógica compartilhada."""

from __future__ import annotations

from abc import ABC
from datetime import datetime, timezone


class BaseService(ABC):
    """Classe base para todos os serviços da camada SOA."""

    @staticmethod
    def agora_utc() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def formatar_timestamp(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

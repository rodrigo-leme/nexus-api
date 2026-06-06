"""DTOs de request para Leitura (telemetria)."""

from datetime import datetime

from pydantic import BaseModel, Field


class RegistrarLeituraRequest(BaseModel):
    sensor_id: int = Field(..., gt=0)
    valor: float = Field(..., examples=[25.3])
    timestamp: datetime | None = None

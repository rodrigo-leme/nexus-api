"""DTOs de response para Leitura."""

from datetime import datetime

from pydantic import BaseModel


class LeituraResponse(BaseModel):
    id: int
    sensor_id: int
    valor: float
    interpretacao: str
    timestamp: datetime
    created_at: datetime

    model_config = {"from_attributes": True}

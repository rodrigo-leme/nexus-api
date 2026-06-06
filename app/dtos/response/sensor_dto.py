"""DTOs de response para Sensor."""

from datetime import datetime

from pydantic import BaseModel


class SensorResponse(BaseModel):
    id: int
    codigo: str
    tipo: str
    ambiente_id: int
    unidade_medida: str
    valor_min: float
    valor_max: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

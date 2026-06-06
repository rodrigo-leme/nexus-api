"""DTOs de response para Alerta."""

from datetime import datetime

from pydantic import BaseModel


class AlertaResponse(BaseModel):
    id: int
    sensor_id: int
    ambiente_id: int
    nivel: str
    mensagem: str
    valor_detectado: float
    status: str
    resolvido_em: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

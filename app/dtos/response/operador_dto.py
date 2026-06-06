"""DTOs de response para Operador."""

from datetime import datetime

from pydantic import BaseModel


class OperadorResponse(BaseModel):
    id: int
    nome: str
    cargo: str
    ambiente_id: int
    matricula: str
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

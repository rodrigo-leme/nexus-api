"""DTOs de response para Ambiente."""

from datetime import datetime

from pydantic import BaseModel


class AmbienteResponse(BaseModel):
    id: int
    nome: str
    tipo: str
    localizacao: str
    capacidade_operadores: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AmbienteResumoResponse(BaseModel):
    id: int
    nome: str
    tipo: str
    status: str
    total_sensores: int = 0
    total_operadores: int = 0
    alertas_abertos: int = 0

"""DTOs de request para Ambiente."""

from pydantic import BaseModel, Field


class CriarAmbienteRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, examples=["Plataforma Atlântico Sul"])
    tipo: str = Field(..., examples=["offshore"])
    localizacao: str = Field(..., examples=["Costa do Rio de Janeiro, Brasil"])
    capacidade_operadores: int = Field(..., gt=0, examples=[50])


class AtualizarAmbienteRequest(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    localizacao: str | None = None
    capacidade_operadores: int | None = Field(None, gt=0)
    status: str | None = None

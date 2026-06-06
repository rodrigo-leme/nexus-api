"""DTOs de request para Operador."""

from pydantic import BaseModel, Field


class CriarOperadorRequest(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, examples=["Carlos Silva"])
    cargo: str = Field(..., examples=["engenheiro"])
    ambiente_id: int = Field(..., gt=0)
    matricula: str = Field(..., min_length=3, max_length=30, examples=["OP-001"])


class AtualizarOperadorRequest(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    cargo: str | None = None
    ativo: bool | None = None

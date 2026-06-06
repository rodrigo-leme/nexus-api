"""DTOs de request para Sensor."""

from pydantic import BaseModel, Field


class CriarSensorRequest(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=50, examples=["TEMP-001"])
    tipo: str = Field(..., examples=["temperatura"])
    ambiente_id: int = Field(..., gt=0)
    unidade_medida: str = Field(..., examples=["°C"])
    valor_min: float = Field(..., examples=[-60.0])
    valor_max: float = Field(..., examples=[80.0])


class AtualizarSensorRequest(BaseModel):
    status: str | None = None
    valor_min: float | None = None
    valor_max: float | None = None

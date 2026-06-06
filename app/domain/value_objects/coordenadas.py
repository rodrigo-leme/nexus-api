"""Value Object — Coordenadas geográficas (imutável)."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import ValidationError


@dataclass(frozen=True)
class Coordenadas:
    """Coordenadas geográficas de uma base operacional (VO imutável)."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValidationError(f"Latitude inválida: {self.latitude}")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValidationError(f"Longitude inválida: {self.longitude}")

    def formato_dms(self) -> str:
        """Retorna coordenadas em graus/minutos/segundos."""
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude):.4f}°{lat_dir}, {abs(self.longitude):.4f}°{lon_dir}"

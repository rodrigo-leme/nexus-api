"""Injeção de Dependência — fornece repositórios e serviços via FastAPI Depends."""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.ambiente_repository import AmbienteRepository
from app.infrastructure.repositories.alerta_repository import AlertaRepository
from app.infrastructure.repositories.leitura_repository import LeituraRepository
from app.infrastructure.repositories.operador_repository import OperadorRepository
from app.infrastructure.repositories.sensor_repository import SensorRepository
from app.services.ambiente_service import AmbienteService
from app.services.operador_service import OperadorService
from app.services.sensor_service import SensorService
from app.services.telemetria_service import TelemetriaService


# ---- Repositórios ----

def get_ambiente_repo(db: Session = Depends(get_db)) -> AmbienteRepository:
    return AmbienteRepository(db)


def get_sensor_repo(db: Session = Depends(get_db)) -> SensorRepository:
    return SensorRepository(db)


def get_leitura_repo(db: Session = Depends(get_db)) -> LeituraRepository:
    return LeituraRepository(db)


def get_alerta_repo(db: Session = Depends(get_db)) -> AlertaRepository:
    return AlertaRepository(db)


def get_operador_repo(db: Session = Depends(get_db)) -> OperadorRepository:
    return OperadorRepository(db)


# ---- Serviços (SOA) ----

def get_ambiente_service(
    repo: AmbienteRepository = Depends(get_ambiente_repo),
    alerta_repo: AlertaRepository = Depends(get_alerta_repo),
) -> AmbienteService:
    return AmbienteService(repo, alerta_repo)


def get_sensor_service(
    repo: SensorRepository = Depends(get_sensor_repo),
    ambiente_repo: AmbienteRepository = Depends(get_ambiente_repo),
) -> SensorService:
    return SensorService(repo, ambiente_repo)


def get_telemetria_service(
    leitura_repo: LeituraRepository = Depends(get_leitura_repo),
    sensor_repo: SensorRepository = Depends(get_sensor_repo),
    alerta_repo: AlertaRepository = Depends(get_alerta_repo),
) -> TelemetriaService:
    return TelemetriaService(leitura_repo, sensor_repo, alerta_repo)


def get_operador_service(
    repo: OperadorRepository = Depends(get_operador_repo),
    ambiente_repo: AmbienteRepository = Depends(get_ambiente_repo),
) -> OperadorService:
    return OperadorService(repo, ambiente_repo)

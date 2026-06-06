"""Repositório concreto de Leituras (telemetria)."""

from sqlalchemy.orm import Session

from app.domain.interfaces.repository_interface import ILeituraRepository
from app.infrastructure.database.models import LeituraModel


class LeituraRepository(ILeituraRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, entity_id: int) -> LeituraModel | None:
        return self._db.query(LeituraModel).filter(LeituraModel.id == entity_id).first()

    def get_all(self) -> list[LeituraModel]:
        return self._db.query(LeituraModel).order_by(LeituraModel.timestamp.desc()).limit(100).all()

    def create(self, entity: LeituraModel) -> LeituraModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: LeituraModel) -> LeituraModel:
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        obj = self.get_by_id(entity_id)
        if obj is None:
            return False
        self._db.delete(obj)
        self._db.commit()
        return True

    def get_by_sensor(self, sensor_id: int, limit: int = 50) -> list[LeituraModel]:
        return (
            self._db.query(LeituraModel)
            .filter(LeituraModel.sensor_id == sensor_id)
            .order_by(LeituraModel.timestamp.desc())
            .limit(limit)
            .all()
        )

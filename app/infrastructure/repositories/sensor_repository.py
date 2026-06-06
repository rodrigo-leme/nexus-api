"""Repositório concreto de Sensores."""

from sqlalchemy.orm import Session

from app.domain.interfaces.repository_interface import ISensorRepository
from app.infrastructure.database.models import SensorModel


class SensorRepository(ISensorRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, entity_id: int) -> SensorModel | None:
        return self._db.query(SensorModel).filter(SensorModel.id == entity_id).first()

    def get_all(self) -> list[SensorModel]:
        return self._db.query(SensorModel).all()

    def create(self, entity: SensorModel) -> SensorModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: SensorModel) -> SensorModel:
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

    def get_by_ambiente(self, ambiente_id: int) -> list[SensorModel]:
        return self._db.query(SensorModel).filter(SensorModel.ambiente_id == ambiente_id).all()

    def get_by_codigo(self, codigo: str) -> SensorModel | None:
        return self._db.query(SensorModel).filter(SensorModel.codigo == codigo).first()

"""Repositório concreto de Ambientes — implementa a interface IAmbienteRepository."""

from sqlalchemy.orm import Session

from app.domain.interfaces.repository_interface import IAmbienteRepository
from app.infrastructure.database.models import AmbienteModel


class AmbienteRepository(IAmbienteRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, entity_id: int) -> AmbienteModel | None:
        return self._db.query(AmbienteModel).filter(AmbienteModel.id == entity_id).first()

    def get_all(self) -> list[AmbienteModel]:
        return self._db.query(AmbienteModel).all()

    def create(self, entity: AmbienteModel) -> AmbienteModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: AmbienteModel) -> AmbienteModel:
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

    def get_by_tipo(self, tipo: str) -> list[AmbienteModel]:
        return self._db.query(AmbienteModel).filter(AmbienteModel.tipo == tipo).all()

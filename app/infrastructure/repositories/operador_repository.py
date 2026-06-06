"""Repositório concreto de Operadores."""

from sqlalchemy.orm import Session

from app.domain.interfaces.repository_interface import IOperadorRepository
from app.infrastructure.database.models import OperadorModel


class OperadorRepository(IOperadorRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, entity_id: int) -> OperadorModel | None:
        return self._db.query(OperadorModel).filter(OperadorModel.id == entity_id).first()

    def get_all(self) -> list[OperadorModel]:
        return self._db.query(OperadorModel).all()

    def create(self, entity: OperadorModel) -> OperadorModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: OperadorModel) -> OperadorModel:
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

    def get_by_ambiente(self, ambiente_id: int) -> list[OperadorModel]:
        return self._db.query(OperadorModel).filter(OperadorModel.ambiente_id == ambiente_id).all()

    def get_by_matricula(self, matricula: str) -> OperadorModel | None:
        return self._db.query(OperadorModel).filter(OperadorModel.matricula == matricula).first()

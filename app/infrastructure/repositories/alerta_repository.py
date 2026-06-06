"""Repositório concreto de Alertas."""

from sqlalchemy.orm import Session

from app.domain.interfaces.repository_interface import IAlertaRepository
from app.infrastructure.database.models import AlertaModel


class AlertaRepository(IAlertaRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, entity_id: int) -> AlertaModel | None:
        return self._db.query(AlertaModel).filter(AlertaModel.id == entity_id).first()

    def get_all(self) -> list[AlertaModel]:
        return self._db.query(AlertaModel).order_by(AlertaModel.created_at.desc()).all()

    def create(self, entity: AlertaModel) -> AlertaModel:
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: AlertaModel) -> AlertaModel:
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

    def get_by_ambiente(self, ambiente_id: int) -> list[AlertaModel]:
        return (
            self._db.query(AlertaModel)
            .filter(AlertaModel.ambiente_id == ambiente_id)
            .order_by(AlertaModel.created_at.desc())
            .all()
        )

    def get_abertos(self) -> list[AlertaModel]:
        return (
            self._db.query(AlertaModel)
            .filter(AlertaModel.status == "aberto")
            .order_by(AlertaModel.created_at.desc())
            .all()
        )

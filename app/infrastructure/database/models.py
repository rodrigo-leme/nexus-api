"""Modelos ORM — mapeamento entre entidades de domínio e tabelas do banco."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.connection import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AmbienteModel(Base):
    __tablename__ = "ambientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    localizacao: Mapped[str] = mapped_column(String(200), nullable=False)
    capacidade_operadores: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="operacional")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    sensores: Mapped[list["SensorModel"]] = relationship(back_populates="ambiente", cascade="all, delete-orphan")
    operadores: Mapped[list["OperadorModel"]] = relationship(back_populates="ambiente", cascade="all, delete-orphan")
    alertas: Mapped[list["AlertaModel"]] = relationship(back_populates="ambiente", cascade="all, delete-orphan")


class SensorModel(Base):
    __tablename__ = "sensores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    ambiente_id: Mapped[int] = mapped_column(Integer, ForeignKey("ambientes.id"), nullable=False)
    unidade_medida: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_min: Mapped[float] = mapped_column(Float, nullable=False)
    valor_max: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ativo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    ambiente: Mapped["AmbienteModel"] = relationship(back_populates="sensores")
    leituras: Mapped[list["LeituraModel"]] = relationship(back_populates="sensor", cascade="all, delete-orphan")


class LeituraModel(Base):
    __tablename__ = "leituras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensores.id"), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    interpretacao: Mapped[str] = mapped_column(String(30), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    sensor: Mapped["SensorModel"] = relationship(back_populates="leituras")


class AlertaModel(Base):
    __tablename__ = "alertas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensores.id"), nullable=False)
    ambiente_id: Mapped[int] = mapped_column(Integer, ForeignKey("ambientes.id"), nullable=False)
    nivel: Mapped[str] = mapped_column(String(20), nullable=False)
    mensagem: Mapped[str] = mapped_column(String(500), nullable=False)
    valor_detectado: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="aberto")
    resolvido_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    ambiente: Mapped["AmbienteModel"] = relationship(back_populates="alertas")


class OperadorModel(Base):
    __tablename__ = "operadores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo: Mapped[str] = mapped_column(String(30), nullable=False)
    ambiente_id: Mapped[int] = mapped_column(Integer, ForeignKey("ambientes.id"), nullable=False)
    matricula: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    ambiente: Mapped["AmbienteModel"] = relationship(back_populates="operadores")

"""Serviço de Telemetria — ingestão de leituras + geração automática de alertas."""

from datetime import datetime, timezone

from app.domain.exceptions.domain_exceptions import EntityNotFoundError, SensorOfflineError
from app.dtos.request.leitura_dto import RegistrarLeituraRequest
from app.dtos.response.alerta_dto import AlertaResponse
from app.dtos.response.leitura_dto import LeituraResponse
from app.infrastructure.database.models import AlertaModel, LeituraModel
from app.infrastructure.repositories.alerta_repository import AlertaRepository
from app.infrastructure.repositories.leitura_repository import LeituraRepository
from app.infrastructure.repositories.sensor_repository import SensorRepository
from app.services.base_service import BaseService


class TelemetriaService(BaseService):
    """Microsserviço SOA responsável por ingestão de telemetria e geração de alertas."""

    def __init__(
        self,
        leitura_repo: LeituraRepository,
        sensor_repo: SensorRepository,
        alerta_repo: AlertaRepository,
    ) -> None:
        self._leitura_repo = leitura_repo
        self._sensor_repo = sensor_repo
        self._alerta_repo = alerta_repo

    def registrar_leitura(self, dto: RegistrarLeituraRequest) -> LeituraResponse:
        sensor = self._sensor_repo.get_by_id(dto.sensor_id)
        if sensor is None:
            raise EntityNotFoundError("Sensor", dto.sensor_id)
        if sensor.status in ("inativo", "falha"):
            raise SensorOfflineError(sensor.codigo)

        interpretacao = self._interpretar_valor(sensor.tipo, dto.valor, sensor.valor_min, sensor.valor_max)

        modelo = LeituraModel(
            sensor_id=dto.sensor_id,
            valor=dto.valor,
            interpretacao=interpretacao,
            timestamp=dto.timestamp or self.agora_utc(),
        )
        leitura = self._leitura_repo.create(modelo)

        if interpretacao not in ("NORMAL",):
            self._gerar_alerta(sensor, dto.valor, interpretacao)

        return LeituraResponse.model_validate(leitura)

    def listar_leituras(self, sensor_id: int | None = None, limit: int = 50) -> list[LeituraResponse]:
        if sensor_id:
            modelos = self._leitura_repo.get_by_sensor(sensor_id, limit)
        else:
            modelos = self._leitura_repo.get_all()
        return [LeituraResponse.model_validate(m) for m in modelos]

    def listar_alertas(self, apenas_abertos: bool = False) -> list[AlertaResponse]:
        if apenas_abertos:
            modelos = self._alerta_repo.get_abertos()
        else:
            modelos = self._alerta_repo.get_all()
        return [AlertaResponse.model_validate(m) for m in modelos]

    def resolver_alerta(self, alerta_id: int) -> AlertaResponse:
        alerta = self._alerta_repo.get_by_id(alerta_id)
        if alerta is None:
            raise EntityNotFoundError("Alerta", alerta_id)
        alerta.status = "resolvido"
        alerta.resolvido_em = self.agora_utc()
        atualizado = self._alerta_repo.update(alerta)
        return AlertaResponse.model_validate(atualizado)

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    @staticmethod
    def _interpretar_valor(tipo: str, valor: float, val_min: float, val_max: float) -> str:
        """Interpreta a leitura de acordo com o tipo de sensor (polimorfismo estático)."""
        if tipo == "temperatura":
            if valor < -40 or valor > 60:
                return "CRITICO"
            if valor < -20 or valor > 45:
                return "ALERTA"
            return "NORMAL"
        elif tipo == "pressao":
            if valor < 900 or valor > 1100:
                return "CRITICO"
            if valor < 950 or valor > 1050:
                return "ALERTA"
            return "NORMAL"
        elif tipo == "energia":
            if valor < 100:
                return "CRITICO"
            if valor < 500:
                return "ALERTA"
            return "NORMAL"
        elif tipo == "radiacao":
            if valor > 500:
                return "CRITICO"
            if valor > 100:
                return "ALERTA"
            return "NORMAL"
        else:
            if valor < val_min or valor > val_max:
                return "CRITICO"
            return "NORMAL"

    def _gerar_alerta(self, sensor, valor: float, interpretacao: str) -> None:
        nivel = "critico" if "CRITICO" in interpretacao else "alerta"
        mensagem = (
            f"Sensor {sensor.codigo} ({sensor.tipo}): valor {valor} {sensor.unidade_medida} "
            f"detectado como {interpretacao}."
        )
        alerta = AlertaModel(
            sensor_id=sensor.id,
            ambiente_id=sensor.ambiente_id,
            nivel=nivel,
            mensagem=mensagem,
            valor_detectado=valor,
        )
        self._alerta_repo.create(alerta)

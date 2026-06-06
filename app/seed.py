"""Script de seed — popula o banco de dados com dados de exemplo para demonstração."""

from datetime import datetime, timezone, timedelta

from app.infrastructure.database.connection import SessionLocal, create_tables
from app.infrastructure.database.models import (
    AlertaModel,
    AmbienteModel,
    LeituraModel,
    OperadorModel,
    SensorModel,
)


def seed() -> None:
    create_tables()
    db = SessionLocal()

    try:
        if db.query(AmbienteModel).count() > 0:
            print("Banco já possui dados. Seed ignorado.")
            return

        # -- Ambientes --
        ambientes = [
            AmbienteModel(
                nome="Plataforma Atlântico Sul",
                tipo="offshore",
                localizacao="Costa do Rio de Janeiro, Brasil (-22.9068, -43.1729)",
                capacidade_operadores=50,
                status="operacional",
            ),
            AmbienteModel(
                nome="Base Comandante Ferraz",
                tipo="antartica",
                localizacao="Baía do Almirantado, Antártida (-62.0849, -58.3915)",
                capacidade_operadores=30,
                status="operacional",
            ),
            AmbienteModel(
                nome="Centro de Operações Delta",
                tipo="militar",
                localizacao="Região Norte, Brasil (-3.1190, -60.0217)",
                capacidade_operadores=100,
                status="alerta",
            ),
        ]
        db.add_all(ambientes)
        db.commit()

        for a in ambientes:
            db.refresh(a)

        # -- Sensores --
        sensores = [
            SensorModel(codigo="TEMP-OFF-001", tipo="temperatura", ambiente_id=ambientes[0].id, unidade_medida="°C", valor_min=-10.0, valor_max=60.0),
            SensorModel(codigo="PRESS-OFF-001", tipo="pressao", ambiente_id=ambientes[0].id, unidade_medida="hPa", valor_min=900.0, valor_max=1100.0),
            SensorModel(codigo="ENRG-OFF-001", tipo="energia", ambiente_id=ambientes[0].id, unidade_medida="kW", valor_min=0.0, valor_max=5000.0),
            SensorModel(codigo="TEMP-ANT-001", tipo="temperatura", ambiente_id=ambientes[1].id, unidade_medida="°C", valor_min=-60.0, valor_max=10.0),
            SensorModel(codigo="RAD-ANT-001", tipo="radiacao", ambiente_id=ambientes[1].id, unidade_medida="μSv/h", valor_min=0.0, valor_max=500.0),
            SensorModel(codigo="TEMP-MIL-001", tipo="temperatura", ambiente_id=ambientes[2].id, unidade_medida="°C", valor_min=10.0, valor_max=50.0),
            SensorModel(codigo="ENRG-MIL-001", tipo="energia", ambiente_id=ambientes[2].id, unidade_medida="kW", valor_min=0.0, valor_max=10000.0),
        ]
        db.add_all(sensores)
        db.commit()

        for s in sensores:
            db.refresh(s)

        # -- Operadores --
        operadores = [
            OperadorModel(nome="Carlos Silva", cargo="engenheiro", ambiente_id=ambientes[0].id, matricula="OP-001"),
            OperadorModel(nome="Ana Pereira", cargo="medico", ambiente_id=ambientes[0].id, matricula="OP-002"),
            OperadorModel(nome="Dr. Marcos Oliveira", cargo="pesquisador", ambiente_id=ambientes[1].id, matricula="OP-003"),
            OperadorModel(nome="Tenente Ribeiro", cargo="comandante", ambiente_id=ambientes[2].id, matricula="OP-004"),
            OperadorModel(nome="João Santos", cargo="tecnico", ambiente_id=ambientes[2].id, matricula="OP-005"),
        ]
        db.add_all(operadores)
        db.commit()

        # -- Leituras de telemetria --
        agora = datetime.now(timezone.utc)
        leituras = [
            LeituraModel(sensor_id=sensores[0].id, valor=28.5, interpretacao="NORMAL", timestamp=agora - timedelta(hours=3)),
            LeituraModel(sensor_id=sensores[0].id, valor=35.2, interpretacao="NORMAL", timestamp=agora - timedelta(hours=2)),
            LeituraModel(sensor_id=sensores[0].id, valor=48.0, interpretacao="ALERTA", timestamp=agora - timedelta(hours=1)),
            LeituraModel(sensor_id=sensores[1].id, valor=1013.0, interpretacao="NORMAL", timestamp=agora - timedelta(hours=2)),
            LeituraModel(sensor_id=sensores[2].id, valor=2500.0, interpretacao="NORMAL", timestamp=agora - timedelta(hours=1)),
            LeituraModel(sensor_id=sensores[3].id, valor=-45.0, interpretacao="CRITICO", timestamp=agora - timedelta(minutes=30)),
            LeituraModel(sensor_id=sensores[4].id, valor=150.0, interpretacao="ALERTA", timestamp=agora - timedelta(minutes=15)),
        ]
        db.add_all(leituras)
        db.commit()

        # -- Alertas --
        alertas = [
            AlertaModel(
                sensor_id=sensores[0].id,
                ambiente_id=ambientes[0].id,
                nivel="alerta",
                mensagem="Sensor TEMP-OFF-001 (temperatura): valor 48.0 °C detectado como ALERTA.",
                valor_detectado=48.0,
                status="aberto",
            ),
            AlertaModel(
                sensor_id=sensores[3].id,
                ambiente_id=ambientes[1].id,
                nivel="critico",
                mensagem="Sensor TEMP-ANT-001 (temperatura): valor -45.0 °C detectado como CRITICO.",
                valor_detectado=-45.0,
                status="aberto",
            ),
            AlertaModel(
                sensor_id=sensores[4].id,
                ambiente_id=ambientes[1].id,
                nivel="alerta",
                mensagem="Sensor RAD-ANT-001 (radiacao): valor 150.0 μSv/h detectado como ALERTA.",
                valor_detectado=150.0,
                status="aberto",
            ),
        ]
        db.add_all(alertas)
        db.commit()

        print("Seed concluído com sucesso!")
        print(f"  - {len(ambientes)} ambientes")
        print(f"  - {len(sensores)} sensores")
        print(f"  - {len(operadores)} operadores")
        print(f"  - {len(leituras)} leituras")
        print(f"  - {len(alertas)} alertas")

    finally:
        db.close()


if __name__ == "__main__":
    seed()

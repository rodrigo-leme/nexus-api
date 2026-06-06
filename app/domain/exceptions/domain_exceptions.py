"""Exceções de domínio — tratamento específico para sistemas críticos espaciais."""


class NexusBaseException(Exception):
    """Exceção base de toda a aplicação NEXUS."""

    def __init__(self, message: str, code: str = "NEXUS_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(NexusBaseException):
    """Dados de entrada inválidos."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class EntityNotFoundError(NexusBaseException):
    """Entidade não encontrada no banco de dados."""

    def __init__(self, entity_type: str, entity_id: int) -> None:
        super().__init__(
            f"{entity_type} com id={entity_id} não encontrado.",
            code="NOT_FOUND",
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class SensorOfflineError(NexusBaseException):
    """Tentativa de leitura em sensor offline ou em falha."""

    def __init__(self, sensor_codigo: str) -> None:
        super().__init__(
            f"Sensor '{sensor_codigo}' está offline ou em falha. Leitura ignorada.",
            code="SENSOR_OFFLINE",
        )


class LimiteOperadoresError(NexusBaseException):
    """Base atingiu a capacidade máxima de operadores."""

    def __init__(self, ambiente_nome: str, capacidade: int) -> None:
        super().__init__(
            f"Ambiente '{ambiente_nome}' atingiu capacidade máxima de {capacidade} operadores.",
            code="LIMITE_OPERADORES",
        )


class AlertaJaResolvidoError(NexusBaseException):
    """Tentativa de resolver um alerta já resolvido."""

    def __init__(self, alerta_id: int) -> None:
        super().__init__(
            f"Alerta id={alerta_id} já foi resolvido anteriormente.",
            code="ALERTA_JA_RESOLVIDO",
        )


class DatabaseError(NexusBaseException):
    """Erro de conexão ou operação no banco de dados."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="DATABASE_ERROR")

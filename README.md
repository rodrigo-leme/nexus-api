# NEXUS API

**Sistema Operacional para Ambientes Extremos**

> _"Onde o comum não alcança."_

## Motivação

Plataformas offshore, bases na Antártida e instalações militares operam em condições onde **falha = fatalidade**. Hoje, esses ambientes funcionam com sistemas fragmentados, isolados e reativos — sem integração entre sensores, operadores e protocolos de contingência.

O **NEXUS** é uma plataforma SOA inspirada nos protocolos de resiliência da NASA/ISS, projetada para unificar telemetria em tempo real, monitoramento de operadores e geração automática de alertas preditivos em uma única API resiliente.

### Como se integra à Global Solution

Este projeto implementa o backend (API REST) do ecossistema NEXUS, responsável por:
- Gerenciar **ambientes extremos** (offshore, antártica, militar, espacial)
- Controlar **sensores IoT** com leituras de telemetria em tempo real
- Gerar **alertas automáticos** quando anomalias são detectadas
- Gerenciar **operadores** alocados em cada base

---

## Arquitetura & Requisitos Técnicos

### SOA (Service-Oriented Architecture)

A aplicação segue o padrão SOA com microsserviços independentes:

```
┌──────────────────────────────────────────────────────────────┐
│                        NEXUS API                             │
├──────────────┬──────────────┬────────────┬───────────────────┤
│  Ambiente    │   Sensor     │ Telemetria │   Operador        │
│  Service     │   Service    │  Service   │   Service         │
├──────────────┴──────────────┴────────────┴───────────────────┤
│              Camada de Repositórios (Interfaces)             │
├──────────────────────────────────────────────────────────────┤
│              SQLAlchemy ORM + SQLite                         │
└──────────────────────────────────────────────────────────────┘
```

### Modelagem de Domínio & POO

| Conceito | Implementação |
|---|---|
| **Classe Abstrata** | `BaseEntity` — entidade raiz com `id`, timestamps e `validate()` abstrato |
| **Herança** | `Sensor` → `SensorTemperatura`, `SensorPressao`, `SensorEnergia`, `SensorRadiacao` |
| **Polimorfismo** | `interpretar_leitura(valor)` — cada tipo de sensor interpreta diferente |
| **Classes Públicas/Privadas** | Atributos protegidos (`_id`, `_created_at`) com `@property` |
| **Enums** | `TipoAmbiente`, `StatusSensor`, `NivelAlerta`, `CargoOperador` |

### Abstração e Interfaces

- **`IRepository[T]`** — Interface genérica (ABC) para todos os repositórios
- **Interfaces específicas**: `IAmbienteRepository`, `ISensorRepository`, `ILeituraRepository`, `IAlertaRepository`, `IOperadorRepository`
- **Injeção de Dependência**: via `FastAPI Depends()` em `app/api/dependencies/deps.py`

### Value Objects (VO) e DTOs

- **VOs imutáveis**: `Coordenadas` (lat/lon com validação) e `FaixaOperacional` (limites de sensor)
- **DTOs de Request**: `CriarAmbienteRequest`, `RegistrarLeituraRequest`, etc.
- **DTOs de Response**: `AmbienteResponse`, `AlertaResponse`, `AmbienteResumoResponse`, etc.

### Tratamento de Exceções

Hierarquia de exceções específicas do domínio:

```
NexusBaseException
├── ValidationError          (422)
├── EntityNotFoundError      (404)
├── SensorOfflineError       (409)
├── LimiteOperadoresError    (409)
├── AlertaJaResolvidoError   (409)
└── DatabaseError            (500)
```

Handlers globais registrados em `app/api/exception_handlers.py`.

### Conexão com Banco de Dados

- **ORM**: SQLAlchemy 2.0 com Mapped columns
- **Banco**: SQLite (arquivo `nexus.db`)
- **Modelos**: `AmbienteModel`, `SensorModel`, `LeituraModel`, `AlertaModel`, `OperadorModel`
- **Relacionamentos**: Foreign Keys com cascade delete

---

## Diagrama de Fluxo

### Fluxo de Ingestão de Telemetria

```
ESP32/Sensor IoT
      │
      ▼
POST /api/v1/telemetria/leituras
      │
      ▼
┌─────────────────┐
│ TelemetriaService│
│                 │
│ 1. Valida sensor│
│ 2. Verifica     │
│    status ativo │
│ 3. Interpreta   │
│    leitura      │
│ 4. Persiste     │
│    leitura      │
│ 5. Se anomalia: │
│    gera alerta  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
 Leitura   Alerta
  (DB)      (DB)
```

### Fluxo de Gerenciamento de Operadores

```
POST /api/v1/operadores
         │
         ▼
┌──────────────────┐
│ OperadorService  │
│                  │
│ 1. Valida cargo  │
│ 2. Verifica      │
│    ambiente      │
│ 3. Checa         │
│    matrícula     │
│    duplicada     │
│ 4. Verifica      │
│    capacidade    │
│    máxima        │
│ 5. Persiste      │
└──────────────────┘
```

---

## Estrutura de Pastas

```
nexus-api/
├── app/
│   ├── main.py                          # Ponto de entrada FastAPI
│   ├── seed.py                          # Script de seed para dados de exemplo
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── base_entity.py           # Classe abstrata base
│   │   │   ├── ambiente.py              # Entidade Ambiente
│   │   │   ├── sensor.py               # Hierarquia de Sensores (herança)
│   │   │   ├── leitura.py              # Entidade Leitura (telemetria)
│   │   │   ├── alerta.py               # Entidade Alerta
│   │   │   └── operador.py             # Entidade Operador
│   │   ├── interfaces/
│   │   │   └── repository_interface.py  # Interfaces ABC de repositório
│   │   ├── value_objects/
│   │   │   ├── coordenadas.py           # VO Coordenadas geográficas
│   │   │   └── faixa_operacional.py     # VO Faixa operacional do sensor
│   │   └── exceptions/
│   │       └── domain_exceptions.py     # Exceções específicas do domínio
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── connection.py            # Configuração SQLAlchemy + SQLite
│   │   │   └── models.py               # Modelos ORM
│   │   └── repositories/
│   │       ├── ambiente_repository.py   # Repositório de Ambientes
│   │       ├── sensor_repository.py     # Repositório de Sensores
│   │       ├── leitura_repository.py    # Repositório de Leituras
│   │       ├── alerta_repository.py     # Repositório de Alertas
│   │       └── operador_repository.py   # Repositório de Operadores
│   ├── services/
│   │   ├── base_service.py              # Serviço base abstrato
│   │   ├── ambiente_service.py          # Serviço SOA de Ambientes
│   │   ├── sensor_service.py            # Serviço SOA de Sensores
│   │   ├── telemetria_service.py        # Serviço SOA de Telemetria + Alertas
│   │   └── operador_service.py          # Serviço SOA de Operadores
│   ├── api/
│   │   ├── exception_handlers.py        # Handlers globais de exceção
│   │   ├── routers/
│   │   │   ├── ambiente_router.py       # Endpoints de Ambientes
│   │   │   ├── sensor_router.py         # Endpoints de Sensores
│   │   │   ├── telemetria_router.py     # Endpoints de Telemetria
│   │   │   └── operador_router.py       # Endpoints de Operadores
│   │   └── dependencies/
│   │       └── deps.py                  # Injeção de Dependência (FastAPI)
│   └── dtos/
│       ├── request/                     # DTOs de entrada
│       │   ├── ambiente_dto.py
│       │   ├── sensor_dto.py
│       │   ├── leitura_dto.py
│       │   └── operador_dto.py
│       └── response/                    # DTOs de saída
│           ├── ambiente_dto.py
│           ├── sensor_dto.py
│           ├── leitura_dto.py
│           ├── alerta_dto.py
│           └── operador_dto.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Como Executar

### Pré-requisitos

- Python 3.12+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/rodrigo-leme/nexus-api.git
cd nexus-api

# Instale as dependências
pip install -r requirements.txt

# Popule o banco com dados de exemplo
python -m app.seed

# Inicie o servidor
uvicorn app.main:app --reload
```

### Acesso

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Endpoints da API

### Ambientes
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/ambientes/` | Listar todos os ambientes |
| GET | `/api/v1/ambientes/{id}` | Buscar ambiente por ID |
| GET | `/api/v1/ambientes/{id}/resumo` | Dashboard resumido do ambiente |
| POST | `/api/v1/ambientes/` | Criar novo ambiente |
| PUT | `/api/v1/ambientes/{id}` | Atualizar ambiente |
| DELETE | `/api/v1/ambientes/{id}` | Deletar ambiente |
| GET | `/api/v1/ambientes/tipo/{tipo}` | Filtrar por tipo |

### Sensores
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/sensores/` | Listar todos os sensores |
| GET | `/api/v1/sensores/{id}` | Buscar sensor por ID |
| POST | `/api/v1/sensores/` | Criar novo sensor |
| PUT | `/api/v1/sensores/{id}` | Atualizar sensor |
| DELETE | `/api/v1/sensores/{id}` | Deletar sensor |
| GET | `/api/v1/sensores/ambiente/{id}` | Sensores de um ambiente |

### Telemetria
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/telemetria/leituras` | Registrar leitura de sensor |
| GET | `/api/v1/telemetria/leituras` | Listar leituras (filtro por sensor) |
| GET | `/api/v1/telemetria/alertas` | Listar alertas (filtro abertos) |
| PATCH | `/api/v1/telemetria/alertas/{id}/resolver` | Resolver um alerta |

### Operadores
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/operadores/` | Listar todos os operadores |
| GET | `/api/v1/operadores/{id}` | Buscar operador por ID |
| POST | `/api/v1/operadores/` | Criar novo operador |
| PUT | `/api/v1/operadores/{id}` | Atualizar operador |
| DELETE | `/api/v1/operadores/{id}` | Deletar operador |
| GET | `/api/v1/operadores/ambiente/{id}` | Operadores de um ambiente |

---

## Integrantes

| Nome | RM |
|------|-----|
| Fabrini | - |
| Cezar | - |
| Rodrigo | - |

---

## Licença

Projeto acadêmico — FIAP Global Solution 2025.

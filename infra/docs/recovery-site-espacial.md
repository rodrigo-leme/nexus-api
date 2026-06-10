# Plano de Recovery Site em Datacenter Espacial — Space Code LTDA

Atividade complementar da Global Solutions: plano de criação de um segundo
"data center" (recovery site) da infraestrutura da Space Code em órbita,
alinhado aos pilares de ESG e sustentabilidade.

## 1. Visão Geral

| | Site Primário (Terra) | Recovery Site (Órbita Baixa - LEO) |
|---|---|---|
| Localização | Azure (Brazil South) | Constelação LEO (~550 km) |
| Função | Produção (AD, DNS, IIS) | Réplica passiva (warm standby) |
| Energia | Rede elétrica + UPS | Painéis solares (zero emissão) |
| Refrigeração | HVAC | Radiadores no vácuo (sem água) |
| RPO / RTO | — | RPO ≤ 15 min · RTO ≤ 1 h |

## 2. Conectividade Terra × Espaço

- **Enlace principal:** laser óptico intersatelital + downlink Ka-band (estilo Starlink),
  latência Terra↔LEO de ~20–40 ms — viável para replicação assíncrona.
- **Enlace de contingência:** RF banda S de menor largura, apenas para heartbeat,
  controle e replicação delta do AD.
- **Janelas de visibilidade:** constelação com múltiplos satélites e roteamento
  inter-satelital garante cobertura contínua (sem "janela cega").
- **Segurança do enlace:** TLS 1.3 + VPN IPsec site-to-site; chaves rotacionadas
  via HSM em ambos os sites.

## 3. Replicação de Serviços

| Serviço | Estratégia de replicação |
|---|---|
| **Active Directory** | RODC (Read-Only Domain Controller) orbital em site AD dedicado (`Site-LEO`), replicação assíncrona agendada nas janelas de maior banda |
| **DNS** | Zonas integradas ao AD replicam junto; zona `spacecode.internal` com transferência de zona secundária |
| **IIS / Site institucional** | Conteúdo estático sincronizado via DFS-R; `contatos.json` replicado com fila local (offline-first) |
| **Dados / VMs** | Snapshots incrementais (Azure Site Recovery-like) enviados a cada 15 min |

## 4. Desenvolvimento Replicado em Terra e no Espaço

- Repositórios Git espelhados (push automático Terra → órbita).
- Pipeline CI/CD com *runners* nos dois sites: o artefato aprovado em Terra é
  promovido automaticamente ao ambiente orbital.
- Feature flags para degradação graciosa quando o enlace estiver restrito.

## 5. Failover e Failback

1. **Detecção:** heartbeat a cada 30 s; 3 falhas consecutivas iniciam o protocolo.
2. **Failover:** RODC orbital promovido a DC gravável; DNS público aponta para o
   gateway orbital; IIS orbital assume com o último conteúdo sincronizado.
3. **Operação degradada:** somente serviços críticos (autenticação, site, telemetria).
4. **Failback:** ao restaurar o site terrestre, replicação reversa de deltas,
   verificação de consistência (USN/SYSVOL) e devolução gradual do tráfego.

## 6. ESG e Sustentabilidade

- **Ambiental:** energia 100% solar e refrigeração passiva no vácuo — elimina o
  consumo de água e a pegada de carbono da refrigeração, principal desafio dos
  datacenters de IA em Terra.
- **Social:** continuidade de serviços críticos que protegem operadores em
  ambientes extremos.
- **Governança:** trilha de auditoria replicada e imutável nos dois sites;
  conformidade LGPD/ISO 27001.

## 7. Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Radiação (bit-flip) | Hardware rad-hardened + ECC + scrubbing de memória |
| Detritos orbitais | Redundância N+1 entre satélites da constelação |
| Perda prolongada de enlace | Operação autônoma com fila offline e reconciliação posterior |
| Custo de lançamento | Módulos padronizados em rideshare; ROI via PUE ~1.0 |

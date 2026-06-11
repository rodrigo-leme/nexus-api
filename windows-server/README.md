# Infraestrutura Windows Server — Space Code LTDA

Scripts PowerShell para configuracao completa da infraestrutura da **Space Code LTDA** no Windows Server 2022.

## Pre-requisitos

- Windows Server 2022 (ou 2019+)
- Executar todos os scripts como **Administrador**
- Maquina cliente com Windows 10/11

## Ordem de Execucao

### No Servidor

```powershell
# 1. Active Directory (promove a DC + cria usuarios/grupos/OUs)
.\setup-ad.ps1

# >>> REINICIAR O SERVIDOR <<<

# 2. Group Policy Objects (politicas de bloqueio + wallpaper)
.\setup-gpo.ps1

# 3. DNS (zona direta para o site)
.\setup-dns.ps1

# 4. IIS (instala e configura o site institucional)
.\setup-iis.ps1
```

### Na Maquina Cliente

```powershell
# 5. Ingressar no dominio
.\join-client.ps1 -ServerIP <IP_DO_SERVIDOR>
```

Ou use o script mestre:

```powershell
.\setup-all.ps1
```

## Estrutura Criada

### Active Directory
| Item | Detalhes |
|------|---------|
| Dominio | `spacecode.local` |
| OUs | Back, Front, PM |
| Sub-OUs | Back_Devs, Front_Devs, PM_Users |
| Grupos | GRP_Back (5), GRP_Front (3), GRP_PM (2) |
| Usuarios | 10 funcionarios |
| Senha Inicial | `SpaceCode@2026` |
| Alterar Senha | `rodrigo.leme` (primeiro login) |

### GPOs
| GPO | OU | Bloqueios |
|-----|-----|-----------|
| GPO_Back | Back | Painel de Controle, USB, Regedit |
| GPO_Front | Front | Painel de Controle, USB, Regedit |
| GPO_PM | PM | Painel de Controle, USB, Regedit, CMD, Gerenciador de Tarefas |
| Wallpaper | Todos | Wallpaper corporativo NEXUS/Space Code |

### DNS
| Registro | Tipo | Destino |
|----------|------|---------|
| spacecode.internal | A | IP do servidor |
| www.spacecode.internal | A | IP do servidor |
| api.spacecode.internal | A | IP do servidor |

### IIS
| Item | Valor |
|------|-------|
| Site | SpaceCode |
| URL | http://spacecode.internal |
| Pasta | C:\inetpub\spacecode |
| Form | Salva em data/contatos.json |

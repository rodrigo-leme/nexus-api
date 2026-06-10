# Space Code LTDA — Infraestrutura Windows Server (Global Solutions)

Automação completa da infraestrutura da software house **Space Code LTDA**:
Active Directory, DNS e IIS em Windows Server 2019+ (Azure ou VirtualBox).

## Estrutura

```
infra/
├── scripts/                       # Automação PowerShell (executar em ordem)
│   ├── 01-instalar-roles.ps1      # AD DS, DNS, IIS (+ASP) e GPMC
│   ├── 02-promover-dc.ps1         # Nova floresta spacecode.local (REINICIA o servidor)
│   ├── 03-criar-ous-grupos-usuarios.ps1  # OUs, Sub-OUs, grupos e 10 usuários
│   ├── 04-criar-gpos.ps1          # GPOs Back/Front/PM + Wallpaper
│   ├── 05-configurar-dns.ps1      # Zona direta spacecode.internal + registros A
│   └── 06-publicar-site-iis.ps1   # Publica o site institucional no IIS
├── site/                          # Site institucional (HTML/CSS/ASP)
│   ├── index.html                 # Quem somos, devs e formulário de contato
│   ├── salvar-contato.asp         # Grava o form em data/contatos.json
│   ├── css/style.css
│   └── img/                       # Fotos dos devs e wallpaper corporativo
└── docs/
    └── recovery-site-espacial.md  # Plano do recovery site em datacenter espacial
```

## Como executar

Em um PowerShell **como Administrador**, na raiz do repositório:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
.\infra\scripts\01-instalar-roles.ps1
.\infra\scripts\02-promover-dc.ps1     # o servidor reinicia automaticamente
# ... após o reboot, logar como SPACECODE\Administrator
.\infra\scripts\03-criar-ous-grupos-usuarios.ps1
.\infra\scripts\04-criar-gpos.ps1
.\infra\scripts\05-configurar-dns.ps1
.\infra\scripts\06-publicar-site-iis.ps1
```

Depois acesse `http://spacecode.internal` no Microsoft Edge.

## Mapeamento Requisito → Implementação

| Requisito (PDF) | Implementação |
|---|---|
| AD: 10 usuários | `03-criar-ous-grupos-usuarios.ps1` — 10 funcionários |
| Grupos Back (5) / Front (3) / PM (2) | Grupos de segurança com membros distribuídos |
| OUs Back, Front, PM | OUs principais na raiz do domínio |
| Sub-OUs Back_Devs, Front_Devs, PM_Users | Criadas dentro das OUs principais |
| 1 usuário "alterar senha no 1º login" | `ana.souza` (`-ChangePasswordAtLogon $true`) |
| GPO Back/Front: bloquear Painel de Controle, USB, Regedit | `GPO_Back` / `GPO_Front` vinculadas às OUs |
| GPO PM: + bloquear CMD e Gerenciador de Tarefas | `GPO_PM` vinculada à OU PM |
| Wallpaper único para todos | `GPO_Wallpaper` no domínio (imagem via NETLOGON) |
| Cliente adicionado ao domínio | `Add-Computer -DomainName spacecode.local` no cliente |
| DNS: zona direta do site | Zona `spacecode.internal` + registros A (`@` e `www`) |
| IIS: site institucional | Site `SpaceCode` com host headers na porta 80 |
| Form (Nome, Sobrenome, Mensagem) obrigatório → JSON | `salvar-contato.asp` grava em `data/contatos.json` |
| Recovery site espacial (atividade complementar) | `docs/recovery-site-espacial.md` + apresentação |

## Credenciais padrão (ambiente de laboratório)

- Usuários do AD: senha inicial `SpaceCode@2026!`
- `ana.souza` é obrigada a trocar a senha no primeiro login

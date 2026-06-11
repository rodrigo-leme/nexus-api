<#
.SYNOPSIS
    Script de configuracao do DNS para Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Este script:
    1. Instala o role DNS Server (se necessario)
    2. Cria a zona de pesquisa direta para o site
    3. Cria registros A e CNAME para o site institucional

.NOTES
    O DNS ja eh instalado junto com o AD DS,
    mas este script garante a configuracao da zona do site.
    Executar como Administrador no Domain Controller.
#>

param(
    [string]$SiteZone = "spacecode.internal",
    [string]$ServerIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" } | Select-Object -First 1 -ExpandProperty IPAddress)
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " SPACE CODE LTDA - Setup DNS"                -ForegroundColor Cyan
Write-Host " Zona: $SiteZone"                            -ForegroundColor Cyan
Write-Host " IP do Servidor: $ServerIP"                  -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ============================================================
# ETAPA 1 - Verificar/Instalar role DNS
# ============================================================
Write-Host "`n[1/4] Verificando role DNS Server..." -ForegroundColor Yellow

$dnsFeature = Get-WindowsFeature DNS
if ($dnsFeature.Installed) {
    Write-Host "  -> DNS Server ja esta instalado." -ForegroundColor Green
} else {
    Write-Host "  -> Instalando DNS Server..." -ForegroundColor Yellow
    Install-WindowsFeature -Name DNS -IncludeManagementTools
    Write-Host "  -> DNS Server instalado com sucesso." -ForegroundColor Green
}

# ============================================================
# ETAPA 2 - Criar Zona de Pesquisa Direta
# ============================================================
Write-Host "`n[2/4] Criando zona de pesquisa direta: $SiteZone..." -ForegroundColor Yellow

$existingZone = Get-DnsServerZone -Name $SiteZone -ErrorAction SilentlyContinue
if (-not $existingZone) {
    Add-DnsServerPrimaryZone -Name $SiteZone -ZoneFile "$SiteZone.dns" -DynamicUpdate None
    Write-Host "  -> Zona criada: $SiteZone" -ForegroundColor Green
} else {
    Write-Host "  -> Zona ja existe: $SiteZone" -ForegroundColor DarkGray
}

# ============================================================
# ETAPA 3 - Criar Registros DNS
# ============================================================
Write-Host "`n[3/4] Criando registros DNS..." -ForegroundColor Yellow

# Registro A para o site principal (raiz da zona)
$existingA = Get-DnsServerResourceRecord -ZoneName $SiteZone -Name "@" -RRType A -ErrorAction SilentlyContinue
if (-not $existingA) {
    Add-DnsServerResourceRecordA -Name "@" -ZoneName $SiteZone -IPv4Address $ServerIP
    Write-Host "  -> Registro A criado: $SiteZone -> $ServerIP" -ForegroundColor Green
} else {
    Write-Host "  -> Registro A ja existe para $SiteZone" -ForegroundColor DarkGray
}

# Registro A para 'www'
$existingWWW = Get-DnsServerResourceRecord -ZoneName $SiteZone -Name "www" -RRType A -ErrorAction SilentlyContinue
if (-not $existingWWW) {
    Add-DnsServerResourceRecordA -Name "www" -ZoneName $SiteZone -IPv4Address $ServerIP
    Write-Host "  -> Registro A criado: www.$SiteZone -> $ServerIP" -ForegroundColor Green
} else {
    Write-Host "  -> Registro A ja existe para www.$SiteZone" -ForegroundColor DarkGray
}

# Registro A para 'api' (NEXUS API)
$existingAPI = Get-DnsServerResourceRecord -ZoneName $SiteZone -Name "api" -RRType A -ErrorAction SilentlyContinue
if (-not $existingAPI) {
    Add-DnsServerResourceRecordA -Name "api" -ZoneName $SiteZone -IPv4Address $ServerIP
    Write-Host "  -> Registro A criado: api.$SiteZone -> $ServerIP" -ForegroundColor Green
} else {
    Write-Host "  -> Registro A ja existe para api.$SiteZone" -ForegroundColor DarkGray
}

# ============================================================
# ETAPA 4 - Configurar DNS do cliente para apontar ao servidor
# ============================================================
Write-Host "`n[4/4] Configurando DNS do servidor local..." -ForegroundColor Yellow

$adapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1
if ($adapter) {
    Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ServerAddresses $ServerIP
    Write-Host "  -> DNS do adaptador '$($adapter.Name)' configurado para $ServerIP" -ForegroundColor Green
}

# Resumo
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Resumo DNS:"
Write-Host "  Zona Direta:      $SiteZone"
Write-Host "  $SiteZone      -> $ServerIP (A)"
Write-Host "  www.$SiteZone  -> $ServerIP (A)"
Write-Host "  api.$SiteZone  -> $ServerIP (A)"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n  Para testar a resolucao:" -ForegroundColor Magenta
Write-Host "  nslookup $SiteZone" -ForegroundColor White
Write-Host "  nslookup www.$SiteZone" -ForegroundColor White
Write-Host "`nSetup DNS concluido com sucesso!" -ForegroundColor Green

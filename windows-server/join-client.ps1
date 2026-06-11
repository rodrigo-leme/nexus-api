<#
.SYNOPSIS
    Script para ingressar maquina cliente no dominio Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Executar este script na MAQUINA CLIENTE (Windows 10/11).
    Ele configura o DNS e ingressa no dominio spacecode.local.

.NOTES
    Executar como Administrador na maquina cliente.
    Necessita credenciais de administrador do dominio.
#>

param(
    [string]$DomainName = "spacecode.local",
    [string]$ServerIP = "CONFIGURE_O_IP_DO_SERVIDOR"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " SPACE CODE LTDA - Ingressar Cliente"        -ForegroundColor Cyan
Write-Host " Dominio: $DomainName"                        -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Validar IP
if ($ServerIP -eq "CONFIGURE_O_IP_DO_SERVIDOR") {
    $ServerIP = Read-Host "Informe o IP do Domain Controller"
}

# ============================================================
# ETAPA 1 - Configurar DNS do cliente
# ============================================================
Write-Host "`n[1/3] Configurando DNS do cliente..." -ForegroundColor Yellow

$adapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1
if ($adapter) {
    Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ServerAddresses $ServerIP
    Write-Host "  -> DNS configurado para $ServerIP no adaptador '$($adapter.Name)'" -ForegroundColor Green
} else {
    Write-Host "  -> [ERRO] Nenhum adaptador de rede ativo encontrado!" -ForegroundColor Red
    exit 1
}

# ============================================================
# ETAPA 2 - Testar conectividade
# ============================================================
Write-Host "`n[2/3] Testando conectividade com o DC..." -ForegroundColor Yellow

$ping = Test-Connection -ComputerName $ServerIP -Count 2 -Quiet
if ($ping) {
    Write-Host "  -> Conectividade OK com $ServerIP" -ForegroundColor Green
} else {
    Write-Host "  -> [ERRO] Nao foi possivel conectar ao DC ($ServerIP)" -ForegroundColor Red
    Write-Host "     Verifique a rede e tente novamente." -ForegroundColor Yellow
    exit 1
}

# Testar resolucao DNS
$nslookup = Resolve-DnsName -Name $DomainName -ErrorAction SilentlyContinue
if ($nslookup) {
    Write-Host "  -> Resolucao DNS OK: $DomainName" -ForegroundColor Green
} else {
    Write-Host "  -> [AVISO] Resolucao DNS falhou para $DomainName" -ForegroundColor Yellow
    Write-Host "     Continuando mesmo assim..." -ForegroundColor Yellow
}

# ============================================================
# ETAPA 3 - Ingressar no Dominio
# ============================================================
Write-Host "`n[3/3] Ingressando no dominio $DomainName..." -ForegroundColor Yellow
Write-Host "  Serao solicitadas as credenciais do administrador do dominio." -ForegroundColor Magenta

$credential = Get-Credential -Message "Credenciais de administrador do dominio $DomainName"
Add-Computer -DomainName $DomainName -Credential $credential -Force -Restart

Write-Host "`n  A maquina sera reiniciada automaticamente." -ForegroundColor Red
Write-Host "  Apos o reboot, faca login com: $DomainName\rodrigo.leme" -ForegroundColor Magenta
Write-Host "  Senha inicial: SpaceCode@2026 (sera necessario alterar)" -ForegroundColor Magenta

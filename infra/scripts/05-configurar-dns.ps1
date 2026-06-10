# =====================================================================
# Space Code LTDA - Global Solutions
# 05 - Configuracao da zona direta de DNS para o site do IIS
#   Zona: spacecode.internal
#   Registros: spacecode.internal (A) e www.spacecode.internal (A)
# =====================================================================

$ZoneName = "spacecode.internal"
$ServerIP = (Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.InterfaceAlias -notmatch "Loopback" -and $_.IPAddress -notmatch "^169\." } |
    Select-Object -First 1 -ExpandProperty IPAddress)

Write-Host "IP do servidor: $ServerIP" -ForegroundColor Cyan

# Zona direta (primaria)
if (-not (Get-DnsServerZone -Name $ZoneName -ErrorAction SilentlyContinue)) {
    Add-DnsServerPrimaryZone -Name $ZoneName -ReplicationScope "Forest" -ErrorAction SilentlyContinue
    if (-not (Get-DnsServerZone -Name $ZoneName -ErrorAction SilentlyContinue)) {
        # Fallback para servidor DNS sem AD (zona em arquivo)
        Add-DnsServerPrimaryZone -Name $ZoneName -ZoneFile "$ZoneName.dns"
    }
    Write-Host "Zona direta criada: $ZoneName" -ForegroundColor Green
}

# Registro A para a raiz da zona e para www
foreach ($RecordName in "@", "www") {
    $Existing = Get-DnsServerResourceRecord -ZoneName $ZoneName -Name $RecordName -RRType A -ErrorAction SilentlyContinue
    if (-not $Existing) {
        Add-DnsServerResourceRecordA -ZoneName $ZoneName -Name $RecordName -IPv4Address $ServerIP
        Write-Host "Registro A criado: $RecordName.$ZoneName -> $ServerIP" -ForegroundColor Green
    }
}

# Garantir que o proprio servidor usa o DNS local
Get-NetAdapter | Where-Object Status -eq "Up" | ForEach-Object {
    Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses ("127.0.0.1")
}

Write-Host "`nTeste de resolucao:" -ForegroundColor Cyan
Resolve-DnsName $ZoneName -Server 127.0.0.1 | Format-Table -AutoSize
Resolve-DnsName "www.$ZoneName" -Server 127.0.0.1 | Format-Table -AutoSize

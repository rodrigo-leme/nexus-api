# =====================================================================
# Space Code LTDA - Global Solutions
# 04 - Criacao das GPOs e vinculo as OUs
#   GPO_Back / GPO_Front : Bloquear Painel de Controle, USB e Regedit
#   GPO_PM               : + Bloquear CMD e Gerenciador de Tarefas
#   GPO_Wallpaper        : Wallpaper unico para todos (vinculada ao dominio)
# =====================================================================

Import-Module GroupPolicy
Import-Module ActiveDirectory

$DomainDN  = (Get-ADDomain).DistinguishedName
$DnsRoot   = (Get-ADDomain).DNSRoot

# ---------- Wallpaper compartilhado via NETLOGON ----------
$WallpaperSrc   = Join-Path $PSScriptRoot "..\site\img\wallpaper-spacecode.jpg"
$NetlogonDir    = "\\$DnsRoot\NETLOGON\wallpaper"
$WallpaperDest  = "$NetlogonDir\wallpaper-spacecode.jpg"
New-Item -ItemType Directory -Path $NetlogonDir -Force | Out-Null
Copy-Item $WallpaperSrc $WallpaperDest -Force

# ---------- Funcao auxiliar: restricoes comuns ----------
function Set-RestricoesComuns([string]$GpoName) {
    # Bloquear Painel de Controle
    Set-GPRegistryValue -Name $GpoName -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
        -ValueName "NoControlPanel" -Type DWord -Value 1 | Out-Null
    # Bloquear Regedit
    Set-GPRegistryValue -Name $GpoName -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
        -ValueName "DisableRegistryTools" -Type DWord -Value 1 | Out-Null
    # Bloquear USB (negar todo acesso a armazenamento removivel)
    Set-GPRegistryValue -Name $GpoName -Key "HKCU\Software\Policies\Microsoft\Windows\RemovableStorageDevices" `
        -ValueName "Deny_All" -Type DWord -Value 1 | Out-Null
}

# ---------- GPO_Back ----------
$Gpo = Get-GPO -Name "GPO_Back" -ErrorAction SilentlyContinue
if (-not $Gpo) { $Gpo = New-GPO -Name "GPO_Back" -Comment "Restricoes do grupo Back" }
Set-RestricoesComuns "GPO_Back"
New-GPLink -Name "GPO_Back" -Target "OU=Back,$DomainDN" -LinkEnabled Yes -ErrorAction SilentlyContinue
Write-Host "GPO_Back criada e vinculada a OU=Back" -ForegroundColor Green

# ---------- GPO_Front ----------
$Gpo = Get-GPO -Name "GPO_Front" -ErrorAction SilentlyContinue
if (-not $Gpo) { $Gpo = New-GPO -Name "GPO_Front" -Comment "Restricoes do grupo Front" }
Set-RestricoesComuns "GPO_Front"
New-GPLink -Name "GPO_Front" -Target "OU=Front,$DomainDN" -LinkEnabled Yes -ErrorAction SilentlyContinue
Write-Host "GPO_Front criada e vinculada a OU=Front" -ForegroundColor Green

# ---------- GPO_PM (restricoes comuns + CMD + Gerenciador de Tarefas) ----------
$Gpo = Get-GPO -Name "GPO_PM" -ErrorAction SilentlyContinue
if (-not $Gpo) { $Gpo = New-GPO -Name "GPO_PM" -Comment "Restricoes do grupo PM" }
Set-RestricoesComuns "GPO_PM"
Set-GPRegistryValue -Name "GPO_PM" -Key "HKCU\Software\Policies\Microsoft\Windows\System" `
    -ValueName "DisableCMD" -Type DWord -Value 1 | Out-Null
Set-GPRegistryValue -Name "GPO_PM" -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "DisableTaskMgr" -Type DWord -Value 1 | Out-Null
New-GPLink -Name "GPO_PM" -Target "OU=PM,$DomainDN" -LinkEnabled Yes -ErrorAction SilentlyContinue
Write-Host "GPO_PM criada e vinculada a OU=PM" -ForegroundColor Green

# ---------- GPO_Wallpaper (todos os usuarios - vinculo no dominio) ----------
$Gpo = Get-GPO -Name "GPO_Wallpaper" -ErrorAction SilentlyContinue
if (-not $Gpo) { $Gpo = New-GPO -Name "GPO_Wallpaper" -Comment "Wallpaper corporativo Space Code" }
Set-GPRegistryValue -Name "GPO_Wallpaper" -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "Wallpaper" -Type String -Value $WallpaperDest | Out-Null
Set-GPRegistryValue -Name "GPO_Wallpaper" -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "WallpaperStyle" -Type String -Value "2" | Out-Null   # 2 = Esticar
New-GPLink -Name "GPO_Wallpaper" -Target $DomainDN -LinkEnabled Yes -ErrorAction SilentlyContinue
Write-Host "GPO_Wallpaper criada e vinculada ao dominio" -ForegroundColor Green

gpupdate /force
Write-Host "`nGPOs aplicadas. Resumo:" -ForegroundColor Cyan
Get-GPO -All | Format-Table DisplayName, CreationTime -AutoSize

<#
.SYNOPSIS
    Script de configuracao de Group Policy Objects (GPO) para Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Este script cria e vincula GPOs as OUs:
    - Back:  Bloquear Painel de Controle, USB, Regedit
    - Front: Bloquear Painel de Controle, USB, Regedit
    - PM:    Bloquear Painel de Controle, USB, Regedit, CMD, Gerenciador de Tarefas
    - Todos: Wallpaper padrao NEXUS/Space Code

.NOTES
    Executar APOS o setup-ad.ps1 e reboot.
    Executar como Administrador no Domain Controller.
#>

param(
    [string]$DomainName = "spacecode.local",
    [string]$WallpaperSource = "$PSScriptRoot\..\website\assets\wallpaper-spacecode.png"
)

Import-Module GroupPolicy
Import-Module ActiveDirectory

$baseDN = "DC=" + ($DomainName -replace "\.", ",DC=")

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " SPACE CODE LTDA - Setup GPOs"               -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ============================================================
# FUNCOES AUXILIARES
# ============================================================

function Set-RegistryPolicy {
    param(
        [string]$GPOName,
        [string]$Key,
        [string]$ValueName,
        [string]$Type,
        $Value
    )
    Set-GPRegistryValue -Name $GPOName -Key $Key -ValueName $ValueName -Type $Type -Value $Value | Out-Null
}

# ============================================================
# ETAPA 1 - Copiar Wallpaper para pasta compartilhada
# ============================================================
Write-Host "`n[1/5] Configurando wallpaper corporativo..." -ForegroundColor Yellow

$wallpaperShare = "C:\NEXUS-Wallpaper"
if (-not (Test-Path $wallpaperShare)) {
    New-Item -ItemType Directory -Path $wallpaperShare -Force | Out-Null
}

if (Test-Path $WallpaperSource) {
    Copy-Item -Path $WallpaperSource -Destination "$wallpaperShare\wallpaper.png" -Force
    Write-Host "  -> Wallpaper copiado para $wallpaperShare" -ForegroundColor Green
} else {
    Write-Host "  -> [AVISO] Wallpaper nao encontrado em: $WallpaperSource" -ForegroundColor Yellow
    Write-Host "     Coloque manualmente o arquivo em $wallpaperShare\wallpaper.png" -ForegroundColor Yellow
}

# Compartilhar a pasta
$shareName = "NEXUS-Wallpaper$"
if (-not (Get-SmbShare -Name $shareName -ErrorAction SilentlyContinue)) {
    New-SmbShare -Name $shareName -Path $wallpaperShare -ReadAccess "Everyone" | Out-Null
    Write-Host "  -> Compartilhamento criado: \\$env:COMPUTERNAME\$shareName" -ForegroundColor Green
}

$wallpaperPath = "\\$env:COMPUTERNAME\$shareName\wallpaper.png"

# ============================================================
# ETAPA 2 - GPO para grupo BACK (Bloquear: Painel, USB, Regedit)
# ============================================================
Write-Host "`n[2/5] Criando GPO: GPO_Back..." -ForegroundColor Yellow

$gpoBack = "GPO_Back"
if (-not (Get-GPO -Name $gpoBack -ErrorAction SilentlyContinue)) {
    New-GPO -Name $gpoBack | Out-Null
}

# Bloquear Painel de Controle
Set-RegistryPolicy -GPOName $gpoBack `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
    -ValueName "NoControlPanel" -Type DWord -Value 1

# Bloquear USB (acesso a dispositivos de armazenamento removivel)
Set-RegistryPolicy -GPOName $gpoBack `
    -Key "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" `
    -ValueName "Start" -Type DWord -Value 4

# Bloquear Regedit
Set-RegistryPolicy -GPOName $gpoBack `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "DisableRegistryTools" -Type DWord -Value 2

# Wallpaper
Set-RegistryPolicy -GPOName $gpoBack `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "Wallpaper" -Type String -Value $wallpaperPath
Set-RegistryPolicy -GPOName $gpoBack `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "WallpaperStyle" -Type String -Value "2"

# Vincular GPO a OU Back
New-GPLink -Name $gpoBack -Target "OU=Back,$baseDN" -LinkEnabled Yes -ErrorAction SilentlyContinue | Out-Null
Write-Host "  -> GPO_Back criada e vinculada: Painel, USB, Regedit bloqueados" -ForegroundColor Green

# ============================================================
# ETAPA 3 - GPO para grupo FRONT (Bloquear: Painel, USB, Regedit)
# ============================================================
Write-Host "`n[3/5] Criando GPO: GPO_Front..." -ForegroundColor Yellow

$gpoFront = "GPO_Front"
if (-not (Get-GPO -Name $gpoFront -ErrorAction SilentlyContinue)) {
    New-GPO -Name $gpoFront | Out-Null
}

# Bloquear Painel de Controle
Set-RegistryPolicy -GPOName $gpoFront `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
    -ValueName "NoControlPanel" -Type DWord -Value 1

# Bloquear USB
Set-RegistryPolicy -GPOName $gpoFront `
    -Key "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" `
    -ValueName "Start" -Type DWord -Value 4

# Bloquear Regedit
Set-RegistryPolicy -GPOName $gpoFront `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "DisableRegistryTools" -Type DWord -Value 2

# Wallpaper
Set-RegistryPolicy -GPOName $gpoFront `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "Wallpaper" -Type String -Value $wallpaperPath
Set-RegistryPolicy -GPOName $gpoFront `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "WallpaperStyle" -Type String -Value "2"

New-GPLink -Name $gpoFront -Target "OU=Front,$baseDN" -LinkEnabled Yes -ErrorAction SilentlyContinue | Out-Null
Write-Host "  -> GPO_Front criada e vinculada: Painel, USB, Regedit bloqueados" -ForegroundColor Green

# ============================================================
# ETAPA 4 - GPO para grupo PM (Bloquear: Painel, USB, Regedit, CMD, Gerenciador de Tarefas)
# ============================================================
Write-Host "`n[4/5] Criando GPO: GPO_PM..." -ForegroundColor Yellow

$gpoPM = "GPO_PM"
if (-not (Get-GPO -Name $gpoPM -ErrorAction SilentlyContinue)) {
    New-GPO -Name $gpoPM | Out-Null
}

# Bloquear Painel de Controle
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
    -ValueName "NoControlPanel" -Type DWord -Value 1

# Bloquear USB
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" `
    -ValueName "Start" -Type DWord -Value 4

# Bloquear Regedit
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "DisableRegistryTools" -Type DWord -Value 2

# Bloquear CMD (Prompt de Comando)
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Policies\Microsoft\Windows\System" `
    -ValueName "DisableCMD" -Type DWord -Value 2

# Bloquear Gerenciador de Tarefas
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "DisableTaskMgr" -Type DWord -Value 1

# Wallpaper
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "Wallpaper" -Type String -Value $wallpaperPath
Set-RegistryPolicy -GPOName $gpoPM `
    -Key "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" `
    -ValueName "WallpaperStyle" -Type String -Value "2"

New-GPLink -Name $gpoPM -Target "OU=PM,$baseDN" -LinkEnabled Yes -ErrorAction SilentlyContinue | Out-Null
Write-Host "  -> GPO_PM criada e vinculada: Painel, USB, Regedit, CMD, Task Manager bloqueados" -ForegroundColor Green

# ============================================================
# ETAPA 5 - Resumo
# ============================================================
Write-Host "`n[5/5] Resumo das GPOs:" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  GPO_Back  -> OU=Back:  Painel, USB, Regedit"
Write-Host "  GPO_Front -> OU=Front: Painel, USB, Regedit"
Write-Host "  GPO_PM    -> OU=PM:    Painel, USB, Regedit, CMD, Task Manager"
Write-Host "  Wallpaper -> Todos: $wallpaperPath"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n  Para forcar aplicacao imediata no cliente:" -ForegroundColor Magenta
Write-Host "  gpupdate /force" -ForegroundColor White
Write-Host "`nSetup GPO concluido com sucesso!" -ForegroundColor Green

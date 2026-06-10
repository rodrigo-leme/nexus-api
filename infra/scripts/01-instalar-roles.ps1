# =====================================================================
# Space Code LTDA - Global Solutions
# 01 - Instalacao das roles: AD DS, DNS e IIS (com ASP classico)
# Executar como Administrador em Windows Server 2019+
# =====================================================================

Write-Host "Instalando roles AD DS, DNS e IIS..." -ForegroundColor Cyan

Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
Install-WindowsFeature -Name DNS -IncludeManagementTools
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
Install-WindowsFeature -Name Web-ASP            # ASP classico (form -> JSON)
Install-WindowsFeature -Name GPMC               # Console de Gerenciamento de GPO

Write-Host "Roles instaladas com sucesso." -ForegroundColor Green
Get-WindowsFeature AD-Domain-Services, DNS, Web-Server, Web-ASP, GPMC |
    Format-Table DisplayName, InstallState -AutoSize

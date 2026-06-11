<#
.SYNOPSIS
    Script mestre - executa toda a infraestrutura Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Ordem de execucao:
    1. setup-ad.ps1   -> Active Directory (usuarios, grupos, OUs)
    2. [REBOOT]       -> Necessario apos promocao a DC
    3. setup-gpo.ps1  -> Group Policy Objects
    4. setup-dns.ps1  -> DNS (zona direta do site)
    5. setup-iis.ps1  -> IIS (site institucional)
    6. join-client.ps1 -> Executar na maquina CLIENTE

.NOTES
    Executar como Administrador no Windows Server 2022.
    A ordem dos scripts eh importante!
#>

Write-Host @"

 =============================================
     SPACE CODE LTDA - Infrastructure Setup
            Global Solution 2026
 =============================================

  Este script executa a configuracao completa:

  SERVIDOR (este script):
    1. Active Directory (AD DS)
    2. Group Policy Objects (GPO)
    3. DNS Server
    4. IIS Web Server

  CLIENTE (executar separadamente):
    5. Ingressar no dominio (join-client.ps1)

 =============================================

"@ -ForegroundColor Cyan

$step = Read-Host "Qual etapa executar? (1=AD, 2=GPO, 3=DNS, 4=IIS, 5=TODOS apos reboot)"

switch ($step) {
    "1" {
        Write-Host "`nExecutando: Active Directory..." -ForegroundColor Yellow
        & "$PSScriptRoot\setup-ad.ps1"
        Write-Host "`n[IMPORTANTE] Reinicie o servidor e execute novamente com opcao 5." -ForegroundColor Red
    }
    "2" {
        Write-Host "`nExecutando: Group Policy Objects..." -ForegroundColor Yellow
        & "$PSScriptRoot\setup-gpo.ps1"
    }
    "3" {
        Write-Host "`nExecutando: DNS..." -ForegroundColor Yellow
        & "$PSScriptRoot\setup-dns.ps1"
    }
    "4" {
        Write-Host "`nExecutando: IIS..." -ForegroundColor Yellow
        & "$PSScriptRoot\setup-iis.ps1"
    }
    "5" {
        Write-Host "`nExecutando todas as etapas (pos-reboot)..." -ForegroundColor Yellow
        Write-Host "`n--- GPO ---" -ForegroundColor Cyan
        & "$PSScriptRoot\setup-gpo.ps1"
        Write-Host "`n--- DNS ---" -ForegroundColor Cyan
        & "$PSScriptRoot\setup-dns.ps1"
        Write-Host "`n--- IIS ---" -ForegroundColor Cyan
        & "$PSScriptRoot\setup-iis.ps1"
        Write-Host "`n=== INFRAESTRUTURA COMPLETA ===" -ForegroundColor Green
    }
    default {
        Write-Host "Opcao invalida." -ForegroundColor Red
    }
}

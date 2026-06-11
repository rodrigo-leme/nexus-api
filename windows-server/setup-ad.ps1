<#
.SYNOPSIS
    Script de configuracao do Active Directory para Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Este script:
    1. Instala o role AD DS e promove o servidor a Domain Controller
    2. Cria a estrutura de OUs e Sub-OUs (Back, Front, PM)
    3. Cria 10 usuarios e distribui nos grupos corretos
    4. Configura politica de senha para primeiro login

.NOTES
    Dominio: spacecode.local
    Executar como Administrador no Windows Server 2022
#>

param(
    [string]$DomainName = "spacecode.local",
    [string]$NetBIOSName = "SPACECODE",
    [string]$SafeModePassword = "S@feM0de2026!"
)

# ============================================================
# ETAPA 1 - Instalar e Promover Domain Controller
# ============================================================
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " SPACE CODE LTDA - Setup Active Directory"    -ForegroundColor Cyan
Write-Host " Dominio: $DomainName"                        -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Instala o role AD DS
Write-Host "`n[1/5] Instalando role Active Directory Domain Services..." -ForegroundColor Yellow
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools -ErrorAction Stop
Write-Host "  -> AD DS instalado com sucesso." -ForegroundColor Green

# Promove a Domain Controller (se ainda nao for)
$isDC = (Get-WmiObject Win32_ComputerSystem).DomainRole
if ($isDC -lt 4) {
    Write-Host "`n[INFO] Promovendo servidor a Domain Controller..." -ForegroundColor Yellow
    $securePassword = ConvertTo-SecureString $SafeModePassword -AsPlainText -Force
    Install-ADDSForest `
        -DomainName $DomainName `
        -DomainNetBIOSName $NetBIOSName `
        -SafeModeAdministratorPassword $securePassword `
        -InstallDns:$true `
        -Force:$true `
        -NoRebootOnCompletion:$false
    Write-Host "  -> Servidor sera reiniciado. Execute este script novamente apos o reboot." -ForegroundColor Red
    exit 0
}

Import-Module ActiveDirectory

# ============================================================
# ETAPA 2 - Criar Estrutura de OUs
# ============================================================
Write-Host "`n[2/5] Criando estrutura de Organizational Units..." -ForegroundColor Yellow

$baseDN = "DC=" + ($DomainName -replace "\.", ",DC=")

# OUs principais
$ousMain = @("Back", "Front", "PM")
foreach ($ou in $ousMain) {
    $ouPath = "OU=$ou,$baseDN"
    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$ou'" -SearchBase $baseDN -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $ou -Path $baseDN -ProtectedFromAccidentalDeletion $false
        Write-Host "  -> OU criada: $ou" -ForegroundColor Green
    } else {
        Write-Host "  -> OU ja existe: $ou" -ForegroundColor DarkGray
    }
}

# Sub-OUs
$subOUs = @{
    "Back"  = "Back_Devs"
    "Front" = "Front_Devs"
    "PM"    = "PM_Users"
}

foreach ($parent in $subOUs.Keys) {
    $subName = $subOUs[$parent]
    $parentDN = "OU=$parent,$baseDN"
    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$subName'" -SearchBase $parentDN -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $subName -Path $parentDN -ProtectedFromAccidentalDeletion $false
        Write-Host "  -> Sub-OU criada: $subName (dentro de $parent)" -ForegroundColor Green
    } else {
        Write-Host "  -> Sub-OU ja existe: $subName" -ForegroundColor DarkGray
    }
}

# ============================================================
# ETAPA 3 - Criar Grupos de Seguranca
# ============================================================
Write-Host "`n[3/5] Criando grupos de seguranca..." -ForegroundColor Yellow

$grupos = @(
    @{ Name = "GRP_Back";  OU = "OU=Back_Devs,OU=Back,$baseDN" },
    @{ Name = "GRP_Front"; OU = "OU=Front_Devs,OU=Front,$baseDN" },
    @{ Name = "GRP_PM";    OU = "OU=PM_Users,OU=PM,$baseDN" }
)

foreach ($grp in $grupos) {
    if (-not (Get-ADGroup -Filter "Name -eq '$($grp.Name)'" -ErrorAction SilentlyContinue)) {
        New-ADGroup -Name $grp.Name -GroupScope Global -GroupCategory Security -Path $grp.OU
        Write-Host "  -> Grupo criado: $($grp.Name)" -ForegroundColor Green
    } else {
        Write-Host "  -> Grupo ja existe: $($grp.Name)" -ForegroundColor DarkGray
    }
}

# ============================================================
# ETAPA 4 - Criar 10 Usuarios
# ============================================================
Write-Host "`n[4/5] Criando usuarios (10 funcionarios)..." -ForegroundColor Yellow

$defaultPassword = ConvertTo-SecureString "SpaceCode@2026" -AsPlainText -Force

# 5 Back-end devs
$usersBack = @(
    @{ First = "Rodrigo";  Last = "Leme";     Login = "rodrigo.leme";    ChangeAtLogon = $true  },
    @{ First = "Cezar";    Last = "Santos";    Login = "cezar.santos";    ChangeAtLogon = $false },
    @{ First = "Fabrini";  Last = "Oliveira";  Login = "fabrini.oliveira";ChangeAtLogon = $false },
    @{ First = "Lucas";    Last = "Mendes";    Login = "lucas.mendes";    ChangeAtLogon = $false },
    @{ First = "Ana";      Last = "Costa";     Login = "ana.costa";       ChangeAtLogon = $false }
)

# 3 Front-end devs
$usersFront = @(
    @{ First = "Maria";    Last = "Silva";     Login = "maria.silva";     ChangeAtLogon = $false },
    @{ First = "Pedro";    Last = "Almeida";   Login = "pedro.almeida";   ChangeAtLogon = $false },
    @{ First = "Julia";    Last = "Ferreira";  Login = "julia.ferreira";  ChangeAtLogon = $false }
)

# 2 PMs
$usersPM = @(
    @{ First = "Carlos";   Last = "Ribeiro";   Login = "carlos.ribeiro";  ChangeAtLogon = $false },
    @{ First = "Beatriz";  Last = "Martins";   Login = "beatriz.martins"; ChangeAtLogon = $false }
)

function Create-SCUser {
    param($User, $Group, $OUPath)
    $upn = "$($User.Login)@$DomainName"
    if (-not (Get-ADUser -Filter "SamAccountName -eq '$($User.Login)'" -ErrorAction SilentlyContinue)) {
        New-ADUser `
            -Name "$($User.First) $($User.Last)" `
            -GivenName $User.First `
            -Surname $User.Last `
            -SamAccountName $User.Login `
            -UserPrincipalName $upn `
            -Path $OUPath `
            -AccountPassword $defaultPassword `
            -Enabled $true `
            -ChangePasswordAtLogon $User.ChangeAtLogon `
            -Description "Funcionario Space Code LTDA"

        Add-ADGroupMember -Identity $Group -Members $User.Login
        
        $changeFlag = if ($User.ChangeAtLogon) { " [ALTERAR SENHA NO 1o LOGIN]" } else { "" }
        Write-Host "  -> Usuario criado: $($User.First) $($User.Last) ($($User.Login))$changeFlag" -ForegroundColor Green
    } else {
        Write-Host "  -> Usuario ja existe: $($User.Login)" -ForegroundColor DarkGray
    }
}

$backOU  = "OU=Back_Devs,OU=Back,$baseDN"
$frontOU = "OU=Front_Devs,OU=Front,$baseDN"
$pmOU    = "OU=PM_Users,OU=PM,$baseDN"

foreach ($u in $usersBack)  { Create-SCUser -User $u -Group "GRP_Back"  -OUPath $backOU }
foreach ($u in $usersFront) { Create-SCUser -User $u -Group "GRP_Front" -OUPath $frontOU }
foreach ($u in $usersPM)    { Create-SCUser -User $u -Group "GRP_PM"    -OUPath $pmOU }

# ============================================================
# ETAPA 5 - Resumo
# ============================================================
Write-Host "`n[5/5] Resumo da configuracao:" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Dominio:     $DomainName"
Write-Host "  OUs:         Back, Front, PM"
Write-Host "  Sub-OUs:     Back_Devs, Front_Devs, PM_Users"
Write-Host "  Grupos:      GRP_Back (5), GRP_Front (3), GRP_PM (2)"
Write-Host "  Usuarios:    10 (total)"
Write-Host "  Alterar Senha: rodrigo.leme (primeiro login)"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n  NOTA: O usuario 'rodrigo.leme' foi configurado para" -ForegroundColor Magenta
Write-Host "  alterar a senha no primeiro login. Use este usuario" -ForegroundColor Magenta
Write-Host "  para demonstrar as politicas no video/apresentacao." -ForegroundColor Magenta
Write-Host "`nSetup AD concluido com sucesso!" -ForegroundColor Green

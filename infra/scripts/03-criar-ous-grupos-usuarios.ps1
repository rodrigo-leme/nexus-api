# =====================================================================
# Space Code LTDA - Global Solutions
# 03 - Criacao de OUs, Sub-OUs, Grupos e 10 usuarios
#   OUs:     Back, Front, PM
#   Sub-OUs: Back_Devs, Front_Devs, PM_Users
#   Grupos:  Back (5), Front (3), PM (2)
#   Usuario "ana.souza" deve trocar a senha no primeiro login
# =====================================================================

Import-Module ActiveDirectory

$DomainDN  = (Get-ADDomain).DistinguishedName
$UpnSuffix = (Get-ADDomain).DNSRoot
$Senha     = ConvertTo-SecureString "SpaceCode@2026!" -AsPlainText -Force

# ---------- 1. OUs principais e Sub-OUs ----------
$Estrutura = @{
    "Back"  = "Back_Devs"
    "Front" = "Front_Devs"
    "PM"    = "PM_Users"
}

foreach ($OU in $Estrutura.Keys) {
    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$OU'" -SearchBase $DomainDN -SearchScope OneLevel -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $OU -Path $DomainDN -ProtectedFromAccidentalDeletion $false
        Write-Host "OU criada: $OU" -ForegroundColor Green
    }
    $SubOU  = $Estrutura[$OU]
    $OUPath = "OU=$OU,$DomainDN"
    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$SubOU'" -SearchBase $OUPath -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $SubOU -Path $OUPath -ProtectedFromAccidentalDeletion $false
        Write-Host "Sub-OU criada: $SubOU (dentro de $OU)" -ForegroundColor Green
    }
}

# ---------- 2. Grupos de seguranca ----------
$Grupos = @(
    @{ Nome = "Back";  Path = "OU=Back_Devs,OU=Back,$DomainDN" },
    @{ Nome = "Front"; Path = "OU=Front_Devs,OU=Front,$DomainDN" },
    @{ Nome = "PM";    Path = "OU=PM_Users,OU=PM,$DomainDN" }
)
foreach ($G in $Grupos) {
    if (-not (Get-ADGroup -Filter "Name -eq '$($G.Nome)'" -ErrorAction SilentlyContinue)) {
        New-ADGroup -Name $G.Nome -GroupScope Global -GroupCategory Security -Path $G.Path
        Write-Host "Grupo criado: $($G.Nome)" -ForegroundColor Green
    }
}

# ---------- 3. 10 funcionarios ----------
# Back: 5 | Front: 3 | PM: 2
$Funcionarios = @(
    @{ Nome = "Ana";      Sobrenome = "Souza";    Login = "ana.souza";      Grupo = "Back";  TrocarSenha = $true  },
    @{ Nome = "Bruno";    Sobrenome = "Lima";     Login = "bruno.lima";     Grupo = "Back";  TrocarSenha = $false },
    @{ Nome = "Carlos";   Sobrenome = "Pereira";  Login = "carlos.pereira"; Grupo = "Back";  TrocarSenha = $false },
    @{ Nome = "Daniela";  Sobrenome = "Rocha";    Login = "daniela.rocha";  Grupo = "Back";  TrocarSenha = $false },
    @{ Nome = "Eduardo";  Sobrenome = "Martins";  Login = "eduardo.martins";Grupo = "Back";  TrocarSenha = $false },
    @{ Nome = "Fernanda"; Sobrenome = "Alves";    Login = "fernanda.alves"; Grupo = "Front"; TrocarSenha = $false },
    @{ Nome = "Gabriel";  Sobrenome = "Costa";    Login = "gabriel.costa";  Grupo = "Front"; TrocarSenha = $false },
    @{ Nome = "Helena";   Sobrenome = "Dias";     Login = "helena.dias";    Grupo = "Front"; TrocarSenha = $false },
    @{ Nome = "Igor";     Sobrenome = "Nunes";    Login = "igor.nunes";     Grupo = "PM";    TrocarSenha = $false },
    @{ Nome = "Julia";    Sobrenome = "Ferreira"; Login = "julia.ferreira"; Grupo = "PM";    TrocarSenha = $false }
)

$PathPorGrupo = @{
    "Back"  = "OU=Back_Devs,OU=Back,$DomainDN"
    "Front" = "OU=Front_Devs,OU=Front,$DomainDN"
    "PM"    = "OU=PM_Users,OU=PM,$DomainDN"
}

foreach ($F in $Funcionarios) {
    if (-not (Get-ADUser -Filter "SamAccountName -eq '$($F.Login)'" -ErrorAction SilentlyContinue)) {
        New-ADUser `
            -Name "$($F.Nome) $($F.Sobrenome)" `
            -GivenName $F.Nome `
            -Surname $F.Sobrenome `
            -SamAccountName $F.Login `
            -UserPrincipalName "$($F.Login)@$UpnSuffix" `
            -AccountPassword $Senha `
            -Path $PathPorGrupo[$F.Grupo] `
            -ChangePasswordAtLogon $F.TrocarSenha `
            -Enabled $true
        Add-ADGroupMember -Identity $F.Grupo -Members $F.Login
        Write-Host "Usuario criado: $($F.Login) -> grupo $($F.Grupo) (Trocar senha: $($F.TrocarSenha))" -ForegroundColor Green
    }
}

Write-Host "`nResumo:" -ForegroundColor Cyan
foreach ($G in "Back", "Front", "PM") {
    $Membros = (Get-ADGroupMember -Identity $G | Measure-Object).Count
    Write-Host "  Grupo $G : $Membros membros"
}

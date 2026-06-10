# =====================================================================
# Space Code LTDA - Global Solutions
# 02 - Promocao do servidor a Controlador de Dominio (nova floresta)
# Dominio: spacecode.local
# ATENCAO: o servidor sera REINICIADO automaticamente ao final.
# =====================================================================

$DomainName  = "spacecode.local"
$NetbiosName = "SPACECODE"

# Senha de modo de restauracao (DSRM) - troque em producao
$SafeModePwd = ConvertTo-SecureString "SpaceCode@2026!" -AsPlainText -Force

Import-Module ADDSDeployment

Install-ADDSForest `
    -DomainName $DomainName `
    -DomainNetbiosName $NetbiosName `
    -SafeModeAdministratorPassword $SafeModePwd `
    -InstallDns:$true `
    -CreateDnsDelegation:$false `
    -DatabasePath "C:\Windows\NTDS" `
    -LogPath "C:\Windows\NTDS" `
    -SysvolPath "C:\Windows\SYSVOL" `
    -NoRebootOnCompletion:$false `
    -Force:$true

# =====================================================================
# Space Code LTDA - Global Solutions
# 06 - Publicacao do site institucional no IIS
#   Site: SpaceCode  |  Host: spacecode.internal / www.spacecode.internal
#   Form de contato grava em C:\inetpub\spacecode\data\contatos.json
# =====================================================================

Import-Module WebAdministration

$SiteName = "SpaceCode"
$SiteRoot = "C:\inetpub\spacecode"
$Source   = Join-Path $PSScriptRoot "..\site"

# ---------- Copiar arquivos do site ----------
New-Item -ItemType Directory -Path $SiteRoot -Force | Out-Null
Copy-Item "$Source\*" $SiteRoot -Recurse -Force

# Pasta de dados para o JSON do formulario (com permissao de escrita para o IIS)
$DataDir = Join-Path $SiteRoot "data"
New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
if (-not (Test-Path "$DataDir\contatos.json")) {
    Set-Content -Path "$DataDir\contatos.json" -Value "[]" -Encoding UTF8
}
$Acl  = Get-Acl $DataDir
$Rule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS", "Modify", "ContainerInherit,ObjectInherit", "None", "Allow")
$Acl.AddAccessRule($Rule)
Set-Acl $DataDir $Acl

# ---------- Criar o site no IIS ----------
if (Get-Website -Name $SiteName -ErrorAction SilentlyContinue) {
    Remove-Website -Name $SiteName
}
New-Website -Name $SiteName -PhysicalPath $SiteRoot -Port 80 -HostHeader "spacecode.internal"
New-WebBinding -Name $SiteName -Protocol http -Port 80 -HostHeader "www.spacecode.internal"

# Habilitar ASP classico e configurar pagina padrao
Set-WebConfigurationProperty -Filter "system.webServer/asp" -PSPath "IIS:\Sites\$SiteName" -Name "enableParentPaths" -Value $true -ErrorAction SilentlyContinue
Add-WebConfigurationProperty -Filter "system.webServer/defaultDocument/files" -PSPath "IIS:\Sites\$SiteName" -Name "." -Value @{value="index.html"} -ErrorAction SilentlyContinue

Start-Website -Name $SiteName
Write-Host "Site '$SiteName' publicado em http://spacecode.internal" -ForegroundColor Green
Get-Website | Format-Table Name, State, PhysicalPath -AutoSize

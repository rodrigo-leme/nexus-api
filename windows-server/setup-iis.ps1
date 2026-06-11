<#
.SYNOPSIS
    Script de configuracao do IIS para Space Code LTDA.
    Projeto Global Solution - Sistemas Operacionais (FIAP 2026)

.DESCRIPTION
    Este script:
    1. Instala o IIS (Web Server) com modulos necessarios
    2. Cria o site institucional no IIS
    3. Configura o binding para o dominio spacecode.internal
    4. Configura pasta de dados para o formulario de contato

.NOTES
    Executar como Administrador no Windows Server.
    Os arquivos do site devem estar em ..\website\
#>

param(
    [string]$SiteName = "SpaceCode",
    [string]$SiteHostName = "spacecode.internal",
    [string]$WebsitePath = "$PSScriptRoot\..\website",
    [int]$Port = 80
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " SPACE CODE LTDA - Setup IIS"                -ForegroundColor Cyan
Write-Host " Site: $SiteName"                             -ForegroundColor Cyan
Write-Host " Host: $SiteHostName"                         -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# ============================================================
# ETAPA 1 - Instalar IIS
# ============================================================
Write-Host "`n[1/5] Instalando IIS e modulos..." -ForegroundColor Yellow

$features = @(
    "Web-Server",
    "Web-Default-Doc",
    "Web-Dir-Browsing",
    "Web-Http-Errors",
    "Web-Static-Content",
    "Web-Http-Logging",
    "Web-Stat-Compression",
    "Web-Filtering",
    "Web-CGI",
    "Web-ISAPI-Ext",
    "Web-ISAPI-Filter",
    "Web-Mgmt-Console",
    "Web-Scripting-Tools"
)

foreach ($feat in $features) {
    $installed = Get-WindowsFeature -Name $feat
    if (-not $installed.Installed) {
        Install-WindowsFeature -Name $feat -ErrorAction SilentlyContinue | Out-Null
    }
}
Write-Host "  -> IIS e modulos instalados com sucesso." -ForegroundColor Green

Import-Module WebAdministration

# ============================================================
# ETAPA 2 - Preparar pasta do site
# ============================================================
Write-Host "`n[2/5] Preparando pasta do site..." -ForegroundColor Yellow

$sitePath = "C:\inetpub\spacecode"
if (-not (Test-Path $sitePath)) {
    New-Item -ItemType Directory -Path $sitePath -Force | Out-Null
}

# Copiar arquivos do website
$sourceWeb = (Resolve-Path $WebsitePath -ErrorAction SilentlyContinue)
if ($sourceWeb) {
    Copy-Item -Path "$sourceWeb\*" -Destination $sitePath -Recurse -Force
    Write-Host "  -> Arquivos copiados de $sourceWeb para $sitePath" -ForegroundColor Green
} else {
    Write-Host "  -> [AVISO] Pasta do website nao encontrada: $WebsitePath" -ForegroundColor Yellow
    Write-Host "     Copie manualmente os arquivos para $sitePath" -ForegroundColor Yellow
}

# Criar pasta de dados para o formulario
$dataPath = "$sitePath\data"
if (-not (Test-Path $dataPath)) {
    New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
}

# Criar arquivo JSON inicial
$jsonPath = "$dataPath\contatos.json"
if (-not (Test-Path $jsonPath)) {
    "[]" | Out-File -FilePath $jsonPath -Encoding UTF8
    Write-Host "  -> Arquivo contatos.json criado em $dataPath" -ForegroundColor Green
}

# Permissoes de escrita para IIS_IUSRS (necessario para o form salvar JSON)
$acl = Get-Acl $dataPath
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS", "Modify", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($rule)
Set-Acl -Path $dataPath -AclObject $acl
Write-Host "  -> Permissoes de escrita concedidas para IIS_IUSRS em $dataPath" -ForegroundColor Green

# ============================================================
# ETAPA 3 - Criar site no IIS
# ============================================================
Write-Host "`n[3/5] Criando site no IIS..." -ForegroundColor Yellow

# Remover site padrao se existir na porta 80
$defaultSite = Get-Website -Name "Default Web Site" -ErrorAction SilentlyContinue
if ($defaultSite) {
    Stop-Website -Name "Default Web Site" -ErrorAction SilentlyContinue
    Write-Host "  -> Default Web Site parado." -ForegroundColor DarkGray
}

# Criar novo site
$existingSite = Get-Website -Name $SiteName -ErrorAction SilentlyContinue
if (-not $existingSite) {
    New-Website -Name $SiteName `
        -PhysicalPath $sitePath `
        -Port $Port `
        -HostHeader $SiteHostName `
        -Force | Out-Null
    Write-Host "  -> Site '$SiteName' criado no IIS." -ForegroundColor Green
} else {
    Write-Host "  -> Site '$SiteName' ja existe." -ForegroundColor DarkGray
}

# Adicionar binding sem host header (acesso direto por IP)
$existingBinding = Get-WebBinding -Name $SiteName -Port $Port -HostHeader "" -ErrorAction SilentlyContinue
if (-not $existingBinding) {
    New-WebBinding -Name $SiteName -Port $Port -HostHeader "" -ErrorAction SilentlyContinue
    Write-Host "  -> Binding adicional criado (acesso por IP direto)." -ForegroundColor Green
}

# ============================================================
# ETAPA 4 - Configurar Default Document
# ============================================================
Write-Host "`n[4/5] Configurando documento padrao..." -ForegroundColor Yellow

# Garantir que index.html eh o documento padrao
Set-WebConfigurationProperty -Filter "system.webServer/defaultDocument/files" `
    -PSPath "IIS:\Sites\$SiteName" `
    -Name "." `
    -Value @{value="index.html"} -ErrorAction SilentlyContinue

Write-Host "  -> Default document configurado: index.html" -ForegroundColor Green

# Iniciar o site
Start-Website -Name $SiteName -ErrorAction SilentlyContinue
Write-Host "  -> Site '$SiteName' iniciado." -ForegroundColor Green

# ============================================================
# ETAPA 5 - Resumo
# ============================================================
Write-Host "`n[5/5] Resumo IIS:" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Site:       $SiteName"
Write-Host "  Pasta:      $sitePath"
Write-Host "  URL:        http://$SiteHostName"
Write-Host "  URL (IP):   http://$((Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike '*Loopback*' } | Select-Object -First 1).IPAddress)"
Write-Host "  Dados Form: $dataPath\contatos.json"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n  Para testar no Microsoft Edge:" -ForegroundColor Magenta
Write-Host "  http://$SiteHostName" -ForegroundColor White
Write-Host "`nSetup IIS concluido com sucesso!" -ForegroundColor Green

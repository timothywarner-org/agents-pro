#requires -Version 7.0
<#
.SYNOPSIS
  Grand unified Windows 11 setup for Copilot Studio / Microsoft 365 development.

.DESCRIPTION
  Run this from an elevated PowerShell 7 session.
  It will:
    - verify elevation and Windows
    - trust PSGallery
    - install/update pwsh 7-friendly modules
    - install/update Power Platform PowerShell modules in Windows PowerShell 5.1
    - install/update Power Platform CLI (pac)
    - verify commands/modules afterward
    - print next-step connect commands

.NOTES
  Why both shells?
    Microsoft.PowerApps.Administration.PowerShell and Microsoft.PowerApps.PowerShell
    still require Windows PowerShell 5.x per Microsoft docs.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ----------------------------
# Utility / logging helpers
# ----------------------------
function Write-Phase {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Write-Info {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Gray
}

function Write-Ok {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "[ OK ] $Message" -ForegroundColor Green
}

function Write-WarnEx {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Fail {
    param([Parameter(Mandatory)][string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Test-IsAdministrator {
    $identity  = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Assert-Environment {
    if (-not $IsWindows) {
        throw "This script is Windows-only."
    }

    if (-not (Test-IsAdministrator)) {
        throw "Run this from an elevated PowerShell 7 session."
    }

    if ($PSVersionTable.PSVersion.Major -lt 7) {
        throw "Run this script in PowerShell 7 or later."
    }

    Write-Ok "Environment checks passed."
}

function Ensure-Tls12 {
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Write-Ok "TLS 1.2 enabled for current session."
    }
    catch {
        Write-WarnEx "Could not explicitly set TLS 1.2. Continuing."
    }
}

function Ensure-PackageManagementPrereqs {
    Write-Phase "Package management prerequisites"

    try {
        $nuget = Get-PackageProvider -Name NuGet -ListAvailable -ErrorAction SilentlyContinue
        if (-not $nuget) {
            Write-Info "Installing NuGet package provider..."
            Install-PackageProvider -Name NuGet -Force -Scope AllUsers | Out-Null
        }
        Write-Ok "NuGet provider available."
    }
    catch {
        throw "Failed to install or verify NuGet provider. $($_.Exception.Message)"
    }

    try {
        $repo = Get-PSRepository -Name PSGallery -ErrorAction Stop
        if ($repo.InstallationPolicy -ne 'Trusted') {
            Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
            Write-Ok "PSGallery set to Trusted."
        }
        else {
            Write-Ok "PSGallery already Trusted."
        }
    }
    catch {
        throw "Failed to configure PSGallery. $($_.Exception.Message)"
    }
}

function Get-InstalledModuleVersion {
    param([Parameter(Mandatory)][string]$Name)

    $m = Get-InstalledModule -Name $Name -ErrorAction SilentlyContinue
    if ($m) { return $m.Version.ToString() }
    return $null
}

function Install-OrUpdatePwshModule {
    param(
        [Parameter(Mandatory)][string]$Name
    )

    Write-Info "Ensuring pwsh module: $Name"

    try {
        $installedVersion = Get-InstalledModule -Name $Name -ErrorAction SilentlyContinue
        $galleryVersion   = Find-Module -Name $Name -Repository PSGallery -ErrorAction Stop

        if (-not $installedVersion) {
            Install-Module -Name $Name -Scope CurrentUser -Repository PSGallery -Force -AllowClobber -SkipPublisherCheck
            Write-Ok "$Name installed ($($galleryVersion.Version))."
            return
        }

        if ([version]$installedVersion.Version -lt [version]$galleryVersion.Version) {
            Update-Module -Name $Name -Force -ErrorAction Stop
            Write-Ok "$Name updated from $($installedVersion.Version) to $($galleryVersion.Version)."
        }
        else {
            Write-Ok "$Name already current ($($installedVersion.Version))."
        }
    }
    catch {
        Write-WarnEx "Normal install/update path failed for $Name. Trying repair install."
        try {
            Install-Module -Name $Name -Scope CurrentUser -Repository PSGallery -Force -AllowClobber -SkipPublisherCheck -ErrorAction Stop
            Write-Ok "$Name repaired/reinstalled."
        }
        catch {
            throw "Failed to install/update $Name. $($_.Exception.Message)"
        }
    }
}

function Assert-CommandPresent {
    param([Parameter(Mandatory)][string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found after install: $Name"
    }
}

function Get-WindowsPowerShellPath {
    $path = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
    if (-not (Test-Path $path)) {
        throw "Windows PowerShell 5.1 executable not found at: $path"
    }
    return $path
}

function Install-OrUpdateWinPsModules {
    param(
        [Parameter(Mandatory)][string[]]$ModuleNames
    )

    Write-Phase "Windows PowerShell 5.1 module setup"

    $winps = Get-WindowsPowerShellPath

    $scriptBlock = @'
param([string[]]$ModuleNames)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-HostInfo([string]$m) { Write-Host "[WinPS] $m" -ForegroundColor Gray }
function Write-HostOk([string]$m)   { Write-Host "[WinPS] $m" -ForegroundColor Green }

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$nuget = Get-PackageProvider -Name NuGet -ListAvailable -ErrorAction SilentlyContinue
if (-not $nuget) {
    Install-PackageProvider -Name NuGet -Force -Scope AllUsers | Out-Null
}

$repo = Get-PSRepository -Name PSGallery -ErrorAction Stop
if ($repo.InstallationPolicy -ne 'Trusted') {
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
}

foreach ($name in $ModuleNames) {
    Write-HostInfo "Ensuring module: $name"
    $installed = Get-InstalledModule -Name $name -ErrorAction SilentlyContinue
    $gallery   = Find-Module -Name $name -Repository PSGallery -ErrorAction Stop

    if (-not $installed) {
        Install-Module -Name $name -Scope CurrentUser -Repository PSGallery -Force -AllowClobber -SkipPublisherCheck
        Write-HostOk "$name installed ($($gallery.Version))."
        continue
    }

    if ([version]$installed.Version -lt [version]$gallery.Version) {
        Update-Module -Name $name -Force
        Write-HostOk "$name updated from $($installed.Version) to $($gallery.Version))."
    }
    else {
        Write-HostOk "$name already current ($($installed.Version))."
    }
}
'@

    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($scriptBlock))
    $moduleArg = ($ModuleNames | ForEach-Object { "'$_'" }) -join ','

    $output = & $winps -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded -ModuleNames $ModuleNames 2>&1
    $exitCode = $LASTEXITCODE

    $output | ForEach-Object { Write-Host $_ }

    if ($exitCode -ne 0) {
        throw "Windows PowerShell module install/update failed with exit code $exitCode."
    }

    Write-Ok "Windows PowerShell 5.1 module phase completed."
}

function Find-Winget {
    $cmd = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $possible = @(
        "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe",
        "$env:ProgramFiles\WindowsApps"
    )

    foreach ($p in $possible) {
        if (Test-Path $p) { return $p }
    }

    return $null
}

function Ensure-PacCli {
    Write-Phase "Power Platform CLI (pac)"

    $winget = Find-Winget
    $pacCmd = Get-Command pac -ErrorAction SilentlyContinue

    if ($pacCmd) {
        Write-Info "pac already present at $($pacCmd.Source). Attempting update via 'pac install latest'."
        try {
            & pac install latest | Out-Host
            Write-Ok "pac updated."
            return
        }
        catch {
            Write-WarnEx "pac update failed. Will try WinGet/MSI path."
        }
    }

    if ($winget) {
        Write-Info "Installing Power Platform CLI via WinGet."
        try {
            & winget install --id Microsoft.PowerPlatformCLI --exact --accept-source-agreements --accept-package-agreements --silent
            if ($LASTEXITCODE -eq 0) {
                $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
                if (Get-Command pac -ErrorAction SilentlyContinue) {
                    Write-Ok "pac installed via WinGet."
                    return
                }
            }
            else {
                Write-WarnEx "WinGet install returned exit code $LASTEXITCODE."
            }
        }
        catch {
            Write-WarnEx "WinGet install path failed: $($_.Exception.Message)"
        }
    }
    else {
        Write-WarnEx "winget.exe not found. Falling back to Microsoft MSI download."
    }

    try {
        $tempDir = Join-Path $env:TEMP "pac-cli-setup"
        New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
        $msiPath = Join-Path $tempDir "powerapps-cli-1.0.msi"

        # Microsoft docs currently reference this MSI filename for Windows installation.
        $downloadUrl = "https://aka.ms/PowerAppsCLI"
        Write-Info "Downloading pac MSI from $downloadUrl"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $msiPath -UseBasicParsing

        Write-Info "Installing pac MSI silently."
        $proc = Start-Process msiexec.exe -ArgumentList "/i `"$msiPath`" /qn /norestart" -Wait -PassThru
        if ($proc.ExitCode -ne 0) {
            throw "msiexec failed with exit code $($proc.ExitCode)"
        }

        $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
        Assert-CommandPresent -Name 'pac'
        Write-Ok "pac installed via MSI."
    }
    catch {
        throw "Failed to install Power Platform CLI. $($_.Exception.Message)"
    }
}

function Test-ModuleAvailable {
    param(
        [Parameter(Mandatory)][string]$Name
    )
    return [bool](Get-Module -ListAvailable -Name $Name -ErrorAction SilentlyContinue)
}

function Verify-Installs {
    Write-Phase "Verification"

    $pwshModules = @(
        'Microsoft.Graph.Authentication',
        'Microsoft.Graph.Users',
        'Microsoft.Graph.Sites',
        'Microsoft.Graph.Groups',
        'Microsoft.Graph.Teams',
        'Microsoft.Graph.Identity.DirectoryManagement',
        'MicrosoftTeams',
        'PnP.PowerShell',
        'ExchangeOnlineManagement',
        'Microsoft.Entra'
    )

    foreach ($m in $pwshModules) {
        if (Test-ModuleAvailable -Name $m) {
            $ver = (Get-Module -ListAvailable -Name $m | Sort-Object Version -Descending | Select-Object -First 1).Version
            Write-Ok "$m available ($ver)"
        }
        else {
            Write-Fail "$m missing"
        }
    }

    $winps = Get-WindowsPowerShellPath
    $checkScript = @'
$mods = @(
  "Microsoft.PowerApps.Administration.PowerShell",
  "Microsoft.PowerApps.PowerShell"
)

foreach ($m in $mods) {
    $found = Get-Module -ListAvailable -Name $m -ErrorAction SilentlyContinue |
             Sort-Object Version -Descending |
             Select-Object -First 1
    if ($found) {
        Write-Output "$m|$($found.Version)"
    }
    else {
        Write-Output "$m|MISSING"
    }
}
'@
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($checkScript))
    $results = & $winps -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded 2>$null

    foreach ($line in $results) {
        $parts = $line -split '\|', 2
        if ($parts.Count -eq 2) {
            if ($parts[1] -eq 'MISSING') {
                Write-Fail "$($parts[0]) missing in Windows PowerShell 5.1"
            }
            else {
                Write-Ok "$($parts[0]) available in Windows PowerShell 5.1 ($($parts[1]))"
            }
        }
    }

    if (Get-Command pac -ErrorAction SilentlyContinue) {
        $pacVersion = (& pac help 2>$null | Select-Object -First 1)
        Write-Ok "pac available"
        if ($pacVersion) { Write-Info $pacVersion }
    }
    else {
        Write-Fail "pac missing"
    }
}

function Print-NextSteps {
    Write-Phase "Next steps"

    @'
# Run these interactively after setup.

# Microsoft Graph
Connect-MgGraph -Scopes "User.Read.All","Sites.Read.All","Group.Read.All","Directory.Read.All"

# Teams
Connect-MicrosoftTeams

# SharePoint Online via PnP
Connect-PnPOnline -Url "https://<tenant>.sharepoint.com" -Interactive

# Exchange Online
Connect-ExchangeOnline

# Entra
Connect-Entra -Scopes "User.Read.All","Application.Read.All","Directory.Read.All"

# Power Platform admin / maker (runs in Windows PowerShell 5.1)
powershell.exe -NoProfile -Command "Add-PowerAppsAccount"

# Power Platform CLI
pac auth create --name default
'@ | Write-Host -ForegroundColor White
}

# ----------------------------
# Main
# ----------------------------
try {
    Write-Phase "Copilot Studio / M365 Dev Bootstrap"
    Assert-Environment
    Ensure-Tls12
    Ensure-PackageManagementPrereqs

    Write-Phase "Install/update PowerShell 7 modules"

    # Lean Graph install instead of full monolith.
    $pwshModules = @(
        'Microsoft.Graph.Authentication',
        'Microsoft.Graph.Users',
        'Microsoft.Graph.Sites',
        'Microsoft.Graph.Groups',
        'Microsoft.Graph.Teams',
        'Microsoft.Graph.Identity.DirectoryManagement',
        'MicrosoftTeams',
        'PnP.PowerShell',
        'ExchangeOnlineManagement',
        'Microsoft.Entra'
    )

    foreach ($module in $pwshModules) {
        Install-OrUpdatePwshModule -Name $module
    }

    # Power Platform modules still require Windows PowerShell 5.x.
    Install-OrUpdateWinPsModules -ModuleNames @(
        'Microsoft.PowerApps.Administration.PowerShell',
        'Microsoft.PowerApps.PowerShell'
    )

    Ensure-PacCli
    Verify-Installs
    Print-NextSteps

    Write-Phase "Done"
    Write-Ok "Bootstrap completed."
}
catch {
    Write-Fail $_.Exception.Message
    exit 1
}

#requires -Version 7.0
#requires -RunAsAdministrator
<#
.SYNOPSIS
    Grand unified Windows 11 setup for Copilot Studio / Microsoft 365 development.

.DESCRIPTION
    Bootstraps a Windows 11 workstation for Copilot Studio, Power Platform, and
    Microsoft 365 Graph development. Designed to be idempotent — safe to re-run.

    Phases:
      1. Environment guardrails (elevation, Windows, PowerShell 7+)
      2. TLS 1.2 for legacy gallery endpoints
      3. NuGet provider + trusted PSGallery (both shells)
      4. PowerShell 7 modules installed in parallel (Graph SDK split, Teams, PnP,
         Exchange Online, Entra)
      5. Windows PowerShell 5.1 modules (Microsoft.PowerApps.* — these still do
         not support pwsh 7 per Microsoft docs)
      6. Power Platform CLI (pac) via winget, with MSI fallback
      7. Post-install verification + connect-command cheat sheet

.NOTES
    Author : Tim Warner
    Why both shells?
        Microsoft.PowerApps.Administration.PowerShell and
        Microsoft.PowerApps.PowerShell are authored against Windows PowerShell
        5.x and load .NET Framework assemblies that do not resolve cleanly under
        pwsh 7. Microsoft's guidance is to keep them on 5.1.

.EXAMPLE
    # From an elevated PowerShell 7 window:
    pwsh -File .\install-powershell-modules-for-copilot-studio-dev.ps1

.LINK
    https://learn.microsoft.com/power-platform/admin/powershell-getting-started
    https://learn.microsoft.com/power-platform/developer/cli/introduction
#>

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Constants — single source of truth for module lists so install & verify
# phases cannot drift apart.
# ---------------------------------------------------------------------------
$script:PwshModules = @(
    'Microsoft.Graph.Authentication'
    'Microsoft.Graph.Users'
    'Microsoft.Graph.Sites'
    'Microsoft.Graph.Groups'
    'Microsoft.Graph.Teams'
    'Microsoft.Graph.Identity.DirectoryManagement'
    'MicrosoftTeams'
    'PnP.PowerShell'
    'ExchangeOnlineManagement'
    'Microsoft.Entra'
)

$script:WinPsModules = @(
    'Microsoft.PowerApps.Administration.PowerShell'
    'Microsoft.PowerApps.PowerShell'
)

# ---------------------------------------------------------------------------
# Logging helpers — colored, prefixed, and tee-able if the caller redirects.
# ---------------------------------------------------------------------------
function Write-Phase { param([Parameter(Mandatory)][string]$Message) Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Write-Info  { param([Parameter(Mandatory)][string]$Message) Write-Host "[INFO] $Message" -ForegroundColor Gray }
function Write-Ok    { param([Parameter(Mandatory)][string]$Message) Write-Host "[ OK ] $Message" -ForegroundColor Green }
function Write-WarnEx{ param([Parameter(Mandatory)][string]$Message) Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-Fail  { param([Parameter(Mandatory)][string]$Message) Write-Host "[FAIL] $Message" -ForegroundColor Red }

# ---------------------------------------------------------------------------
# Environment guardrails
# ---------------------------------------------------------------------------
function Test-IsAdministrator {
    $identity  = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Confirm-Environment {
    # #requires -RunAsAdministrator handles elevation on pwsh 7+, but we double
    # check so the failure message is informative rather than a cryptic stop.
    if (-not $IsWindows)            { throw "This script is Windows-only." }
    if (-not (Test-IsAdministrator)){ throw "Run this from an elevated PowerShell 7 session." }
    if ($PSVersionTable.PSVersion.Major -lt 7) { throw "Run this script in PowerShell 7 or later." }
    Write-Ok "Environment checks passed (pwsh $($PSVersionTable.PSVersion))."
}

function Set-Tls12 {
    # Some module manifests and the PSGallery SSL endpoints still negotiate
    # poorly on default SChannel when TLS 1.0/1.1 are disabled. Explicit is
    # cheaper than debugging a one-off SSL handshake failure.
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Write-Ok "TLS 1.2 enabled for current session."
    }
    catch {
        Write-WarnEx "Could not explicitly set TLS 1.2: $($_.Exception.Message). Continuing."
    }
}

# ---------------------------------------------------------------------------
# Package management prerequisites
# ---------------------------------------------------------------------------
function Initialize-PackageManagement {
    Write-Phase "Package management prerequisites"

    try {
        if (-not (Get-PackageProvider -Name NuGet -ListAvailable -ErrorAction SilentlyContinue)) {
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

# ---------------------------------------------------------------------------
# PowerShell 7 module installer — parallelized
# ---------------------------------------------------------------------------
function Install-PwshModules {
    param([Parameter(Mandatory)][string[]]$ModuleNames)

    Write-Phase "PowerShell 7 module install/update (parallel)"

    # ForEach -Parallel spins a runspace per module. PowerShellGet is thread
    # safe for CurrentUser-scoped installs against distinct modules, so we
    # get a ~Nx speedup (bounded by ThrottleLimit) without risking collisions.
    $results = $ModuleNames | ForEach-Object -ThrottleLimit 5 -Parallel {
        $name = $_
        $out  = [pscustomobject]@{ Name = $name; Status = ''; Message = '' }

        try {
            $installed = Get-InstalledModule -Name $name -ErrorAction SilentlyContinue
            $gallery   = Find-Module -Name $name -Repository PSGallery -ErrorAction Stop

            if (-not $installed) {
                Install-Module -Name $name -Scope CurrentUser -Repository PSGallery `
                    -Force -AllowClobber -SkipPublisherCheck -ErrorAction Stop
                $out.Status  = 'Installed'
                $out.Message = "$name installed ($($gallery.Version))."
            }
            elseif ([version]$installed.Version -lt [version]$gallery.Version) {
                Update-Module -Name $name -Force -ErrorAction Stop
                $out.Status  = 'Updated'
                $out.Message = "$name updated from $($installed.Version) to $($gallery.Version)."
            }
            else {
                $out.Status  = 'Current'
                $out.Message = "$name already current ($($installed.Version))."
            }
        }
        catch {
            # Repair pass — a partial install from a previous run can poison
            # Get-InstalledModule. Force reinstall with -AllowClobber resolves.
            try {
                Install-Module -Name $name -Scope CurrentUser -Repository PSGallery `
                    -Force -AllowClobber -SkipPublisherCheck -ErrorAction Stop
                $out.Status  = 'Repaired'
                $out.Message = "$name repaired/reinstalled."
            }
            catch {
                $out.Status  = 'Failed'
                $out.Message = "$name failed: $($_.Exception.Message)"
            }
        }
        $out
    }

    foreach ($r in $results) {
        switch ($r.Status) {
            'Failed' { Write-Fail $r.Message }
            default  { Write-Ok   $r.Message }
        }
    }

    if ($results | Where-Object Status -eq 'Failed') {
        throw "One or more pwsh 7 modules failed to install. See [FAIL] lines above."
    }
}

# ---------------------------------------------------------------------------
# Windows PowerShell 5.1 module installer
# ---------------------------------------------------------------------------
function Get-WindowsPowerShellPath {
    $path = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
    if (-not (Test-Path $path)) { throw "Windows PowerShell 5.1 executable not found at: $path" }
    return $path
}

function Install-WinPsModules {
    param([Parameter(Mandatory)][string[]]$ModuleNames)

    Write-Phase "Windows PowerShell 5.1 module setup"

    $winps = Get-WindowsPowerShellPath

    # Inline the module list into the child script rather than rely on
    # -EncodedCommand argument passing (which is NOT supported — the prior
    # version silently ran against an empty list). We bake the literal array
    # into the script text so the child process is fully self-contained.
    $moduleLiteral = ($ModuleNames | ForEach-Object { "'$($_.Replace("'","''"))'" }) -join ','

    $scriptBlock = @"
`$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-HostInfo(`$m) { Write-Host "[WinPS] `$m" -ForegroundColor Gray  }
function Write-HostOk  (`$m) { Write-Host "[WinPS] `$m" -ForegroundColor Green }
function Write-HostFail(`$m) { Write-Host "[WinPS] `$m" -ForegroundColor Red   }

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

if (-not (Get-PackageProvider -Name NuGet -ListAvailable -ErrorAction SilentlyContinue)) {
    Install-PackageProvider -Name NuGet -Force -Scope AllUsers | Out-Null
}

`$repo = Get-PSRepository -Name PSGallery -ErrorAction Stop
if (`$repo.InstallationPolicy -ne 'Trusted') {
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
}

`$modules = @($moduleLiteral)
`$failed  = @()

foreach (`$name in `$modules) {
    try {
        Write-HostInfo "Ensuring module: `$name"
        `$installed = Get-InstalledModule -Name `$name -ErrorAction SilentlyContinue
        `$gallery   = Find-Module      -Name `$name -Repository PSGallery -ErrorAction Stop

        if (-not `$installed) {
            Install-Module -Name `$name -Scope CurrentUser -Repository PSGallery ``
                -Force -AllowClobber -SkipPublisherCheck -ErrorAction Stop
            Write-HostOk "`$name installed (`$(`$gallery.Version))."
        }
        elseif ([version]`$installed.Version -lt [version]`$gallery.Version) {
            Update-Module -Name `$name -Force -ErrorAction Stop
            Write-HostOk "`$name updated from `$(`$installed.Version) to `$(`$gallery.Version)."
        }
        else {
            Write-HostOk "`$name already current (`$(`$installed.Version))."
        }
    }
    catch {
        Write-HostFail "`$name failed: `$(`$_.Exception.Message)"
        `$failed += `$name
    }
}

if (`$failed.Count -gt 0) { exit 2 }
exit 0
"@

    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($scriptBlock))

    & $winps -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded 2>&1 | ForEach-Object { Write-Host $_ }
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        throw "Windows PowerShell module install/update failed with exit code $exitCode."
    }
    Write-Ok "Windows PowerShell 5.1 module phase completed."
}

# ---------------------------------------------------------------------------
# Power Platform CLI (pac)
# ---------------------------------------------------------------------------
function Find-Winget {
    # Get-Command resolves PATH correctly; only fall back to known install
    # locations that are themselves executables (not parent directories).
    $cmd = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidate = Join-Path $env:LOCALAPPDATA 'Microsoft\WindowsApps\winget.exe'
    if (Test-Path $candidate) { return $candidate }

    return $null
}

function Update-PathFromMachineAndUser {
    # Refresh PATH in-process after an installer mutates the Machine/User
    # environment blocks — otherwise the newly installed command won't be
    # discoverable until the user opens a new shell.
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
                [System.Environment]::GetEnvironmentVariable('Path','User')
}

function Install-PacCli {
    Write-Phase "Power Platform CLI (pac)"

    $winget = Find-Winget

    # Preferred path: winget install-or-upgrade. `pac install latest` from the
    # previous version of this script is not a real pac command.
    if ($winget) {
        Write-Info "Installing/upgrading Power Platform CLI via WinGet."
        try {
            $wingetArgs = @(
                'install', '--id', 'Microsoft.PowerPlatformCLI',
                '--exact', '--accept-source-agreements', '--accept-package-agreements', '--silent'
            )
            & $winget @wingetArgs
            # winget returns 0 on install and a non-zero "no available upgrade"
            # code (e.g. 0x8A15002B) when already current. Treat "command exists
            # after the call" as the real success signal.
            Update-PathFromMachineAndUser
            if (Get-Command pac -ErrorAction SilentlyContinue) {
                Write-Ok "pac available via WinGet."
                return
            }
            Write-WarnEx "WinGet finished (exit $LASTEXITCODE) but pac still not on PATH. Falling back to MSI."
        }
        catch {
            Write-WarnEx "WinGet install path failed: $($_.Exception.Message)"
        }
    }
    else {
        Write-WarnEx "winget.exe not found. Falling back to Microsoft MSI download."
    }

    # MSI fallback — aka.ms/PowerAppsCLI currently 302s to the signed MSI.
    try {
        $tempDir = Join-Path $env:TEMP 'pac-cli-setup'
        New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
        $msiPath = Join-Path $tempDir 'powerapps-cli.msi'

        $downloadUrl = 'https://aka.ms/PowerAppsCLI'
        Write-Info "Downloading pac MSI from $downloadUrl"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $msiPath -UseBasicParsing

        Write-Info "Installing pac MSI silently."
        $proc = Start-Process msiexec.exe -ArgumentList "/i `"$msiPath`" /qn /norestart" -Wait -PassThru
        if ($proc.ExitCode -ne 0) { throw "msiexec failed with exit code $($proc.ExitCode)" }

        Update-PathFromMachineAndUser
        if (-not (Get-Command pac -ErrorAction SilentlyContinue)) {
            throw "pac not found on PATH after MSI install. Open a new shell and re-run."
        }
        Write-Ok "pac installed via MSI."
    }
    catch {
        throw "Failed to install Power Platform CLI. $($_.Exception.Message)"
    }
}

# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
function Test-ModuleAvailable {
    param([Parameter(Mandatory)][string]$Name)
    return [bool](Get-Module -ListAvailable -Name $Name -ErrorAction SilentlyContinue)
}

function Test-Installs {
    Write-Phase "Verification"

    foreach ($m in $script:PwshModules) {
        if (Test-ModuleAvailable -Name $m) {
            $ver = (Get-Module -ListAvailable -Name $m | Sort-Object Version -Descending | Select-Object -First 1).Version
            Write-Ok "$m available ($ver)"
        }
        else {
            Write-Fail "$m missing"
        }
    }

    # Probe WinPS 5.1 for the Power Platform modules. Pipe-delimited output is
    # easier to parse than Write-Host text.
    $winps = Get-WindowsPowerShellPath
    $moduleLiteral = ($script:WinPsModules | ForEach-Object { "'$($_.Replace("'","''"))'" }) -join ','
    $checkScript = @"
`$mods = @($moduleLiteral)
foreach (`$m in `$mods) {
    `$found = Get-Module -ListAvailable -Name `$m -ErrorAction SilentlyContinue |
             Sort-Object Version -Descending | Select-Object -First 1
    if (`$found) { Write-Output "`$m|`$(`$found.Version)" }
    else         { Write-Output "`$m|MISSING" }
}
"@
    $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($checkScript))
    $results = & $winps -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encoded 2>$null

    foreach ($line in $results) {
        $parts = $line -split '\|', 2
        if ($parts.Count -ne 2) { continue }
        if ($parts[1] -eq 'MISSING') { Write-Fail "$($parts[0]) missing in Windows PowerShell 5.1" }
        else                         { Write-Ok   "$($parts[0]) available in Windows PowerShell 5.1 ($($parts[1]))" }
    }

    if (Get-Command pac -ErrorAction SilentlyContinue) {
        $pacVersion = (& pac --version 2>$null | Select-Object -First 1)
        Write-Ok "pac available"
        if ($pacVersion) { Write-Info "pac version: $pacVersion" }
    }
    else {
        Write-Fail "pac missing"
    }
}

# ---------------------------------------------------------------------------
# Next-step cheat sheet
# ---------------------------------------------------------------------------
function Show-NextSteps {
    Write-Phase "Next steps"
    @'
# Run these interactively after setup.

# Microsoft Graph
Connect-MgGraph -Scopes "User.Read.All","Sites.Read.All","Group.Read.All","Directory.Read.All"

# Teams
Connect-MicrosoftTeams

# SharePoint Online via PnP
# PnP.PowerShell 2.x REQUIRES your own Entra app registration — the built-in
# multi-tenant app was retired. One-time setup (admin consent required):
#   Register-PnPEntraIDAppForInteractiveLogin `
#       -ApplicationName "PnP PowerShell CLI" `
#       -Tenant "<tenant>.onmicrosoft.com" `
#       -Interactive
# Then connect with the ClientId it prints:
Connect-PnPOnline -Url "https://<tenant>.sharepoint.com" -Interactive -ClientId "<app-id>"

# Exchange Online
Connect-ExchangeOnline
# If you hit an MSAL RuntimeBroker NullReferenceException on pwsh 7, the WAM
# broker failed to init. Use device code or browser auth instead:
#   Connect-ExchangeOnline -Device
#   Connect-ExchangeOnline -UseWebLogin

# Entra
Connect-Entra -Scopes "User.Read.All","Application.Read.All","Directory.Read.All"

# Power Platform admin / maker (runs in Windows PowerShell 5.1)
powershell.exe -NoProfile -Command "Add-PowerAppsAccount"

# Power Platform CLI
pac auth create --name default
'@ | Write-Host -ForegroundColor White
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
try {
    $sw = [Diagnostics.Stopwatch]::StartNew()

    Write-Phase "Copilot Studio / M365 Dev Bootstrap"
    Confirm-Environment
    Set-Tls12
    Initialize-PackageManagement

    Install-PwshModules  -ModuleNames $script:PwshModules
    Install-WinPsModules -ModuleNames $script:WinPsModules

    Install-PacCli
    Test-Installs
    Show-NextSteps

    $sw.Stop()
    Write-Phase "Done"
    Write-Ok "Bootstrap completed in $([int]$sw.Elapsed.TotalSeconds)s."
}
catch {
    Write-Fail $_.Exception.Message
    exit 1
}

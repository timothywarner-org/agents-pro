<#
.SYNOPSIS
    Stages the Contoso Pinball Gallery Concierge agent intelligence pack to SharePoint.

.DESCRIPTION
    Uploads the local agent teaching artifacts to an existing SharePoint site,
    preserving the repo-relative folder structure under a stable target folder.
    The script is idempotent: files are overwritten in place and folders are
    created only when missing.

.PARAMETER SharePointHost
    SharePoint host name, for example timwinfo2.sharepoint.com.

.PARAMETER SitePath
    Server-relative site path, for example /sites/CERTSTAR.NET.

.PARAMETER TargetFolder
    Folder under the site's default document library.

.PARAMETER ProjectRoot
    Path to the Contoso Pinball Gallery Concierge project folder.

.PARAMETER TenantId
    Microsoft Entra tenant ID.

.PARAMETER GraphScopes
    Microsoft Graph delegated scopes used for staging.

.EXAMPLE
    pwsh .\scripts\stage-contoso-agent-intelligence.graph.ps1 `
      -SharePointHost timwinfo2.sharepoint.com `
      -SitePath /sites/CERTSTAR.NET
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter()]
    [ValidatePattern('^[a-zA-Z0-9.-]+\.sharepoint\.com$')]
    [string] $SharePointHost = 'timwinfo2.sharepoint.com',

    [Parameter()]
    [ValidatePattern('^/sites/[a-zA-Z0-9._-]+$')]
    [string] $SitePath = '/sites/CERTSTAR.NET',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $TargetFolder = 'Pinball Concierge Agent Intelligence',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $ProjectRoot = (Split-Path -Parent (Split-Path -Parent $PSCommandPath)),

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $TenantId = 'f74b1450-e46a-41df-abee-ebf3621bfd85',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string[]] $GraphScopes = @('Sites.ReadWrite.All', 'Files.ReadWrite.All'),

    [Parameter()]
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:GraphRoot = 'https://graph.microsoft.com/v1.0'
$script:StageTargetFolder = $TargetFolder

function Write-Step {
    param([Parameter(Mandatory)][string] $Message)
    Write-Host "[contoso-intelligence-stage] $Message"
}

function Connect-Graph {
    Import-Module Microsoft.Graph.Authentication -ErrorAction Stop

    $context = Get-MgContext
    $missingScopes = @()
    if ($context) {
        $missingScopes = @($GraphScopes | Where-Object { $_ -notin $context.Scopes })
    }

    if (-not $context -or $context.TenantId -ne $TenantId -or $missingScopes.Count -gt 0) {
        Write-Step "Connecting to Microsoft Graph with scopes: $($GraphScopes -join ', ')"
        Connect-MgGraph `
            -TenantId $TenantId `
            -Scopes $GraphScopes `
            -ContextScope CurrentUser `
            -NoWelcome | Out-Null
        $context = Get-MgContext
    }

    if (-not $context) {
        throw "Microsoft Graph authentication did not return a context."
    }

    $missingScopes = @($GraphScopes | Where-Object { $_ -notin $context.Scopes })
    if ($missingScopes.Count -gt 0) {
        throw "Microsoft Graph context is missing required scopes: $($missingScopes -join ', ')."
    }

    Write-Step "Graph context: $($context.Account) / tenant $($context.TenantId)"
}

function Invoke-Graph {
    param(
        [Parameter(Mandatory)][ValidateSet('GET', 'POST', 'PUT')]
        [string] $Method,
        [Parameter(Mandatory)][string] $Uri,
        [Parameter()][object] $Body,
        [Parameter()][string] $InputFilePath,
        [Parameter()][string] $ContentType = 'application/json'
    )

    $args = @{
        Method      = $Method
        Uri         = $Uri
        ErrorAction = 'Stop'
    }

    if ($Body) {
        $args.Body = $Body | ConvertTo-Json -Depth 20
        $args.ContentType = $ContentType
    }

    if ($InputFilePath) {
        $args.InputFilePath = $InputFilePath
        $args.ContentType = $ContentType
    }

    try {
        return Invoke-MgGraphRequest @args
    }
    catch {
        $detail = $_.ErrorDetails.Message
        if ([string]::IsNullOrWhiteSpace($detail)) {
            $detail = $_.Exception.Message
        }
        throw "Graph $Method failed for $Uri. $detail"
    }
}

function ConvertTo-GraphPath {
    param([Parameter(Mandatory)][string[]] $Segments)
    return ($Segments | ForEach-Object { [Uri]::EscapeDataString($_) -replace '%2F', '/' }) -join '/'
}

function Get-Site {
    $encodedPath = $SitePath.TrimEnd('/')
    $uri = "$script:GraphRoot/sites/$SharePointHost`:$encodedPath`?`$select=id,displayName,webUrl"
    return Invoke-Graph -Method GET -Uri $uri
}

function Test-DrivePath([string] $SiteId, [string[]] $Segments) {
    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $path = ConvertTo-GraphPath -Segments $Segments
    try {
        Invoke-MgGraphRequest -Method GET -Uri "$script:GraphRoot/sites/$encodedSiteId/drive/root:/$path" -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Ensure-DriveFolder([string] $SiteId, [string[]] $Segments) {
    if ($null -eq $Segments -or $Segments.Count -eq 0) {
        throw "Ensure-DriveFolder received no path segments."
    }

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $currentSegments = @()

    foreach ($segment in $Segments) {
        $parentSegments = @($currentSegments)
        $currentSegments += $segment

        if (Test-DrivePath $SiteId $currentSegments) {
            continue
        }

        $childrenUri = if ($parentSegments.Count -eq 0) {
            "$script:GraphRoot/sites/$encodedSiteId/drive/root/children"
        }
        else {
            $parentPath = ConvertTo-GraphPath -Segments $parentSegments
            "$script:GraphRoot/sites/$encodedSiteId/drive/root:/$parentPath`:/children"
        }

        if ($PSCmdlet.ShouldProcess(($currentSegments -join '/'), 'Create SharePoint folder')) {
            Invoke-Graph -Method POST -Uri $childrenUri -Body @{
                name = $segment
                folder = @{}
                '@microsoft.graph.conflictBehavior' = 'replace'
            } | Out-Null
        }
    }
}

function Get-AgentFiles {
    $includeExtensions = @('.md', '.yml', '.yaml', '.json', '.ps1', '.svg')
    Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File |
        Where-Object {
            $includeExtensions -contains $_.Extension.ToLowerInvariant() -and
            $_.FullName -notmatch '\\.git\\'
        } |
        Sort-Object FullName
}

function Publish-AgentFiles {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $RootFolder
    )

    # Fixed folder name keeps Copilot Studio setup docs and live demo paths stable.
    $publishRootFolder = 'Pinball Concierge Agent Intelligence'

    $files = @(Get-AgentFiles)
    $encodedSiteId = [Uri]::EscapeDataString($SiteId)

    Ensure-DriveFolder $SiteId @($publishRootFolder)

    foreach ($file in $files) {
        $relativePath = [IO.Path]::GetRelativePath($ProjectRoot, $file.FullName)
        $relativeSegments = $relativePath -split '[\\/]'

        if ($relativeSegments.Count -gt 1) {
            $folderSegments = @($publishRootFolder) + @($relativeSegments[0..($relativeSegments.Count - 2)])
            Ensure-DriveFolder $SiteId ([string[]] $folderSegments)
        }

        $targetSegments = @($publishRootFolder) + $relativeSegments
        $targetPath = ConvertTo-GraphPath -Segments $targetSegments
        $uri = "$script:GraphRoot/sites/$encodedSiteId/drive/root:/$targetPath`:/content"

        if ($DryRun) {
            Write-Step "Would upload: $relativePath"
            continue
        }

        if ($PSCmdlet.ShouldProcess($relativePath, 'Upload agent intelligence file')) {
            Invoke-Graph -Method PUT -Uri $uri -InputFilePath $file.FullName -ContentType 'application/octet-stream' | Out-Null
        }
    }

    Write-Step "Staged $($files.Count) files under '$publishRootFolder'."
}

Connect-Graph
Write-Step "Project root: $ProjectRoot"
Write-Step "Target site: https://$SharePointHost$SitePath"
Write-Step "Target folder: $script:StageTargetFolder"

$site = Get-Site
Write-Step "Resolved site: $($site.displayName) <$($site.webUrl)>"

Publish-AgentFiles -SiteId $site.id -RootFolder $script:StageTargetFolder

Write-Host ''
Write-Host 'Agent intelligence staging summary'
Write-Host '----------------------------------'
Write-Host "Site:          $($site.webUrl)"
Write-Host "Folder:        $script:StageTargetFolder"
Write-Host "Local source:  $ProjectRoot"

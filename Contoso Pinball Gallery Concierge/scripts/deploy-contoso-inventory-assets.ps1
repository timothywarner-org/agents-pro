<#
.SYNOPSIS
    Deploys Contoso Pinball Gallery inventory demo assets to a Microsoft 365 SharePoint tenant.

.DESCRIPTION
    Creates or updates the SharePoint site, knowledge document library, inventory
    lists, list fields, seed list rows, and knowledge files used by the Contoso
    Pinball Gallery Concierge Inventory Lookup flow.

    The script is idempotent. It uses stable business keys such as SKU,
    HoldReference, and MovementReference so re-running updates existing records
    instead of creating duplicates.

.PARAMETER TenantName
    SharePoint tenant short name. For https://contoso.sharepoint.com, use contoso.

.PARAMETER SiteAlias
    SharePoint site alias under /sites.

.PARAMETER SiteTitle
    Display title for the SharePoint site.

.PARAMETER OwnerEmail
    Optional owner UPN used when creating the site.

.PARAMETER ClientId
    Optional Entra application client ID for PnP.PowerShell interactive auth.
    If omitted, PnP.PowerShell uses its configured default or environment value.

.PARAMETER DeviceLogin
    Uses PnP.PowerShell device-code authentication instead of browser interactive
    authentication. This is better for terminal-only agent sessions.

.PARAMETER OSLogin
    Uses the Windows account broker for PnP.PowerShell authentication. This is
    the preferred path when the admin account is already signed in on Windows.

.PARAMETER UseAzureCliToken
    Uses the current Azure CLI login to request a SharePoint access token for
    each PnP connection. This avoids browser prompts in automation terminals.

.PARAMETER ProjectRoot
    Path to the Contoso Pinball Gallery Concierge project folder.

.PARAMETER SkipSiteCreation
    Connects to the target site and provisions assets without creating the site.

.PARAMETER DryRun
    Shows the intended target and validates local assets without writing to M365.

.EXAMPLE
    pwsh .\scripts\deploy-contoso-inventory-assets.ps1 `
      -TenantName techtrainertim `
      -OwnerEmail admin@techtrainertim.com

.EXAMPLE
    pwsh .\scripts\deploy-contoso-inventory-assets.ps1 `
      -TenantName techtrainertim `
      -ClientId "00000000-0000-0000-0000-000000000000" `
      -SiteAlias ContosoPinballGallery
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter()]
    [ValidatePattern('^[a-zA-Z0-9-]+$')]
    [string] $TenantName = 'techtrainertim',

    [Parameter()]
    [ValidatePattern('^[a-zA-Z0-9.-]+$')]
    [string] $SiteAlias = 'ContosoPinballGallery',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $SiteTitle = 'Contoso Pinball Gallery',

    [Parameter()]
    [ValidatePattern('^[^@\s]+@[^@\s]+\.[^@\s]+$')]
    [string] $OwnerEmail,

    [Parameter()]
    [ValidatePattern('^[0-9a-fA-F-]{36}$')]
    [string] $ClientId,

    [Parameter()]
    [switch] $DeviceLogin,

    [Parameter()]
    [switch] $OSLogin,

    [Parameter()]
    [switch] $UseAzureCliToken,

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $ProjectRoot = (Split-Path -Parent (Split-Path -Parent $PSCommandPath)),

    [Parameter()]
    [switch] $SkipSiteCreation,

    [Parameter()]
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:Lists = @{
    Machines  = 'CPG Inventory Machines'
    Holds     = 'CPG Inventory Holds'
    Movements = 'CPG Inventory Movements'
}

$script:KnowledgeLibrary = 'Concierge Knowledge'

function Write-Step {
    param([Parameter(Mandatory)][string] $Message)
    Write-Host "[contoso-inventory] $Message"
}

function Resolve-AssetPath {
    param([Parameter(Mandatory)][string] $RelativePath)
    $path = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required asset not found: $path"
    }
    return (Resolve-Path -LiteralPath $path).Path
}

function Import-SeedJson {
    param([Parameter(Mandatory)][string] $RelativePath)
    $path = Resolve-AssetPath -RelativePath $RelativePath
    return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
}

function Assert-Module {
    if (-not (Get-Module -ListAvailable -Name PnP.PowerShell)) {
        throw @"
PnP.PowerShell is required.

Install it from an elevated PowerShell 7 session:
  Install-Module PnP.PowerShell -Scope CurrentUser

Then rerun this script. If your tenant requires a custom PnP Entra app,
pass -ClientId or set PNPPOWERSHELL_CLIENTID.
"@
    }

    Import-Module PnP.PowerShell -ErrorAction Stop
}

function Connect-ContosoPnP {
    param([Parameter(Mandatory)][string] $Url)

    $connectArgs = @{
        Url = $Url
    }

    $authModeCount = @($DeviceLogin, $OSLogin, $UseAzureCliToken).Where({ $_ }).Count
    if ($authModeCount -gt 1) {
        throw "Choose only one auth mode: -DeviceLogin, -OSLogin, or -UseAzureCliToken."
    }

    if ($UseAzureCliToken) {
        $resource = 'https://{0}' -f ([Uri] $Url).Host
        Write-Step "Requesting Azure CLI token for $resource"
        $token = az account get-access-token --resource $resource --query accessToken -o tsv
        if ([string]::IsNullOrWhiteSpace($token)) {
            throw "Azure CLI did not return an access token for $resource. Run az login as $OwnerEmail and retry."
        }

        $connectArgs.AccessToken = $token
    }
    elseif ($OSLogin) {
        $connectArgs.OSLogin = $true
        $connectArgs.PersistLogin = $true
    }
    elseif ($DeviceLogin) {
        $connectArgs.DeviceLogin = $true
        $connectArgs.PersistLogin = $true
    }
    else {
        $connectArgs.Interactive = $true
        $connectArgs.PersistLogin = $true
    }

    if ($ClientId) {
        $connectArgs.ClientId = $ClientId
    }

    Write-Step "Connecting to $Url"
    Connect-PnPOnline @connectArgs
}

function Ensure-ContosoSite {
    param(
        [Parameter(Mandatory)][string] $AdminUrl,
        [Parameter(Mandatory)][string] $SiteUrl
    )

    if ($SkipSiteCreation) {
        Write-Step "Skipping site creation. Target site must already exist: $SiteUrl"
        return
    }

    Connect-ContosoPnP -Url $AdminUrl

    $existing = Get-PnPTenantSite -Url $SiteUrl -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Step "Site already exists: $SiteUrl"
        return
    }

    if (-not $OwnerEmail) {
        throw "Site does not exist and -OwnerEmail was not provided. Pass -OwnerEmail admin@techtrainertim.com or use -SkipSiteCreation."
    }

    if ($PSCmdlet.ShouldProcess($SiteUrl, 'Create SharePoint communication site')) {
        Write-Step "Creating communication site: $SiteUrl"
        New-PnPSite `
            -Type CommunicationSite `
            -Title $SiteTitle `
            -Url $SiteUrl `
            -Owner $OwnerEmail `
            -SiteDesign Topic | Out-Null
    }
}

function Ensure-List {
    param(
        [Parameter(Mandatory)][string] $Title,
        [Parameter(Mandatory)][string] $Template
    )

    $list = Get-PnPList -Identity $Title -ErrorAction SilentlyContinue
    if ($list) {
        Write-Step "List/library exists: $Title"
        return $list
    }

    if ($PSCmdlet.ShouldProcess($Title, "Create SharePoint $Template")) {
        Write-Step "Creating $Template`: $Title"
        return New-PnPList -Title $Title -Template $Template -OnQuickLaunch
    }
}

function Ensure-Field {
    param(
        [Parameter(Mandatory)][string] $ListTitle,
        [Parameter(Mandatory)][string] $InternalName,
        [Parameter(Mandatory)][string] $DisplayName,
        [Parameter(Mandatory)][string] $Type,
        [Parameter()][string[]] $Choices,
        [Parameter()][switch] $Required,
        [Parameter()][switch] $AddToDefaultView
    )

    $existing = Get-PnPField -List $ListTitle -Identity $InternalName -ErrorAction SilentlyContinue
    if ($existing) {
        return
    }

    if ($PSCmdlet.ShouldProcess("$ListTitle.$InternalName", 'Create SharePoint field')) {
        if ($Type -eq 'Choice') {
            $choiceXml = ($Choices | ForEach-Object { "<CHOICE>$([System.Security.SecurityElement]::Escape($_))</CHOICE>" }) -join ''
            $requiredValue = if ($Required) { 'TRUE' } else { 'FALSE' }
            $fieldXml = "<Field Type='Choice' DisplayName='$DisplayName' Name='$InternalName' StaticName='$InternalName' Required='$requiredValue' Format='Dropdown'><CHOICES>$choiceXml</CHOICES></Field>"
            Add-PnPFieldFromXml -List $ListTitle -FieldXml $fieldXml | Out-Null
        }
        else {
            Add-PnPField `
                -List $ListTitle `
                -DisplayName $DisplayName `
                -InternalName $InternalName `
                -Type $Type `
                -Required:$Required `
                -AddToDefaultView:$AddToDefaultView | Out-Null
        }

        if ($AddToDefaultView -and $Type -eq 'Choice') {
            Add-PnPViewField -List $ListTitle -Identity 'All Items' -Field $InternalName -ErrorAction SilentlyContinue
        }
    }
}

function Ensure-InventorySchema {
    Ensure-List -Title $script:Lists.Machines -Template GenericList | Out-Null
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'SKU' -DisplayName 'SKU' -Type Text -Required -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Manufacturer' -DisplayName 'Manufacturer' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'ModelYear' -DisplayName 'Model Year' -Type Number -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Era' -DisplayName 'Era' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'ConditionGrade' -DisplayName 'Condition Grade' -Type Choice -Choices @('Museum', 'Excellent', 'Very Good', 'Good', 'Project') -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'PriceUsd' -DisplayName 'Price USD' -Type Currency -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Availability' -DisplayName 'Availability' -Type Choice -Choices @('In stock', 'On hold', 'Sold - waitlist open', 'On order') -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Location' -DisplayName 'Location' -Type Text
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'SerialNumber' -DisplayName 'Serial Number' -Type Text
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'WarrantyDays' -DisplayName 'Warranty Days' -Type Number
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'HoldExpiresUtc' -DisplayName 'Hold Expires UTC' -Type DateTime
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Featured' -DisplayName 'Featured' -Type Boolean -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Tags' -DisplayName 'Tags' -Type Text
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'Notes' -DisplayName 'Notes' -Type Note
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'ServiceStatus' -DisplayName 'Service Status' -Type Text
    Ensure-Field -ListTitle $script:Lists.Machines -InternalName 'SourceDocument' -DisplayName 'Source Document' -Type Text

    Ensure-List -Title $script:Lists.Holds -Template GenericList | Out-Null
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'HoldReference' -DisplayName 'Hold Reference' -Type Text -Required -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'SKU' -DisplayName 'SKU' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'MachineTitle' -DisplayName 'Machine Title' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'ContactName' -DisplayName 'Contact Name' -Type Text
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'ContactEmail' -DisplayName 'Contact Email' -Type Text
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'Status' -DisplayName 'Status' -Type Choice -Choices @('Pending deposit', 'Active', 'Released', 'Expired', 'Converted') -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'ExpiresUtc' -DisplayName 'Expires UTC' -Type DateTime -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Holds -InternalName 'Notes' -DisplayName 'Notes' -Type Note

    Ensure-List -Title $script:Lists.Movements -Template GenericList | Out-Null
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'MovementReference' -DisplayName 'Movement Reference' -Type Text -Required -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'SKU' -DisplayName 'SKU' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'MachineTitle' -DisplayName 'Machine Title' -Type Text -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'MovementType' -DisplayName 'Movement Type' -Type Choice -Choices @('New arrival', 'Hold placed', 'Hold released', 'Sold', 'Restoration complete', 'Price update') -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'MovementUtc' -DisplayName 'Movement UTC' -Type DateTime -AddToDefaultView
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'QuantityDelta' -DisplayName 'Quantity Delta' -Type Number
    Ensure-Field -ListTitle $script:Lists.Movements -InternalName 'Notes' -DisplayName 'Notes' -Type Note
}

function ConvertTo-PnPValue {
    param([object] $Value)
    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [System.Array]) {
        return ($Value -join '; ')
    }

    return $Value
}

function Get-ListItemByKey {
    param(
        [Parameter(Mandatory)][string] $ListTitle,
        [Parameter(Mandatory)][string] $FieldName,
        [Parameter(Mandatory)][string] $FieldValue
    )

    $escapedValue = [System.Security.SecurityElement]::Escape($FieldValue)
    $query = @"
<View>
  <Query>
    <Where>
      <Eq>
        <FieldRef Name='$FieldName' />
        <Value Type='Text'>$escapedValue</Value>
      </Eq>
    </Where>
  </Query>
  <RowLimit>1</RowLimit>
</View>
"@

    return Get-PnPListItem -List $ListTitle -Query $query -ErrorAction Stop | Select-Object -First 1
}

function Upsert-ListItem {
    param(
        [Parameter(Mandatory)][string] $ListTitle,
        [Parameter(Mandatory)][string] $KeyField,
        [Parameter(Mandatory)][string] $KeyValue,
        [Parameter(Mandatory)][hashtable] $Values
    )

    $item = Get-ListItemByKey -ListTitle $ListTitle -FieldName $KeyField -FieldValue $KeyValue

    if ($item) {
        if ($PSCmdlet.ShouldProcess("$ListTitle/$KeyValue", 'Update SharePoint list item')) {
            Set-PnPListItem -List $ListTitle -Identity $item.Id -Values $Values | Out-Null
        }
        return
    }

    if ($PSCmdlet.ShouldProcess("$ListTitle/$KeyValue", 'Create SharePoint list item')) {
        Add-PnPListItem -List $ListTitle -Values $Values | Out-Null
    }
}

function Sync-MachineRows {
    $machines = Import-SeedJson -RelativePath 'data/inventory-machines.seed.json'
    foreach ($machine in $machines) {
        $values = @{
            Title          = $machine.title
            SKU            = $machine.sku
            Manufacturer   = $machine.manufacturer
            ModelYear      = $machine.modelYear
            Era            = $machine.era
            ConditionGrade = $machine.conditionGrade
            PriceUsd       = $machine.priceUsd
            Availability   = $machine.availability
            Location       = $machine.location
            SerialNumber   = $machine.serialNumber
            WarrantyDays   = $machine.warrantyDays
            HoldExpiresUtc = $machine.holdExpiresUtc
            Featured       = [bool] $machine.featured
            Tags           = ConvertTo-PnPValue -Value $machine.tags
            Notes          = $machine.notes
            ServiceStatus  = $machine.serviceStatus
            SourceDocument = $machine.sourceDocument
        }

        Upsert-ListItem -ListTitle $script:Lists.Machines -KeyField 'SKU' -KeyValue $machine.sku -Values $values
    }

    Write-Step "Synced $($machines.Count) machine inventory rows."
}

function Sync-HoldRows {
    $holds = Import-SeedJson -RelativePath 'data/inventory-holds.seed.json'
    foreach ($hold in $holds) {
        $values = @{
            Title         = $hold.holdReference
            HoldReference = $hold.holdReference
            SKU           = $hold.sku
            MachineTitle  = $hold.machineTitle
            ContactName   = $hold.contactName
            ContactEmail  = $hold.contactEmail
            Status        = $hold.status
            ExpiresUtc    = $hold.expiresUtc
            Notes         = $hold.notes
        }

        Upsert-ListItem -ListTitle $script:Lists.Holds -KeyField 'HoldReference' -KeyValue $hold.holdReference -Values $values
    }

    Write-Step "Synced $($holds.Count) hold rows."
}

function Sync-MovementRows {
    $movements = Import-SeedJson -RelativePath 'data/inventory-movements.seed.json'
    foreach ($movement in $movements) {
        $values = @{
            Title             = $movement.movementReference
            MovementReference = $movement.movementReference
            SKU               = $movement.sku
            MachineTitle      = $movement.machineTitle
            MovementType      = $movement.movementType
            MovementUtc       = $movement.movementUtc
            QuantityDelta     = $movement.quantityDelta
            Notes             = $movement.notes
        }

        Upsert-ListItem -ListTitle $script:Lists.Movements -KeyField 'MovementReference' -KeyValue $movement.movementReference -Values $values
    }

    Write-Step "Synced $($movements.Count) movement rows."
}

function Sync-KnowledgeFiles {
    Ensure-List -Title $script:KnowledgeLibrary -Template DocumentLibrary | Out-Null

    $files = @(
        'knowledge/inventory-catalog.md',
        'knowledge/inventory-machine-briefs.md',
        'knowledge/inventory-flow-data-dictionary.md',
        'knowledge/repair-playbook.md',
        'knowledge/warranty-and-services.md',
        'knowledge/pinball-history-research.md',
        'data/inventory-machines.seed.json',
        'data/inventory-holds.seed.json',
        'data/inventory-movements.seed.json'
    )

    foreach ($relativePath in $files) {
        $filePath = Resolve-AssetPath -RelativePath $relativePath
        if ($PSCmdlet.ShouldProcess("$script:KnowledgeLibrary/$([IO.Path]::GetFileName($filePath))", 'Upload knowledge asset')) {
            Add-PnPFile -Path $filePath -Folder $script:KnowledgeLibrary -Values @{
                Title = [IO.Path]::GetFileNameWithoutExtension($filePath)
            } | Out-Null
        }
    }

    Write-Step "Uploaded $($files.Count) knowledge/data files."
}

function Show-DeploymentSummary {
    param([Parameter(Mandatory)][string] $SiteUrl)

    Write-Host ''
    Write-Host 'Deployment summary'
    Write-Host '------------------'
    Write-Host "Site:              $SiteUrl"
    Write-Host "Knowledge library: $script:KnowledgeLibrary"
    Write-Host "Lists:"
    Write-Host "  - $($script:Lists.Machines)"
    Write-Host "  - $($script:Lists.Holds)"
    Write-Host "  - $($script:Lists.Movements)"
    Write-Host ''
    Write-Host 'Use the list "CPG Inventory Machines" as the Inventory Lookup flow source.'
}

$adminUrl = "https://$TenantName-admin.sharepoint.com"
$siteUrl = "https://$TenantName.sharepoint.com/sites/$SiteAlias"

Write-Step "Project root: $ProjectRoot"
Write-Step "Tenant admin URL: $adminUrl"
Write-Step "Target site URL: $siteUrl"

$null = Resolve-AssetPath -RelativePath 'data/inventory-machines.seed.json'
$null = Resolve-AssetPath -RelativePath 'data/inventory-holds.seed.json'
$null = Resolve-AssetPath -RelativePath 'data/inventory-movements.seed.json'

if ($DryRun) {
    Write-Step 'Dry run complete. Local assets exist; no Microsoft 365 writes were attempted.'
    Show-DeploymentSummary -SiteUrl $siteUrl
    return
}

Assert-Module
Ensure-ContosoSite -AdminUrl $adminUrl -SiteUrl $siteUrl
Connect-ContosoPnP -Url $siteUrl
Ensure-InventorySchema
Sync-MachineRows
Sync-HoldRows
Sync-MovementRows
Sync-KnowledgeFiles
Show-DeploymentSummary -SiteUrl $siteUrl

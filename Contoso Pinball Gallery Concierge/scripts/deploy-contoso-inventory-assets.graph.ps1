<#
.SYNOPSIS
    Deploys Contoso Pinball Gallery inventory assets to an existing SharePoint site using Microsoft Graph.

.DESCRIPTION
    Uses Microsoft Graph PowerShell delegated authentication to create or update
    SharePoint lists, list columns, list rows, a knowledge folder, and uploaded
    knowledge files for the Contoso Pinball Gallery Concierge.

    This script is idempotent. It uses stable business keys such as SKU,
    HoldReference, and MovementReference to update existing list items.

.PARAMETER SharePointHost
    SharePoint host name, for example timwinfo2.sharepoint.com.

.PARAMETER SitePath
    Server-relative site path, for example /sites/CERTSTAR.NET.

.PARAMETER ProjectRoot
    Path to the Contoso Pinball Gallery Concierge project folder.

.PARAMETER TenantId
    Microsoft Entra tenant ID.

.PARAMETER GraphScopes
    Microsoft Graph delegated scopes used for the deployment.

.PARAMETER UseDeviceCode
    Uses device-code authentication for Microsoft Graph PowerShell.

.PARAMETER DryRun
    Validates local files and resolves the target site without writing.

.EXAMPLE
    pwsh .\scripts\deploy-contoso-inventory-assets.graph.ps1 `
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
    [string] $ProjectRoot = (Split-Path -Parent (Split-Path -Parent $PSCommandPath)),

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string] $TenantId = 'f74b1450-e46a-41df-abee-ebf3621bfd85',

    [Parameter()]
    [ValidateNotNullOrEmpty()]
    [string[]] $GraphScopes = @('Sites.ReadWrite.All', 'Files.ReadWrite.All'),

    [Parameter()]
    [switch] $UseDeviceCode,

    [Parameter()]
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:GraphRoot = 'https://graph.microsoft.com/v1.0'
$script:Lists = @{
    Machines  = 'CPG Inventory Machines'
    Holds     = 'CPG Inventory Holds'
    Movements = 'CPG Inventory Movements'
}
$script:KnowledgeFolder = 'Concierge Knowledge'

function Write-Step {
    param([Parameter(Mandatory)][string] $Message)
    Write-Host "[contoso-inventory-graph] $Message"
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

function Connect-Graph {
    if (-not (Get-Module -ListAvailable -Name Microsoft.Graph.Authentication)) {
        throw "Microsoft.Graph.Authentication is required. Install it with: Install-Module Microsoft.Graph.Authentication -Scope CurrentUser"
    }

    Import-Module Microsoft.Graph.Authentication -ErrorAction Stop

    $connectArgs = @{
        TenantId     = $TenantId
        Scopes       = $GraphScopes
        ContextScope = 'CurrentUser'
        NoWelcome    = $true
    }

    if ($UseDeviceCode) {
        $connectArgs.UseDeviceCode = $true
    }

    Write-Step "Connecting to Microsoft Graph with scopes: $($GraphScopes -join ', ')"
    Connect-MgGraph @connectArgs | Out-Null

    $context = Get-MgContext
    if (-not $context) {
        throw "Microsoft Graph authentication did not return a context."
    }

    $missingScopes = @($GraphScopes | Where-Object { $_ -notin $context.Scopes })
    if ($missingScopes.Count -gt 0) {
        throw "Microsoft Graph context is missing required scopes: $($missingScopes -join ', '). Run Connect-MgGraph with those scopes and retry."
    }

    Write-Step "Graph context: $($context.Account) / tenant $($context.TenantId)"
    Write-Step "Graph scopes: $($context.Scopes -join ', ')"
}

function Invoke-Graph {
    param(
        [Parameter(Mandatory)][ValidateSet('GET', 'POST', 'PATCH', 'PUT')]
        [string] $Method,

        [Parameter(Mandatory)][string] $Uri,

        [Parameter()][object] $Body,

        [Parameter()][string] $ContentType = 'application/json'
    )

    $args = @{
        Method      = $Method
        Uri         = $Uri
        ErrorAction = 'Stop'
    }

    if ($null -ne $Body) {
        if ($Body -is [string]) {
            $args.Body = $Body
        }
        else {
            $args.Body = $Body | ConvertTo-Json -Depth 20
        }
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

function Get-Site {
    $encodedPath = $SitePath.TrimEnd('/')
    $uri = "$script:GraphRoot/sites/$SharePointHost`:$encodedPath`?`$select=id,displayName,webUrl"
    return Invoke-Graph -Method GET -Uri $uri
}

function Get-ListMap {
    param([Parameter(Mandatory)][string] $SiteId)

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $uri = "$script:GraphRoot/sites/$encodedSiteId/lists?`$select=id,displayName,webUrl"
    $response = Invoke-Graph -Method GET -Uri $uri

    $map = @{}
    foreach ($list in $response.value) {
        $map[$list.displayName] = $list
    }
    return $map
}

function New-ColumnDefinition {
    param(
        [Parameter(Mandatory)][string] $Name,
        [Parameter(Mandatory)][string] $DisplayName,
        [Parameter(Mandatory)][ValidateSet('text', 'note', 'number', 'currency', 'choice', 'boolean', 'dateTime')]
        [string] $Type,
        [Parameter()][string[]] $Choices
    )

    $column = @{
        name        = $Name
        displayName = $DisplayName
    }

    switch ($Type) {
        'text' {
            $column.text = @{}
        }
        'note' {
            # Multiple-line text keeps sales guidance in the row without requiring a second list.
            $column.text = @{
                allowMultipleLines = $true
                linesForEditing    = 6
            }
        }
        'number' {
            $column.number = @{
                decimalPlaces = 'none'
            }
        }
        'currency' {
            $column.currency = @{
                locale = 'en-US'
            }
        }
        'choice' {
            $column.choice = @{
                displayAs = 'dropDownMenu'
                choices   = $Choices
            }
        }
        'boolean' {
            $column.boolean = @{}
        }
        'dateTime' {
            $column.dateTime = @{
                displayAs = 'default'
                format    = 'dateTime'
            }
        }
    }

    return $column
}

function Ensure-GraphList {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $DisplayName,
        [Parameter(Mandatory)][object[]] $Columns
    )

    $listMap = Get-ListMap -SiteId $SiteId
    if ($listMap.ContainsKey($DisplayName)) {
        Write-Step "List exists: $DisplayName"
        return $listMap[$DisplayName]
    }

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $body = @{
        displayName = $DisplayName
        columns     = $Columns
        list        = @{
            template = 'genericList'
        }
    }

    if ($PSCmdlet.ShouldProcess($DisplayName, 'Create SharePoint list via Graph')) {
        Write-Step "Creating list: $DisplayName"
        return Invoke-Graph -Method POST -Uri "$script:GraphRoot/sites/$encodedSiteId/lists" -Body $body
    }
}

function Ensure-InventoryLists {
    param([Parameter(Mandatory)][string] $SiteId)

    $machineColumns = @(
        New-ColumnDefinition -Name 'SKU' -DisplayName 'SKU' -Type text
        New-ColumnDefinition -Name 'Manufacturer' -DisplayName 'Manufacturer' -Type text
        New-ColumnDefinition -Name 'ModelYear' -DisplayName 'Model Year' -Type number
        New-ColumnDefinition -Name 'Era' -DisplayName 'Era' -Type text
        New-ColumnDefinition -Name 'ConditionGrade' -DisplayName 'Condition Grade' -Type choice -Choices @('Museum', 'Excellent', 'Very Good', 'Good', 'Project')
        New-ColumnDefinition -Name 'PriceUsd' -DisplayName 'Price USD' -Type currency
        New-ColumnDefinition -Name 'Availability' -DisplayName 'Availability' -Type choice -Choices @('In stock', 'On hold', 'Sold - waitlist open', 'On order')
        New-ColumnDefinition -Name 'Location' -DisplayName 'Location' -Type text
        New-ColumnDefinition -Name 'SerialNumber' -DisplayName 'Serial Number' -Type text
        New-ColumnDefinition -Name 'WarrantyDays' -DisplayName 'Warranty Days' -Type number
        New-ColumnDefinition -Name 'HoldExpiresUtc' -DisplayName 'Hold Expires UTC' -Type dateTime
        New-ColumnDefinition -Name 'Featured' -DisplayName 'Featured' -Type boolean
        New-ColumnDefinition -Name 'Tags' -DisplayName 'Tags' -Type text
        New-ColumnDefinition -Name 'Notes' -DisplayName 'Notes' -Type note
        New-ColumnDefinition -Name 'ServiceStatus' -DisplayName 'Service Status' -Type text
        New-ColumnDefinition -Name 'SourceDocument' -DisplayName 'Source Document' -Type text
    )

    $holdColumns = @(
        New-ColumnDefinition -Name 'HoldReference' -DisplayName 'Hold Reference' -Type text
        New-ColumnDefinition -Name 'SKU' -DisplayName 'SKU' -Type text
        New-ColumnDefinition -Name 'MachineTitle' -DisplayName 'Machine Title' -Type text
        New-ColumnDefinition -Name 'ContactName' -DisplayName 'Contact Name' -Type text
        New-ColumnDefinition -Name 'ContactEmail' -DisplayName 'Contact Email' -Type text
        New-ColumnDefinition -Name 'Status' -DisplayName 'Status' -Type choice -Choices @('Pending deposit', 'Active', 'Released', 'Expired', 'Converted')
        New-ColumnDefinition -Name 'ExpiresUtc' -DisplayName 'Expires UTC' -Type dateTime
        New-ColumnDefinition -Name 'Notes' -DisplayName 'Notes' -Type note
    )

    $movementColumns = @(
        New-ColumnDefinition -Name 'MovementReference' -DisplayName 'Movement Reference' -Type text
        New-ColumnDefinition -Name 'SKU' -DisplayName 'SKU' -Type text
        New-ColumnDefinition -Name 'MachineTitle' -DisplayName 'Machine Title' -Type text
        New-ColumnDefinition -Name 'MovementType' -DisplayName 'Movement Type' -Type choice -Choices @('New arrival', 'Hold placed', 'Hold released', 'Sold', 'Restoration complete', 'Price update')
        New-ColumnDefinition -Name 'MovementUtc' -DisplayName 'Movement UTC' -Type dateTime
        New-ColumnDefinition -Name 'QuantityDelta' -DisplayName 'Quantity Delta' -Type number
        New-ColumnDefinition -Name 'Notes' -DisplayName 'Notes' -Type note
    )

    @{
        Machines  = Ensure-GraphList -SiteId $SiteId -DisplayName $script:Lists.Machines -Columns $machineColumns
        Holds     = Ensure-GraphList -SiteId $SiteId -DisplayName $script:Lists.Holds -Columns $holdColumns
        Movements = Ensure-GraphList -SiteId $SiteId -DisplayName $script:Lists.Movements -Columns $movementColumns
    }
}

function ConvertTo-FieldValue {
    param([object] $Value)

    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [System.Array]) {
        return ($Value -join '; ')
    }

    return $Value
}

function Get-ExistingItemMap {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $ListId,
        [Parameter(Mandatory)][string] $KeyField
    )

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $uri = "$script:GraphRoot/sites/$encodedSiteId/lists/$ListId/items?expand=fields&`$top=200"
    $response = Invoke-Graph -Method GET -Uri $uri

    $map = @{}
    foreach ($item in $response.value) {
        $key = $item.fields.$KeyField
        if (-not [string]::IsNullOrWhiteSpace($key)) {
            $map[$key] = $item
        }
    }
    return $map
}

function Upsert-GraphListItem {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $ListId,
        [Parameter(Mandatory)][hashtable] $ExistingItems,
        [Parameter(Mandatory)][string] $KeyValue,
        [Parameter(Mandatory)][hashtable] $Fields
    )

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    if ($ExistingItems.ContainsKey($KeyValue)) {
        $itemId = $ExistingItems[$KeyValue].id
        if ($PSCmdlet.ShouldProcess("$ListId/$KeyValue", 'Update list item via Graph')) {
            Invoke-Graph -Method PATCH -Uri "$script:GraphRoot/sites/$encodedSiteId/lists/$ListId/items/$itemId/fields" -Body $Fields | Out-Null
        }
        return
    }

    if ($PSCmdlet.ShouldProcess("$ListId/$KeyValue", 'Create list item via Graph')) {
        $created = Invoke-Graph -Method POST -Uri "$script:GraphRoot/sites/$encodedSiteId/lists/$ListId/items" -Body @{ fields = $Fields }
        $ExistingItems[$KeyValue] = $created
    }
}

function Sync-MachineRows {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $ListId
    )

    $machines = Import-SeedJson -RelativePath 'data/inventory-machines.seed.json'
    $existing = Get-ExistingItemMap -SiteId $SiteId -ListId $ListId -KeyField 'SKU'
    foreach ($machine in $machines) {
        $fields = @{
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
            Tags           = ConvertTo-FieldValue -Value $machine.tags
            Notes          = $machine.notes
            ServiceStatus  = $machine.serviceStatus
            SourceDocument = $machine.sourceDocument
        }

        Upsert-GraphListItem -SiteId $SiteId -ListId $ListId -ExistingItems $existing -KeyValue $machine.sku -Fields $fields
    }

    Write-Step "Synced $($machines.Count) machine inventory rows."
}

function Sync-HoldRows {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $ListId
    )

    $holds = Import-SeedJson -RelativePath 'data/inventory-holds.seed.json'
    $existing = Get-ExistingItemMap -SiteId $SiteId -ListId $ListId -KeyField 'HoldReference'
    foreach ($hold in $holds) {
        $fields = @{
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

        Upsert-GraphListItem -SiteId $SiteId -ListId $ListId -ExistingItems $existing -KeyValue $hold.holdReference -Fields $fields
    }

    Write-Step "Synced $($holds.Count) hold rows."
}

function Sync-MovementRows {
    param(
        [Parameter(Mandatory)][string] $SiteId,
        [Parameter(Mandatory)][string] $ListId
    )

    $movements = Import-SeedJson -RelativePath 'data/inventory-movements.seed.json'
    $existing = Get-ExistingItemMap -SiteId $SiteId -ListId $ListId -KeyField 'MovementReference'
    foreach ($movement in $movements) {
        $fields = @{
            Title             = $movement.movementReference
            MovementReference = $movement.movementReference
            SKU               = $movement.sku
            MachineTitle      = $movement.machineTitle
            MovementType      = $movement.movementType
            MovementUtc       = $movement.movementUtc
            QuantityDelta     = $movement.quantityDelta
            Notes             = $movement.notes
        }

        Upsert-GraphListItem -SiteId $SiteId -ListId $ListId -ExistingItems $existing -KeyValue $movement.movementReference -Fields $fields
    }

    Write-Step "Synced $($movements.Count) movement rows."
}

function Ensure-KnowledgeFolder {
    param([Parameter(Mandatory)][string] $SiteId)

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $childrenUri = "$script:GraphRoot/sites/$encodedSiteId/drive/root/children"
    $body = @{
        name                              = $script:KnowledgeFolder
        folder                            = @{}
        '@microsoft.graph.conflictBehavior' = 'replace'
    }

    if ($PSCmdlet.ShouldProcess($script:KnowledgeFolder, 'Create or reuse knowledge folder')) {
        try {
            Invoke-Graph -Method POST -Uri $childrenUri -Body $body | Out-Null
        }
        catch {
            if ($_.Exception.Message -notmatch 'nameAlreadyExists|already exists') {
                throw
            }
        }
    }
}

function Upload-KnowledgeFiles {
    param([Parameter(Mandatory)][string] $SiteId)

    Ensure-KnowledgeFolder -SiteId $SiteId

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

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    foreach ($relativePath in $files) {
        $filePath = Resolve-AssetPath -RelativePath $relativePath
        $fileName = [IO.Path]::GetFileName($filePath)
        $encodedFolder = [Uri]::EscapeDataString($script:KnowledgeFolder).Replace('%20', ' ')
        $encodedFileName = [Uri]::EscapeDataString($fileName).Replace('%20', ' ')
        $uri = "$script:GraphRoot/sites/$encodedSiteId/drive/root:/$encodedFolder/$encodedFileName`:/content"

        if ($PSCmdlet.ShouldProcess("$script:KnowledgeFolder/$fileName", 'Upload knowledge file via Graph')) {
            Invoke-MgGraphRequest -Method PUT -Uri $uri -InputFilePath $filePath -ContentType 'text/plain' | Out-Null
        }
    }

    Write-Step "Uploaded $($files.Count) knowledge/data files."
}

Connect-Graph

Write-Step "Project root: $ProjectRoot"
Write-Step "Target site: https://$SharePointHost$SitePath"
Write-Step "Tenant ID: $TenantId"

$null = Resolve-AssetPath -RelativePath 'data/inventory-machines.seed.json'
$null = Resolve-AssetPath -RelativePath 'data/inventory-holds.seed.json'
$null = Resolve-AssetPath -RelativePath 'data/inventory-movements.seed.json'

$site = Get-Site
Write-Step "Resolved site: $($site.displayName) <$($site.webUrl)>"

if ($DryRun) {
    Write-Step 'Dry run complete. Local assets and target site resolved; no Microsoft 365 writes were attempted.'
    return
}

$lists = Ensure-InventoryLists -SiteId $site.id
Sync-MachineRows -SiteId $site.id -ListId $lists.Machines.id
Sync-HoldRows -SiteId $site.id -ListId $lists.Holds.id
Sync-MovementRows -SiteId $site.id -ListId $lists.Movements.id
Upload-KnowledgeFiles -SiteId $site.id

Write-Host ''
Write-Host 'Deployment summary'
Write-Host '------------------'
Write-Host "Site:             $($site.webUrl)"
Write-Host "Knowledge folder: $script:KnowledgeFolder"
Write-Host "Lists:"
Write-Host "  - $($script:Lists['Machines'])"
Write-Host "  - $($script:Lists['Holds'])"
Write-Host "  - $($script:Lists['Movements'])"

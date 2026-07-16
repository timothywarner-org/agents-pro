<#
.SYNOPSIS
    Deploys SharePoint backing lists for Contoso deterministic workflows.

.DESCRIPTION
    Creates and seeds the SharePoint lists used by the Contoso Pinball Gallery
    Concierge flows that write commitments: service bookings, repair quotes,
    status lookup, trade-ins, and repair intake.

    The script is idempotent. Each list uses a stable reference field as the
    business key, so reruns update existing rows instead of creating duplicates.

.EXAMPLE
    pwsh .\scripts\deploy-contoso-deterministic-workflow-assets.graph.ps1 `
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
    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:GraphRoot = 'https://graph.microsoft.com/v1.0'

function Write-Step([string] $Message) {
    Write-Host "[contoso-deterministic-assets] $Message"
}

function Connect-Graph {
    Import-Module Microsoft.Graph.Authentication -ErrorAction Stop
    $context = Get-MgContext
    $missingScopes = @()
    if ($context) {
        $missingScopes = @($GraphScopes | Where-Object { $_ -notin $context.Scopes })
    }

    if (-not $context -or $context.TenantId -ne $TenantId -or $missingScopes.Count -gt 0) {
        Connect-MgGraph -TenantId $TenantId -Scopes $GraphScopes -ContextScope CurrentUser -NoWelcome | Out-Null
        $context = Get-MgContext
    }

    if (-not $context) {
        throw 'Microsoft Graph authentication did not return a context.'
    }

    $missingScopes = @($GraphScopes | Where-Object { $_ -notin $context.Scopes })
    if ($missingScopes.Count -gt 0) {
        throw "Microsoft Graph context is missing required scopes: $($missingScopes -join ', ')."
    }

    Write-Step "Graph context: $($context.Account) / tenant $($context.TenantId)"
}

function Invoke-Graph {
    param(
        [Parameter(Mandatory)][ValidateSet('GET', 'POST', 'PATCH')]
        [string] $Method,
        [Parameter(Mandatory)][string] $Uri,
        [Parameter()][object] $Body
    )

    $args = @{
        Method      = $Method
        Uri         = $Uri
        ErrorAction = 'Stop'
    }

    if ($null -ne $Body) {
        $args.Body = $Body | ConvertTo-Json -Depth 20
        $args.ContentType = 'application/json'
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
    $uri = "$script:GraphRoot/sites/$SharePointHost`:$SitePath`?`$select=id,displayName,webUrl"
    Invoke-Graph -Method GET -Uri $uri
}

function Import-Seed([string] $RelativePath) {
    $path = Join-Path $ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required seed file not found: $path"
    }
    Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
}

function New-Column([string] $Name, [string] $DisplayName, [string] $Type, [string[]] $Choices = @()) {
    $column = @{
        name        = $Name
        displayName = $DisplayName
    }

    switch ($Type) {
        'text' { $column.text = @{} }
        'note' { $column.text = @{ allowMultipleLines = $true; linesForEditing = 6 } }
        'number' { $column.number = @{ decimalPlaces = 'none' } }
        'boolean' { $column.boolean = @{} }
        'dateTime' { $column.dateTime = @{ displayAs = 'default'; format = 'dateTime' } }
        'choice' { $column.choice = @{ displayAs = 'dropDownMenu'; choices = $Choices } }
        default { throw "Unsupported column type: $Type" }
    }

    $column
}

function Get-ListMap([string] $SiteId) {
    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    $response = Invoke-Graph -Method GET -Uri "$script:GraphRoot/sites/$encodedSiteId/lists?`$select=id,displayName,webUrl"
    $map = @{}
    foreach ($list in $response.value) {
        $map[$list.displayName] = $list
    }
    $map
}

function Ensure-List([string] $SiteId, [string] $DisplayName, [object[]] $Columns) {
    $map = Get-ListMap -SiteId $SiteId
    if ($map.ContainsKey($DisplayName)) {
        Write-Step "List exists: $DisplayName"
        return $map[$DisplayName]
    }

    if ($DryRun) {
        Write-Step "Would create list: $DisplayName"
        return [pscustomobject]@{ id = "dryrun-$DisplayName"; displayName = $DisplayName }
    }

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    Write-Step "Creating list: $DisplayName"
    Invoke-Graph -Method POST -Uri "$script:GraphRoot/sites/$encodedSiteId/lists" -Body @{
        displayName = $DisplayName
        columns     = $Columns
        list        = @{ template = 'genericList' }
    }
}

function Get-ExistingItemMap([string] $SiteId, [string] $ListId, [string] $KeyField) {
    if ($ListId -like 'dryrun-*') {
        return @{}
    }

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
    $map
}

function Upsert-Item([string] $SiteId, [string] $ListId, [hashtable] $Existing, [string] $KeyValue, [hashtable] $Fields) {
    if ($DryRun) {
        Write-Step "Would upsert item: $KeyValue"
        return
    }

    $encodedSiteId = [Uri]::EscapeDataString($SiteId)
    if ($Existing.ContainsKey($KeyValue)) {
        $itemId = $Existing[$KeyValue].id
        Invoke-Graph -Method PATCH -Uri "$script:GraphRoot/sites/$encodedSiteId/lists/$ListId/items/$itemId/fields" -Body $Fields | Out-Null
        return
    }

    $created = Invoke-Graph -Method POST -Uri "$script:GraphRoot/sites/$encodedSiteId/lists/$ListId/items" -Body @{ fields = $Fields }
    $Existing[$KeyValue] = $created
}

function Sync-ServiceBookings([string] $SiteId, [string] $ListId) {
    $rows = Import-Seed 'data/service-bookings.seed.json'
    $existing = Get-ExistingItemMap $SiteId $ListId 'BookingReference'
    foreach ($row in $rows) {
        Upsert-Item $SiteId $ListId $existing $row.bookingReference @{
            Title             = $row.bookingReference
            BookingReference  = $row.bookingReference
            MachineTitle      = $row.machineTitle
            Symptom           = $row.symptom
            PreferredWindow   = $row.preferredWindow
            ContactEmail      = $row.contactEmail
            ConfirmedWindow   = $row.confirmedWindow
            Status            = $row.status
            ApprovalStatus    = $row.approvalStatus
            Technician        = $row.technician
            ScheduledStartUtc = $row.scheduledStartUtc
            LastUpdatedUtc    = $row.lastUpdatedUtc
            Notes             = $row.notes
        }
    }
    Write-Step "Synced $($rows.Count) service booking rows."
}

function Sync-RepairQuotes([string] $SiteId, [string] $ListId) {
    $rows = Import-Seed 'data/repair-quotes.seed.json'
    $existing = Get-ExistingItemMap $SiteId $ListId 'QuoteReference'
    foreach ($row in $rows) {
        Upsert-Item $SiteId $ListId $existing $row.quoteReference @{
            Title          = $row.quoteReference
            QuoteReference = $row.quoteReference
            MachineTitle   = $row.machineTitle
            Symptom        = $row.symptom
            Tier           = $row.tier
            PriceBand      = $row.priceBand
            Turnaround     = $row.turnaround
            Status         = $row.status
            ContactEmail   = $row.contactEmail
            ExpiresUtc     = $row.expiresUtc
            LastUpdatedUtc = $row.lastUpdatedUtc
            Notes          = $row.notes
        }
    }
    Write-Step "Synced $($rows.Count) repair quote rows."
}

function Sync-StatusLookup([string] $SiteId, [string] $ListId) {
    $rows = Import-Seed 'data/status-lookup.seed.json'
    $existing = Get-ExistingItemMap $SiteId $ListId 'ReferenceNumber'
    foreach ($row in $rows) {
        Upsert-Item $SiteId $ListId $existing $row.referenceNumber @{
            Title           = $row.referenceNumber
            ReferenceNumber = $row.referenceNumber
            ReferenceType   = $row.referenceType
            Status          = $row.status
            LastUpdatedUtc  = $row.lastUpdatedUtc
            SourceList      = $row.sourceList
            CustomerMessage = $row.customerMessage
            Notes           = $row.notes
        }
    }
    Write-Step "Synced $($rows.Count) status lookup rows."
}

function Sync-TradeIns([string] $SiteId, [string] $ListId) {
    $rows = Import-Seed 'data/trade-ins.seed.json'
    $existing = Get-ExistingItemMap $SiteId $ListId 'TradeInReference'
    foreach ($row in $rows) {
        Upsert-Item $SiteId $ListId $existing $row.tradeInReference @{
            Title                    = $row.tradeInReference
            TradeInReference         = $row.tradeInReference
            MachineTitle             = $row.machineTitle
            Era                      = $row.era
            ConditionSelfGrade       = $row.conditionSelfGrade
            ContactEmail             = $row.contactEmail
            EstimateBand             = $row.estimateBand
            Status                   = $row.status
            SpecialistReviewRequired = [bool] $row.specialistReviewRequired
            LastUpdatedUtc           = $row.lastUpdatedUtc
            Notes                    = $row.notes
        }
    }
    Write-Step "Synced $($rows.Count) trade-in rows."
}

function Sync-RepairIntake([string] $SiteId, [string] $ListId) {
    $rows = Import-Seed 'data/repair-intake.seed.json'
    $existing = Get-ExistingItemMap $SiteId $ListId 'IntakeReference'
    foreach ($row in $rows) {
        Upsert-Item $SiteId $ListId $existing $row.intakeReference @{
            Title            = $row.intakeReference
            IntakeReference  = $row.intakeReference
            Source           = $row.source
            MachineTitle     = $row.machineTitle
            Symptom          = $row.symptom
            ContactEmail     = $row.contactEmail
            Priority         = $row.priority
            ProcessingStatus = $row.processingStatus
            CreatedUtc       = $row.createdUtc
            FileUrl          = $row.fileUrl
            Notes            = $row.notes
        }
    }
    Write-Step "Synced $($rows.Count) repair intake rows."
}

Connect-Graph
$site = Get-Site
Write-Step "Resolved site: $($site.displayName) <$($site.webUrl)>"

$bookingList = Ensure-List $site.id 'CPG Service Bookings' @(
    New-Column 'BookingReference' 'Booking Reference' text
    New-Column 'MachineTitle' 'Machine Title' text
    New-Column 'Symptom' 'Symptom' note
    New-Column 'PreferredWindow' 'Preferred Window' choice @('this week', 'next week', 'weekend')
    New-Column 'ContactEmail' 'Contact Email' text
    New-Column 'ConfirmedWindow' 'Confirmed Window' text
    New-Column 'Status' 'Status' choice @('Booked', 'Awaiting approval', 'Completed', 'Cancelled')
    New-Column 'ApprovalStatus' 'Approval Status' choice @('Pending', 'Approved', 'Rejected', 'Not required')
    New-Column 'Technician' 'Technician' text
    New-Column 'ScheduledStartUtc' 'Scheduled Start UTC' dateTime
    New-Column 'LastUpdatedUtc' 'Last Updated UTC' dateTime
    New-Column 'Notes' 'Notes' note
)

$quoteList = Ensure-List $site.id 'CPG Repair Quotes' @(
    New-Column 'QuoteReference' 'Quote Reference' text
    New-Column 'MachineTitle' 'Machine Title' text
    New-Column 'Symptom' 'Symptom' note
    New-Column 'Tier' 'Tier' choice @('Diagnostic', 'Standard', 'Premium', 'Restoration', 'Priority')
    New-Column 'PriceBand' 'Price Band' text
    New-Column 'Turnaround' 'Turnaround' text
    New-Column 'Status' 'Status' choice @('Open', 'Specialist review', 'Accepted', 'Expired', 'Closed')
    New-Column 'ContactEmail' 'Contact Email' text
    New-Column 'ExpiresUtc' 'Expires UTC' dateTime
    New-Column 'LastUpdatedUtc' 'Last Updated UTC' dateTime
    New-Column 'Notes' 'Notes' note
)

$statusList = Ensure-List $site.id 'CPG Status Lookup' @(
    New-Column 'ReferenceNumber' 'Reference Number' text
    New-Column 'ReferenceType' 'Reference Type' choice @('Service booking', 'Repair quote', 'Inventory hold', 'Trade-in', 'Order')
    New-Column 'Status' 'Status' text
    New-Column 'LastUpdatedUtc' 'Last Updated UTC' dateTime
    New-Column 'SourceList' 'Source List' text
    New-Column 'CustomerMessage' 'Customer Message' note
    New-Column 'Notes' 'Notes' note
)

$tradeInList = Ensure-List $site.id 'CPG Trade Ins' @(
    New-Column 'TradeInReference' 'Trade-In Reference' text
    New-Column 'MachineTitle' 'Machine Title' text
    New-Column 'Era' 'Era' text
    New-Column 'ConditionSelfGrade' 'Condition Self Grade' choice @('Museum', 'Excellent', 'Very Good', 'Good', 'Project')
    New-Column 'ContactEmail' 'Contact Email' text
    New-Column 'EstimateBand' 'Estimate Band' text
    New-Column 'Status' 'Status' choice @('Specialist review', 'Awaiting photos', 'Offer ready', 'Closed')
    New-Column 'SpecialistReviewRequired' 'Specialist Review Required' boolean
    New-Column 'LastUpdatedUtc' 'Last Updated UTC' dateTime
    New-Column 'Notes' 'Notes' note
)

$intakeList = Ensure-List $site.id 'CPG Repair Intake' @(
    New-Column 'IntakeReference' 'Intake Reference' text
    New-Column 'Source' 'Source' choice @('SharePoint form', 'Email attachment', 'Manual entry')
    New-Column 'MachineTitle' 'Machine Title' text
    New-Column 'Symptom' 'Symptom' note
    New-Column 'ContactEmail' 'Contact Email' text
    New-Column 'Priority' 'Priority' choice @('Normal', 'Priority', 'Emergency')
    New-Column 'ProcessingStatus' 'Processing Status' choice @('Ready for agent review', 'Needs triage', 'Processed', 'Exception')
    New-Column 'CreatedUtc' 'Created UTC' dateTime
    New-Column 'FileUrl' 'File URL' text
    New-Column 'Notes' 'Notes' note
)

Sync-ServiceBookings $site.id $bookingList.id
Sync-RepairQuotes $site.id $quoteList.id
Sync-StatusLookup $site.id $statusList.id
Sync-TradeIns $site.id $tradeInList.id
Sync-RepairIntake $site.id $intakeList.id

Write-Host ''
Write-Host 'Deterministic workflow asset deployment summary'
Write-Host '-----------------------------------------------'
Write-Host "Site: $($site.webUrl)"
Write-Host 'Lists: CPG Service Bookings, CPG Repair Quotes, CPG Status Lookup, CPG Trade Ins, CPG Repair Intake'

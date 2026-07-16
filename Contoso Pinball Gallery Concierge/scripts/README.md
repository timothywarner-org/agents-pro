# Contoso Inventory Deployment Scripts

These scripts turn the local **Contoso Pinball Gallery Concierge** inventory pack into real Microsoft 365 assets.

## What Gets Created

The deploy script provisions or updates:

| Asset | Name | Purpose |
|-------|------|---------|
| SharePoint site | `Contoso Pinball Gallery` | Demo site for inventory knowledge and flow data. |
| Document library | `Concierge Knowledge` | Markdown and JSON files used as Copilot Studio knowledge sources. |
| SharePoint list | `CPG Inventory Machines` | Transactional source for the **Inventory Lookup** flow. |
| SharePoint list | `CPG Inventory Holds` | Backing store for the **Reserve / Hold a Machine** flow. |
| SharePoint list | `CPG Inventory Movements` | Lightweight audit history for inventory changes. |
| SharePoint list | `CPG Service Bookings` | Backing store for **Book a Service Visit**. |
| SharePoint list | `CPG Repair Quotes` | Backing store for **Request a Repair Quote**. |
| SharePoint list | `CPG Status Lookup` | Read model for **Check Order or Service Status**. |
| SharePoint list | `CPG Trade Ins` | Backing store for **Trade-In Valuation Start**. |
| SharePoint list | `CPG Repair Intake` | Trigger source for autonomous repair-intake demos. |

## First Run

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -OwnerEmail admin@techtrainertim.com
```

If your PnP.PowerShell setup requires a custom Entra application, pass its app ID:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -OwnerEmail admin@techtrainertim.com `
  -ClientId "00000000-0000-0000-0000-000000000000"
```

For terminal-only sessions, use device-code auth:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -OwnerEmail admin@techtrainertim.com `
  -DeviceLogin
```

If Windows already has the admin identity signed in, use brokered Windows auth:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -OwnerEmail admin@techtrainertim.com `
  -OSLogin
```

If Azure CLI is already signed in, use token-based auth:

```powershell
az account show

pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -OwnerEmail admin@techtrainertim.com `
  -UseAzureCliToken
```

## Dry Run

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.ps1" `
  -TenantName techtrainertim `
  -DryRun
```

## Graph PowerShell Deployment

If PnP site/list writes are blocked, deploy to an existing SharePoint site through Microsoft Graph PowerShell:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-inventory-assets.graph.ps1" `
  -SharePointHost timwinfo2.sharepoint.com `
  -SitePath /sites/CERTSTAR.NET `
  -UseDeviceCode
```

This path requests delegated Graph scopes `Sites.ReadWrite.All` and `Files.ReadWrite.All` through `Connect-MgGraph`. Use this instead of Azure CLI scoped Graph tokens when Azure CLI reports `AADSTS650057` for the `mcp-azure-server` client app.

## Deterministic Workflow Lists

Deploy the non-inventory workflow lists with:

```powershell
pwsh ".\Contoso Pinball Gallery Concierge\scripts\deploy-contoso-deterministic-workflow-assets.graph.ps1" `
  -SharePointHost timwinfo2.sharepoint.com `
  -SitePath /sites/CERTSTAR.NET
```

The schema and flow contracts are documented in:

```text
docs/deterministic-workflow-sharepoint-contracts.md
```

## Inventory Lookup Flow Binding

Point the Power Automate **Inventory Lookup** flow at the SharePoint list:

| Flow setting | Value |
|--------------|-------|
| Site Address | `https://techtrainertim.sharepoint.com/sites/ContosoPinballGallery` |
| List Name | `CPG Inventory Machines` |
| Primary key | `SKU` |
| Fallback lookup | `Title` contains the requested machine name |

Recommended SharePoint **Get items** filter when the user provides a SKU:

```text
SKU eq '@{triggerBody()?['SKU']}'
```

Recommended fallback filter when the user provides a title:

```text
substringof('@{triggerBody()?['MachineTitle']}', Title)
```

Return the list fields directly to the agent. Do not let the flow or the agent invent price or availability. The Van Halen brown sound is allowed; brown data is not.

# Azure MCP Server Setup

## Overview

The Azure MCP server provides direct access to Azure services through structured tools, enabling richer data access than CLI commands alone.

## Configuration

Add to your MCP configuration (`.mcp.json` or settings):

```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"],
      "env": {}
    }
  }
}
```

## Authentication

The Azure MCP server uses Azure CLI credentials by default.

### Login First

```bash
# Interactive login
az login

# Device code flow (headless/remote)
az login --use-device-code

# Set subscription
az account set --subscription "Subscription Name"
```

### Service Principal (CI/CD)

Set environment variables:
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`

## Enabling the MCP Server

### In Claude Code

1. Run `/mcp` to view MCP servers
2. Enable the Azure MCP server
3. Or run `/azure:setup` for guided configuration

### Verify Connection

After enabling, verify tools are available:
- Check `/azure:status`
- Try `azure_subscription_list` to list subscriptions

## Benefits Over CLI

| Feature | MCP Server | CLI |
|---------|------------|-----|
| Structured data | JSON responses | Text parsing needed |
| Pagination | Automatic | Manual continuation |
| Schema info | Built-in | Separate queries |
| Authentication | Managed | Manual |

## Available Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| Subscriptions | `azure_subscription_list` | List subscriptions |
| Resource Groups | `azure_resource_group_list` | List resource groups |
| Storage | `azure_storage_*` | Blob, container operations |
| SQL | `azure_sql_*` | Database management |
| Cosmos DB | `azure_cosmosdb_*` | NoSQL operations |
| Key Vault | `azure_keyvault_*` | Secrets management |
| Compute | `azure_appservice_*`, `azure_function_*`, `azure_aks_*` | Compute resources |
| AI | `azure_search_*`, `azure_speech_*`, `azure_foundry_*` | AI services |
| CLI | `azure__extension_cli_install`, `azure__extension_cli_generate` | CLI helpers |

## Troubleshooting

### Server Not Starting

1. Ensure Node.js 18+ is installed
2. Check npx is available
3. Verify network access to npm registry

### Authentication Errors

1. Run `az login` to refresh credentials
2. Check subscription is set: `az account show`
3. Verify permissions on target resources

### Tool Not Available

1. Enable the Azure MCP server first
2. Check server is connected in `/mcp`
3. Some tools require specific permissions

## Fallback to CLI

When MCP is unavailable, use Azure CLI directly:

```bash
# List subscriptions
az account list --output table

# List resources
az resource list -g RESOURCE_GROUP --output table
```

See `cli/cheatsheet.md` for common CLI commands.

# Azure Compute Services

## MANDATORY: Use azd for All Deployments

> **DO NOT use `az` CLI commands like `az containerapp create`, `az webapp up`, etc.**
> **ALWAYS use `azd up` for deployments.**
> Only use `az` for deployments if the user explicitly requests it.

```bash
# Deploy everything - THIS IS THE ONLY WAY
azd up

# Clean up test environments
azd down --force --purge
```

**Why azd is mandatory:**
- **Parallel provisioning** - deploys in seconds, not minutes
- **Automatic ACR integration** - no image pull failures
- **Single command** - `azd up` replaces 5+ `az` commands
- **Use az for queries only** - `az containerapp show`, `az webapp list`, etc.

## Services

| Service | Use When | azd Template |
|---------|----------|--------------|
| Container Apps | Microservices, APIs, containers | `todo-nodejs-mongo-aca` |
| Azure Functions | Event-driven, serverless | `todo-python-mongo-swa-func` |
| App Service | Traditional web apps | `todo-csharp-sql` |
| AKS | Full Kubernetes control | (use azd with custom Bicep) |

## Quick Deploy

```bash
# 1. Initialize from template
azd init --template azure-samples/todo-nodejs-mongo-aca

# 2. Deploy (provisions + deploys in parallel)
azd up

# 3. Iterate on code changes
azd deploy

# 4. Clean up test environment
azd down --force --purge
```

## Pre-flight Check

**Run `/azure:preflight` before deploying** to verify:
- Tools installed (az, azd, docker)
- Authentication valid
- Quotas sufficient
- Docker running

## MCP Server (For Queries Only)

Use MCP tools to **query** existing resources, not deploy:

- `azure_container_app_list` - List container apps
- `azure_appservice_webapp_list` - List web apps
- `azure_function_app_list` - List function apps
- `azure_aks_cluster_list` - List AKS clusters

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## Choosing the Right Compute

| If your app is... | Use | Why |
|-------------------|-----|-----|
| HTTP APIs, microservices | **Container Apps** | Serverless, auto-scale, Dapr |
| Event-driven | **Functions** | Pay-per-execution |
| Traditional web apps | **App Service** | Managed platform |
| Complex K8s workloads | **AKS** | Full control |

## Service Details

- Container Apps (recommended) -> `services/container-apps.md`
- Azure Functions -> `services/functions.md`
- App Service -> `services/app-service.md`
- AKS -> `services/aks.md`

## Production Configs

- Node.js/Express apps -> `scenarios/nodejs-production.md`

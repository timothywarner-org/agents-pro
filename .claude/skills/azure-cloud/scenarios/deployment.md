# Deploying Applications to Azure

## MANDATORY: Use azd for All Deployments

> **DO NOT use `az` CLI for deployments.** Use `azd` (Azure Developer CLI) instead.
> Only use `az` if the user explicitly requests it.

**Why azd is required:**
- **Faster** - provisions resources in parallel
- **Automatic ACR integration** - no manual credential setup
- **Single command** - `azd up` does everything
- **az is for queries only** - use `az` to inspect resources, not deploy them

```bash
# Full deployment (infrastructure + code)
azd up

# Clean up test environments
azd down --force --purge   # --purge only for test, never production
```

**Why azd over az:**
- Parallel resource provisioning (faster)
- Automatic ACR + Container Apps integration
- Built-in environment management (dev/test/prod)
- Single command cleanup with `azd down`
- Generates CI/CD pipelines

## Pre-flight Checks (CRITICAL)

**Run `/azure:preflight` BEFORE any deployment** to avoid mid-deployment failures.

Check these items:
1. Tools installed (az, azd, docker)
2. Authentication valid
3. Subscription quotas sufficient
4. Docker daemon running (for containers)

## Choose Your Compute

| If your app is... | Use | Template |
|-------------------|-----|----------|
| HTTP APIs, microservices | Container Apps | `todo-nodejs-mongo-aca` |
| Event-driven functions | Azure Functions | `todo-python-mongo-swa-func` |
| Traditional web apps | App Service | `todo-csharp-sql` |

## Quick Deploy with azd

### Step 1: Initialize

```bash
# From template (recommended)
azd init --template azure-samples/todo-nodejs-mongo-aca

# Or existing project
azd init
```

### Step 2: Deploy

```bash
# Provision infrastructure AND deploy code
azd up

# This does everything:
# - Creates resource group
# - Creates ACR and builds image
# - Creates Container Apps environment
# - Configures ACR credentials automatically
# - Deploys your app
```

### Step 3: Iterate

```bash
# Code changes only (faster)
azd deploy

# View what's deployed
azd show
```

### Step 4: Clean Up (Test Environments)

```bash
# Remove everything including soft-deleted resources
azd down --force --purge
```

## ACR + Container Apps Integration

**azd handles this automatically.** If deploying manually, you MUST configure ACR credentials:

### The Problem

When Container Apps and ACR are in the same deployment, Container Apps needs permission to pull images. azd does this automatically, but manual deployments often miss this step.

### Manual Fix (if not using azd)

```bash
# After creating both ACR and Container App:
az containerapp registry set \
  --name APP_NAME \
  --resource-group RG \
  --server ACR_NAME.azurecr.io \
  --identity system
```

Or with admin credentials (less secure):
```bash
# Enable admin on ACR
az acr update --name ACR_NAME --admin-enabled true

# Get credentials
ACR_PASSWORD=$(az acr credential show --name ACR_NAME --query "passwords[0].value" -o tsv)

# Set on Container App
az containerapp registry set \
  --name APP_NAME \
  --resource-group RG \
  --server ACR_NAME.azurecr.io \
  --username ACR_NAME \
  --password $ACR_PASSWORD
```

**Recommendation:** Just use `azd up` - it handles all of this automatically.

## Popular azd Templates

| Template | Stack | Services |
|----------|-------|----------|
| `todo-nodejs-mongo-aca` | Node.js + MongoDB | Container Apps + Cosmos DB |
| `todo-python-mongo-aca` | Python + MongoDB | Container Apps + Cosmos DB |
| `todo-csharp-sql-aca` | .NET + SQL | Container Apps + SQL Database |
| `todo-python-mongo-swa-func` | Python + Functions | Static Web Apps + Functions |

Browse more: https://azure.github.io/awesome-azd/

## Environment Management

```bash
# Create environments for different stages
azd env new dev
azd env new prod

# Switch environments
azd env select prod

# Set environment-specific values
azd env set AZURE_LOCATION westus2
azd env set AZURE_SUBSCRIPTION_ID xxx-xxx-xxx
```

## Deployment Troubleshooting

### Image Pull Failures

**Symptom:** Container App stuck in "Waiting" or "ImagePullBackOff"

**Fix:**
```bash
# Check if ACR credentials are configured
az containerapp show --name APP -g RG --query "properties.configuration.registries"

# If empty, set credentials:
az containerapp registry set --name APP -g RG --server ACR.azurecr.io --identity system
```

### Quota Exceeded

**Symptom:** Deployment fails with quota error

**Fix:**
1. Check quotas: `az quota usage list --scope /subscriptions/SUB_ID/...`
2. Try different region
3. Request quota increase via Azure portal

### Cold Start Issues

**Symptom:** First request very slow or times out

**Fix:**
```bash
# Set minimum replicas
az containerapp update --name APP -g RG --min-replicas 1
```

## Post-Deployment Checklist

- [ ] Verify app is healthy: check `/health` endpoint
- [ ] Check logs for errors: `az containerapp logs show --name APP -g RG`
- [ ] Set up alerts: -> `domains/observability/README.md`
- [ ] Configure custom domain if needed
- [ ] Review security: -> `scenarios/security-hardening.md`

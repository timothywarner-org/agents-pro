# Azure Container Apps

> **MANDATORY: Deploy with `azd up` - DO NOT use `az containerapp create/up`**
> The `az` CLI is for queries only (show, list, logs). Use `azd` for all deployments.

## Quick Reference

| Property | Value |
|----------|-------|
| Deploy with | **`azd up` (MANDATORY)** |
| Query with | `az containerapp show/list/logs` |
| MCP tools | `azure_container_app_list` |
| Best for | Microservices, serverless containers, HTTP APIs |

## Deploy with azd (MANDATORY)

```bash
# Initialize
azd init --template azure-samples/todo-nodejs-mongo-aca

# Deploy (handles ACR, Container Apps, networking automatically)
azd up

# Update code only
azd deploy

# Clean up test environment
azd down --force --purge
```

**azd advantages:**
- Parallel resource provisioning (faster than az)
- Automatic ACR credential configuration
- Integrated environment management
- One-command teardown

## Popular azd Templates

| Template | Stack |
|----------|-------|
| `todo-nodejs-mongo-aca` | Node.js + MongoDB + Container Apps |
| `todo-python-mongo-aca` | Python + MongoDB + Container Apps |
| `todo-csharp-sql-aca` | .NET + SQL + Container Apps |

## ACR Integration (CRITICAL)

**azd handles this automatically.** If you must deploy manually, configure ACR credentials:

```bash
# The problem: Container Apps can't pull from ACR without credentials
# The fix:
az containerapp registry set \
  --name APP \
  --resource-group RG \
  --server ACR.azurecr.io \
  --identity system
```

**Symptom of missing ACR config:** Container stuck in "Waiting" or "ImagePullBackOff"

## Manual Deployment (Only If azd Not Possible)

### Option 1: ACR Build (Cloud Build)

```bash
# Build in the cloud (requires ACR Tasks - may be disabled on free subscriptions)
az acr build --registry ACR --image myapp:v1 .
```

### Option 2: Local Docker Build (Fallback)

**If ACR Tasks is disabled** (common on free/trial subscriptions), build locally:

```bash
# Build locally with Docker
docker build -t ACR.azurecr.io/myapp:v1 .

# Login to ACR
az acr login --name ACR

# Push to ACR
docker push ACR.azurecr.io/myapp:v1
```

**Error pattern to detect:** `ACR Tasks is not supported` or `TasksOperationsNotAllowed`

### Deploy to Container Apps

```bash
# Create Container App
az containerapp up \
  --name myapp \
  --resource-group RG \
  --image ACR.azurecr.io/myapp:v1 \
  --ingress external \
  --target-port 8080

# IMPORTANT: Configure ACR credentials
az containerapp registry set \
  --name myapp \
  --resource-group RG \
  --server ACR.azurecr.io \
  --identity system
```

## Scaling Configuration

### HTTP-Based Scaling

```bash
az containerapp update \
  --name myapp \
  --resource-group RG \
  --min-replicas 1 \
  --max-replicas 10 \
  --scale-rule-name http-rule \
  --scale-rule-type http \
  --scale-rule-http-concurrency 50
```

### Prevent Cold Starts

```bash
# Set minimum replicas to avoid cold start
az containerapp update --name myapp -g RG --min-replicas 1
```

## Environment Variables and Secrets

```bash
# Set environment variable
az containerapp update \
  --name myapp -g RG \
  --set-env-vars KEY=VALUE NODE_ENV=production

# Create secret
az containerapp secret set \
  --name myapp -g RG \
  --secrets dbpassword=secretvalue

# Reference secret in env var
az containerapp update \
  --name myapp -g RG \
  --set-env-vars DB_PASSWORD=secretref:dbpassword
```

## Troubleshooting

### ACR Tasks Disabled (Free Subscriptions)

**Symptom:** `az acr build` fails with "ACR Tasks is not supported" or "TasksOperationsNotAllowed"

**Cause:** Free/trial subscriptions often have ACR Tasks disabled

**Fix: Use local Docker build instead:**
```bash
# Build locally
docker build -t ACR.azurecr.io/myapp:v1 .

# Login to ACR
az acr login --name ACR

# Push
docker push ACR.azurecr.io/myapp:v1
```

### Image Pull Failures

**Symptom:** App stuck in "Waiting" or "ImagePullBackOff"

**Diagnose:**
```bash
# Check if registry is configured
az containerapp show --name APP -g RG --query "properties.configuration.registries"
```

**Fix:**
```bash
az containerapp registry set --name APP -g RG --server ACR.azurecr.io --identity system
```

### Cold Start Timeouts

**Symptom:** First request times out

**Fix:**
```bash
az containerapp update --name APP -g RG --min-replicas 1
```

### Port Mismatch

**Symptom:** App starts but requests fail

**Check:**
```bash
az containerapp show --name APP -g RG --query "properties.configuration.ingress.targetPort"
```

**Fix:** Ensure app listens on the configured port (check Dockerfile EXPOSE)

### View Logs

```bash
# Stream logs
az containerapp logs show --name APP -g RG --follow

# Recent logs
az containerapp logs show --name APP -g RG --tail 100
```

## Health Checks

Configure health probes:

```bash
az containerapp update \
  --name myapp -g RG \
  --health-probe-path /health \
  --health-probe-interval 30 \
  --health-probe-timeout 5
```

Your app should expose a health endpoint:
```javascript
app.get('/health', (req, res) => res.sendStatus(200));
```

## Dapr Integration

Enable Dapr for service-to-service communication:

```bash
az containerapp update \
  --name myapp -g RG \
  --enable-dapr \
  --dapr-app-id myapp \
  --dapr-app-port 8080
```

## Best Practices

1. **Use azd** for all deployments
2. **Run preflight checks** before deploying
3. **Set min-replicas=1** to avoid cold starts in production
4. **Configure health probes** for reliability
5. **Use managed identity** for ACR access
6. **Store secrets in Key Vault** with managed identity

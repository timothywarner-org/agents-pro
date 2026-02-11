# Azure App Service

## Quick Reference

| Property | Value |
|----------|-------|
| CLI prefix | `az webapp` |
| MCP tools | `azure_appservice_webapp_list`, `azure_appservice_webapp_get`, `azure_appservice_plan_list` |
| Best for | Web apps, REST APIs, managed hosting |

## App Service Plans

| Tier | Features | Use Case |
|------|----------|----------|
| Free/Shared | Limited, shared infra | Dev/test |
| Basic | Dedicated, no auto-scale | Small production |
| Standard | Auto-scale, staging slots | Production |
| Premium | Enhanced perf, VNet | High-scale production |
| Isolated | Dedicated environment | Compliance, isolation |

## Deployment Options

### Using azd (Recommended for new apps)

```bash
azd init --template azure-samples/todo-python-mongo-swa-func
azd up
```

### Using CLI

```bash
# Create App Service plan
az appservice plan create \
  --name myplan -g RG \
  --sku S1 --is-linux

# Create web app
az webapp create \
  --name myapp -g RG \
  --plan myplan \
  --runtime "NODE:18-lts"

# Deploy from git
az webapp deployment source config \
  --name myapp -g RG \
  --repo-url REPO_URL \
  --branch main
```

### ZIP Deploy

```bash
az webapp deploy \
  --name myapp -g RG \
  --src-path app.zip \
  --type zip
```

## Deployment Slots

```bash
# Create staging slot
az webapp deployment slot create \
  --name myapp -g RG \
  --slot staging

# Deploy to staging
az webapp deploy \
  --name myapp -g RG \
  --slot staging \
  --src-path app.zip

# Swap slots
az webapp deployment slot swap \
  --name myapp -g RG \
  --slot staging \
  --target-slot production
```

## Configuration

```bash
# Set app settings
az webapp config appsettings set \
  --name myapp -g RG \
  --settings KEY=VALUE

# Set connection string
az webapp config connection-string set \
  --name myapp -g RG \
  --connection-string-type SQLAzure \
  --settings MyDb="connection-string"

# Enable always on
az webapp config set \
  --name myapp -g RG \
  --always-on true
```

## Scaling

### Scale Up (Vertical)

```bash
az appservice plan update \
  --name myplan -g RG \
  --sku P1V2
```

### Scale Out (Horizontal)

```bash
# Manual scale
az appservice plan update \
  --name myplan -g RG \
  --number-of-workers 3

# Auto-scale (configure in portal or ARM)
```

## Best Practices

1. Use deployment slots for zero-downtime deployments
2. Store secrets in Key Vault with managed identity
3. Use App Configuration for feature flags
4. Enable always on for production apps
5. Configure health check endpoint
6. Use staging slot for pre-production testing

## Common Issues

**503 Service Unavailable:**
- Check app logs in Log Stream
- Verify app is starting correctly
- Check memory/CPU usage

**Slow cold starts:**
- Enable always on
- Use Premium tier
- Optimize app startup

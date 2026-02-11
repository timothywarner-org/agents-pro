# Azure CLI Cheatsheet

## Authentication

```bash
# Interactive login
az login

# Device code flow (headless)
az login --use-device-code

# Service principal
az login --service-principal -u APP_ID -p PASSWORD --tenant TENANT_ID

# Check current account
az account show

# List subscriptions
az account list --output table

# Set subscription
az account set --subscription "Subscription Name"
```

## Resource Management

```bash
# List resource groups
az group list --output table

# Create resource group
az group create --name RG --location eastus

# List resources in group
az resource list -g RG --output table

# Delete resource group
az group delete --name RG --yes
```

## Storage

```bash
# List storage accounts
az storage account list --output table

# List containers
az storage container list --account-name ACCOUNT --output table

# List blobs
az storage blob list --account-name ACCOUNT --container-name CONTAINER --output table

# Upload blob
az storage blob upload --account-name ACCOUNT --container-name CONTAINER --name BLOB --file FILE

# Download blob
az storage blob download --account-name ACCOUNT --container-name CONTAINER --name BLOB --file FILE
```

## SQL Database

```bash
# List SQL servers
az sql server list --output table

# List databases
az sql db list --server SERVER -g RG --output table

# Create firewall rule
az sql server firewall-rule create --server SERVER -g RG --name RULE --start-ip-address IP --end-ip-address IP
```

## Key Vault

```bash
# List vaults
az keyvault list --output table

# List secrets
az keyvault secret list --vault-name VAULT --output table

# Get secret
az keyvault secret show --vault-name VAULT --name SECRET

# Set secret
az keyvault secret set --vault-name VAULT --name SECRET --value VALUE
```

## App Service

```bash
# List web apps
az webapp list --output table

# Get app details
az webapp show --name APP -g RG

# Deploy ZIP
az webapp deploy --name APP -g RG --src-path app.zip --type zip

# View logs
az webapp log tail --name APP -g RG
```

## Functions

```bash
# List function apps
az functionapp list --output table

# Get app settings
az functionapp config appsettings list --name APP -g RG

# Set app settings
az functionapp config appsettings set --name APP -g RG --settings KEY=VALUE
```

## Container Apps

```bash
# List container apps
az containerapp list --output table

# Deploy
az containerapp up --name APP -g RG --image IMAGE --ingress external --target-port 8080

# View logs
az containerapp logs show --name APP -g RG --follow
```

## AKS

```bash
# List clusters
az aks list --output table

# Get credentials
az aks get-credentials --name CLUSTER -g RG

# Scale node pool
az aks nodepool scale --cluster-name CLUSTER -g RG --name POOL --node-count 5
```

## Azure Developer CLI (azd)

```bash
# Initialize project
azd init --template TEMPLATE

# Provision and deploy
azd up

# Deploy code only
azd deploy

# Tear down
azd down

# View deployed resources
azd show
```

## Monitoring

```bash
# Query logs
az monitor log-analytics query --workspace WORKSPACE_ID --analytics-query "QUERY"

# List activity log
az monitor activity-log list -g RG --max-events 20
```

## Tips

### Output Formats

```bash
--output table    # Human-readable table
--output json     # Full JSON
--output tsv      # Tab-separated (for scripts)
--query "JMESPATH"  # Filter results
```

### Common Queries

```bash
# Get resource IDs
az resource list -g RG --query "[].id" -o tsv

# Filter by type
az resource list -g RG --query "[?type=='Microsoft.Web/sites']" -o table
```

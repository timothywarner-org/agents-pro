# Azure CLI Tips and Patterns

## Output Formatting

### Table Output (Human Readable)

```bash
az resource list -g RG --output table
```

### JSON Output (Scripting)

```bash
az resource list -g RG --output json
```

### TSV Output (Parsing)

```bash
az resource list -g RG --output tsv
```

### YAML Output

```bash
az resource list -g RG --output yaml
```

## JMESPath Queries

### Select Specific Fields

```bash
az resource list --query "[].{Name:name, Type:type}" -o table
```

### Filter Results

```bash
# Exact match
az resource list --query "[?type=='Microsoft.Web/sites']" -o table

# Contains
az resource list --query "[?contains(name, 'prod')]" -o table

# Multiple conditions
az resource list --query "[?type=='Microsoft.Web/sites' && contains(name, 'api')]" -o table
```

### Get Single Value

```bash
az account show --query "id" -o tsv
```

### First/Last Item

```bash
az resource list --query "[0].name" -o tsv
az resource list --query "[-1].name" -o tsv
```

## Environment Variables

### Set Default Subscription

```bash
export AZURE_DEFAULTS_SUBSCRIPTION="subscription-id"
```

### Set Default Location

```bash
export AZURE_DEFAULTS_LOCATION="eastus"
```

### Set Default Resource Group

```bash
export AZURE_DEFAULTS_GROUP="my-resource-group"
```

## Scripting Patterns

### Get Resource ID

```bash
RESOURCE_ID=$(az webapp show -n APP -g RG --query "id" -o tsv)
```

### Loop Over Resources

```bash
for app in $(az webapp list -g RG --query "[].name" -o tsv); do
  echo "Processing $app"
  az webapp show -n "$app" -g RG
done
```

### Check If Resource Exists

```bash
if az webapp show -n APP -g RG &>/dev/null; then
  echo "App exists"
else
  echo "App does not exist"
fi
```

### Wait for Operation

```bash
az webapp create ... --no-wait
az webapp wait --name APP -g RG --created
```

## Error Handling

### Suppress Errors

```bash
az resource show --ids ID 2>/dev/null || echo "Not found"
```

### Check Exit Code

```bash
if az webapp show -n APP -g RG; then
  echo "Success"
else
  echo "Failed with code $?"
fi
```

## Configuration

### View Config

```bash
az config get
```

### Set Defaults

```bash
az config set defaults.group=myRG
az config set defaults.location=eastus
```

### Disable Telemetry

```bash
az config set core.collect_telemetry=false
```

## Extensions

### List Extensions

```bash
az extension list
```

### Add Extension

```bash
az extension add --name extension-name
```

### Update Extensions

```bash
az extension update --name extension-name
```

## Performance Tips

1. **Use `--no-wait`** for long operations
2. **Use `--query`** to reduce output size
3. **Use TSV output** for parsing
4. **Cache results** when querying multiple times
5. **Use resource IDs** instead of name lookups

## Common Issues

### Command Not Found

```bash
# Update CLI
az upgrade

# Or reinstall
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### Authentication Expired

```bash
az login --use-device-code
```

### Permission Denied

Check RBAC roles:
```bash
az role assignment list --assignee USER@domain.com
```

# Azure Functions

## Quick Reference

| Property | Value |
|----------|-------|
| CLI prefix | `az functionapp`, `func` |
| MCP tools | `azure_function_app_list` |
| Best for | Event-driven, pay-per-execution, serverless |

## Hosting Plans

| Plan | Scaling | Timeout | Use Case |
|------|---------|---------|----------|
| Consumption | Auto, to 0 | 5-10 min | Event-driven, variable load |
| Premium | Auto, warm | 30+ min | Consistent load, VNet |
| Dedicated | Manual | Unlimited | Predictable load |

## Trigger Types

| Trigger | Use Case |
|---------|----------|
| HTTP | REST APIs, webhooks |
| Timer | Scheduled jobs (CRON) |
| Blob | File processing |
| Queue | Message processing |
| Event Grid | Event-driven |
| Cosmos DB | Change feed processing |
| Service Bus | Enterprise messaging |

## Local Development

```bash
# Create new function project
func init MyFunctionApp --worker-runtime node

# Create new function
func new --name MyHttpTrigger --template "HTTP trigger"

# Run locally
func start

# Deploy to Azure
func azure functionapp publish FUNCTIONAPP
```

## CLI Management

```bash
# List function apps
az functionapp list --output table

# Get function app details
az functionapp show -n FUNCTIONAPP -g RG

# View function keys
az functionapp keys list -n FUNCTIONAPP -g RG

# Set app settings
az functionapp config appsettings set \
  -n FUNCTIONAPP -g RG \
  --settings KEY=VALUE
```

## Durable Functions

For long-running orchestrations:

```javascript
// Orchestrator
const df = require('durable-functions');

module.exports = df.orchestrator(function* (context) {
    const result1 = yield context.df.callActivity('Step1', input);
    const result2 = yield context.df.callActivity('Step2', result1);
    return result2;
});
```

Patterns:
- Function chaining
- Fan-out/fan-in
- Async HTTP APIs
- Human interaction
- Aggregator

## Cold Start Mitigation

For Consumption plan:
1. Keep package size small (<100MB)
2. Use Premium plan for consistent performance
3. Implement health check endpoints
4. Use pre-warming with timer triggers

## Best Practices

1. **Keep functions small** and single-purpose
2. **Implement idempotency** for at-least-once triggers
3. **Configure retry policies** appropriately
4. **Monitor with Application Insights**
5. **Use Key Vault** for secrets
6. **Enable managed identity** for Azure resource access

## Gotchas

1. **Execution limits** - Consumption has 5-10 min timeout
2. **Scaling delays** - Cold starts on Consumption plan
3. **Binding limits** - Some bindings have connection limits
4. **Storage dependency** - Functions require storage account

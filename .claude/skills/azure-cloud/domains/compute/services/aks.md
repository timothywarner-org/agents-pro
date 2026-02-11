# Azure Kubernetes Service (AKS)

## Quick Reference

| Property | Value |
|----------|-------|
| CLI prefix | `az aks` |
| MCP tools | `azure_aks_cluster_list`, `azure_aks_nodepool_list` |
| Best for | Complex microservices, full K8s control |

## When to Use AKS

- Need full Kubernetes capabilities
- Have Kubernetes expertise
- Complex multi-service architectures
- Require custom controllers/operators
- Need specific K8s features (CRDs, service mesh)

Consider Container Apps for simpler scenarios.

## Cluster Creation

```bash
# Create cluster with managed identity
az aks create \
  --name mycluster -g RG \
  --node-count 3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --name mycluster -g RG
```

## Node Pools

| Pool Type | Use Case |
|-----------|----------|
| System | Core cluster services |
| User (General) | Standard workloads |
| User (Spot) | Batch, interruptible |
| User (GPU) | ML, graphics |

```bash
# Add node pool
az aks nodepool add \
  --cluster-name mycluster -g RG \
  --name userpool \
  --node-count 3 \
  --node-vm-size Standard_DS3_v2

# Scale node pool
az aks nodepool scale \
  --cluster-name mycluster -g RG \
  --name userpool \
  --node-count 5

# Enable autoscaler
az aks nodepool update \
  --cluster-name mycluster -g RG \
  --name userpool \
  --enable-cluster-autoscaler \
  --min-count 1 --max-count 10
```

## Workload Identity

Replace pod-managed identity:

```bash
# Enable OIDC issuer
az aks update \
  --name mycluster -g RG \
  --enable-oidc-issuer \
  --enable-workload-identity

# Create managed identity
az identity create --name myidentity -g RG

# Create federated credential
az identity federated-credential create \
  --name myfc \
  --identity-name myidentity -g RG \
  --issuer $(az aks show -n mycluster -g RG --query "oidcIssuerProfile.issuerUrl" -o tsv) \
  --subject system:serviceaccount:NAMESPACE:SERVICE_ACCOUNT
```

## Cluster Configuration

```bash
# Enable Azure Policy
az aks enable-addons \
  --name mycluster -g RG \
  --addons azure-policy

# Enable monitoring
az aks enable-addons \
  --name mycluster -g RG \
  --addons monitoring

# Update to private cluster
az aks update \
  --name mycluster -g RG \
  --enable-private-cluster
```

## Deployment Patterns

| Pattern | Description |
|---------|-------------|
| Blue-green | Two identical environments, switch traffic |
| Canary | Gradual rollout with traffic split |
| Rolling | Sequential pod replacement (default) |
| A/B | Feature-based routing |

## Best Practices

1. Use managed identity for cluster authentication
2. Enable Azure Policy for governance
3. Configure network policy (Calico/Azure)
4. Use private clusters for production
5. Enable container insights for monitoring
6. Use availability zones for HA
7. Minimum 3 nodes for production
8. Set resource quotas per namespace

## Common Operations

```bash
# List clusters
az aks list --output table

# Get cluster info
az aks show --name mycluster -g RG

# Upgrade cluster
az aks upgrade --name mycluster -g RG --kubernetes-version VERSION

# Start/stop cluster (dev/test)
az aks stop --name mycluster -g RG
az aks start --name mycluster -g RG
```

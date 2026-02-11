# Azure SQL Database

## Quick Reference

| Property | Value |
|----------|-------|
| CLI prefix | `az sql` |
| MCP tools | `azure_sql_server_list`, `azure_sql_database_list`, `azure_sql_firewall_list` |
| Best for | Relational data, ACID transactions, T-SQL |

## Service Tiers

| Tier | Use Case | vCores | Storage |
|------|----------|--------|---------|
| Basic | Dev/test | Shared | 2 GB |
| Standard | Small production | Shared | 250 GB |
| Premium | High IOPS | Dedicated | 4 TB |
| Hyperscale | Large databases | Dedicated | 100 TB |
| Serverless | Variable workloads | Auto-scale | 4 TB |

## DTU vs vCore

**DTU model:** Bundled compute/storage/IO - simpler pricing
**vCore model:** Separate compute/storage - more control

Use vCore for:
- Existing SQL Server licenses (Azure Hybrid Benefit)
- Fine-grained resource control
- Reserved capacity pricing

## High Availability

| Option | SLA | Use Case |
|--------|-----|----------|
| Zone redundant | 99.995% | Regional HA |
| Geo-replication | RPO <5s | Disaster recovery |
| Auto-failover groups | Automatic | Multi-region HA |

## Security Best Practices

1. Enable Azure AD authentication (avoid SQL auth)
2. Use private endpoints
3. Enable TDE (Transparent Data Encryption) - default on
4. Configure auditing to Log Analytics
5. Use Always Encrypted for sensitive columns
6. Enable Advanced Threat Protection

## Performance Optimization

1. **Automatic tuning** - Let Azure optimize indexes
2. **Query performance insights** - Identify slow queries
3. **Elastic pools** - Share resources across databases
4. **Read replicas** - Offload read workloads

## Common Operations

```bash
# List servers
az sql server list --output table

# List databases
az sql db list --server SERVER -g RG --output table

# Check firewall rules
az sql server firewall-rule list --server SERVER -g RG --output table

# Create firewall rule
az sql server firewall-rule create \
  --server SERVER -g RG \
  --name AllowMyIP \
  --start-ip-address IP --end-ip-address IP
```

## Migration from SQL Server

1. **Assessment** - Use Data Migration Assistant
2. **Schema migration** - Generate scripts or use tools
3. **Data migration** - DMS, bacpac, or replication
4. **Cutover** - Switch connection strings
5. **Validation** - Verify data integrity

# Azure Cosmos DB

## Quick Reference

| Property | Value |
|----------|-------|
| CLI prefix | `az cosmosdb` |
| MCP tools | `azure_cosmosdb_account_list`, `azure_cosmosdb_database_list`, `azure_cosmosdb_container_list` |
| Best for | JSON documents, global distribution, <10ms reads |

## API Selection

| API | Data Model | Use Case |
|-----|-----------|----------|
| NoSQL (Core) | Document | Most scenarios, native |
| MongoDB | Document | MongoDB compatibility |
| PostgreSQL | Relational | Distributed PostgreSQL |
| Cassandra | Wide-column | Cassandra workloads |
| Gremlin | Graph | Graph relationships |

## Partitioning Strategy

**Partition key selection is critical:**

Good partition keys:
- High cardinality (many distinct values)
- Even distribution
- Included in most queries

Examples:
- `userId` for user data
- `tenantId` for multi-tenant
- `deviceId` for IoT

Bad partition keys:
- `status` (few values)
- `timestamp` (hot partition)
- `region` (uneven distribution)

## Consistency Levels

| Level | Guarantees | Use Case |
|-------|-----------|----------|
| Strong | Linearizable | Financial transactions |
| Bounded Staleness | Bounded delay | Inventory systems |
| Session | Session consistency | Most applications (default) |
| Consistent Prefix | Order preserved | Audit logs |
| Eventual | No guarantees | Recommendations |

## Request Units (RUs)

RU = normalized cost of operations:
- Point read (1KB): 1 RU
- Write (1KB): ~5 RUs
- Query: varies by complexity

**Throughput options:**
- Provisioned: Set RU/s, consistent cost
- Autoscale: 10-100% of max, automatic
- Serverless: Pay per request

## Common Patterns

### Query with Filters

MCP:
```
Use azure_cosmosdb tools to browse accounts, databases, and containers.
For queries, use the Azure portal or SDK.
```

CLI:
```bash
az cosmosdb sql query \
  --account-name ACCOUNT \
  --database-name DB \
  --container-name CONTAINER \
  --query "SELECT * FROM c WHERE c.status = 'active'"
```

### Cross-Partition Queries

Enable with `--enable-cross-partition-query true` in CLI.
Avoid when possible - they're expensive.

## Cost Optimization

1. Use autoscale instead of manual provisioning
2. Optimize partition keys to avoid cross-partition queries
3. Enable TTL for automatic data expiration
4. Use analytical store for analytics workloads
5. Consider reserved capacity for 1-3 year commitment

## Gotchas

1. **RU consumption** - Complex queries consume more RUs
2. **Partition limits** - 20GB per logical partition
3. **Index policy** - Review and customize for your queries
4. **Consistency trade-offs** - Stronger = higher latency

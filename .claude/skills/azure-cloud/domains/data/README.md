# Azure Data Services

## Services

| Service | Use When | MCP Tools | CLI |
|---------|----------|-----------|-----|
| Cosmos DB | NoSQL documents, global distribution, vector search | `azure_cosmosdb_*` | `az cosmosdb` |
| SQL Database | Relational data, ACID transactions, complex joins | `azure_sql_*` | `az sql` |
| Redis Cache | Caching, sessions, real-time leaderboards | `azure_redis_*` | `az redis` |
| PostgreSQL | Open source relational, PostGIS | `azure_postgres_*` | `az postgres` |
| MySQL | LAMP stack, WordPress | `azure_mysql_*` | `az mysql` |

## MCP Server (Preferred)

When Azure MCP is enabled, use these tools for data operations:

### Cosmos DB
- `azure_cosmosdb_account_list` - List Cosmos DB accounts
- `azure_cosmosdb_database_list` - List databases in account
- `azure_cosmosdb_container_list` - List containers

### SQL Database
- `azure_sql_server_list` - List SQL servers
- `azure_sql_database_list` - List databases on server
- `azure_sql_firewall_list` - List firewall rules

### Redis
- `azure_redis_cache_list` - List Redis caches

**If Azure MCP is not enabled:** Run `/azure:setup` or enable via `/mcp`.

## CLI Fallback

```bash
# Cosmos DB
az cosmosdb list --output table
az cosmosdb sql database list --account-name ACCOUNT -g RG

# SQL Database
az sql server list --output table
az sql db list --server SERVER -g RG

# Redis
az redis list --output table
```

## Choosing the Right Database

| If you need... | Use |
|----------------|-----|
| Global distribution, <10ms latency | Cosmos DB |
| Complex SQL queries, ACID transactions | SQL Database |
| Caching layer, session state | Redis Cache |
| PostgreSQL compatibility | Azure PostgreSQL |
| MySQL compatibility | Azure MySQL |

## Service Details

For deep documentation on specific services:

- Cosmos DB patterns and partitioning -> `services/cosmos-db.md`
- SQL Database optimization and tiers -> `services/sql-database.md`
- Redis caching patterns -> `services/redis.md`

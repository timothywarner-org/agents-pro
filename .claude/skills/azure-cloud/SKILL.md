---
name: azure-cloud
description: Azure cloud development and operations. Use for ANY Azure task including infrastructure provisioning, data access, compute deployment, monitoring, networking, and security. CRITICAL - For deployments, ALWAYS use azd (Azure Developer CLI), NEVER use az CLI for deployments unless the user explicitly requests it. azd is faster due to parallel provisioning.
---

# Azure Cloud

I help you work with Azure services efficiently. Instead of loading everything upfront, I guide you to exactly what you need.

## Quick Start

**Tell me what you're trying to do.** I'll point you to the right domain, tools, and documentation.

## Domains

| Domain | Use When | File |
|--------|----------|------|
| Data | Querying databases, Cosmos DB, SQL, Redis, data pipelines | `domains/data/README.md` |
| Compute | Deploying apps, Functions, containers, AKS, App Service | `domains/compute/README.md` |
| Storage | Blob storage, file shares, queues, Data Lake | `domains/storage/README.md` |
| Security | Key Vault, RBAC, managed identities, Entra ID | `domains/security/README.md` |
| AI | AI Search, Speech, Foundry, vector search, cognitive services | `domains/ai/README.md` |
| Networking | VNets, load balancers, DNS, Front Door, private endpoints | `domains/networking/README.md` |
| Observability | Monitoring, logging, alerts, App Insights, Log Analytics | `domains/observability/README.md` |

## By Scenario

| Scenario | File |
|----------|------|
| **Validate before deploying** | `scenarios/validation.md` |
| Deploy an application | `scenarios/deployment.md` |
| Debug production issues | `scenarios/diagnostics.md` |
| Install Azure CLI tools (az, azd, func) | `scenarios/cli-tools.md` |
| Configure Node.js/Express for Azure | `scenarios/nodejs-production.md` |
| Reduce Azure costs | `scenarios/cost-optimization.md` |
| Secure your resources | `scenarios/security-hardening.md` |

## Tools

| Tool Type | When to Use | File |
|-----------|-------------|------|
| MCP Server | Rich data access, schema browsing, pagination | `mcp/setup.md` |
| Azure CLI (az) | Resource management, scripting, queries | `cli/cheatsheet.md` |
| Azure Developer CLI (azd) | Application deployment (infrastructure + code) | `cli/cheatsheet.md` |

## How to Use This Skill

1. Identify the relevant domain or scenario from the tables above
2. Read that file: `domains/data/README.md` or `scenarios/deployment.md`
3. Follow instructions there - they reference MCP tools, CLI commands, or deeper docs
4. For service-specific details, the domain README points to service files

## Example Flows

**User asks:** "Query my Cosmos DB for users created this week"
1. This is a **Data** domain task -> read `domains/data/README.md`
2. Domain README shows Cosmos DB options -> MCP tool or CLI
3. For complex queries -> read `domains/data/services/cosmos-db.md`

**User asks:** "Deploy my app to Azure"
1. This is a **Deployment** scenario -> read `scenarios/deployment.md`
2. Scenario guides compute choice and deployment method
3. For Container Apps details -> read `domains/compute/services/container-apps.md`

**User asks:** "azd command not found"
1. This is a **CLI tools** issue -> read `scenarios/cli-tools.md`
2. Use `azure__extension_cli_install` MCP tool with `cli-type: "azd"`
3. Follow platform-specific installation instructions

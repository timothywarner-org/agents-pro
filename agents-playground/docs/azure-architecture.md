# Azure Architecture for O'Reilly Agent MVP

This diagram highlights the production-ready Azure landing zone that hosts the LangGraph + CrewAI pipeline alongside the folder watcher demo and token tracking utilities.

## Mermaid Diagram

```mermaid
flowchart LR
    classDef azure fill:#0078D4,stroke:#004578,color:#ffffff,font-weight:bold;
    classDef azureAgent fill:#5B58C6,stroke:#322A8E,color:#ffffff,font-weight:bold;
    classDef azureData fill:#035388,stroke:#012C50,color:#ffffff,font-weight:bold;
    classDef azureControl fill:#00B294,stroke:#00643C,color:#ffffff,font-weight:bold;
    classDef azureNeutral fill:#F3F2F1,stroke:#A19F9D,color:#1A1A1A;
    classDef azureAlert fill:#FFB900,stroke:#C25E00,color:#1A1A1A;

    subgraph Edge["Edge Access"]
        User[Developer Portal<br/>or CLI]:::azureNeutral
        GitHub[GitHub Issue Webhook]:::azureNeutral
    end

    subgraph Azure["Azure Landing Zone"]
        subgraph Entry["API Layer"]
            APIM[Azure API Management<br/>Global Gateway]:::azure
        end
        subgraph Orchestration["Agent Orchestration"]
            Container[Azure Container Apps<br/>LangGraph Orchestrator]:::azure
            subgraph Agents["CrewAI Agent Pool"]
                PM[PM Agent]:::azureAgent
                DEV[Dev Agent]:::azureAgent
                QA[QA Agent]:::azureAgent
            end
        end
        subgraph Data["Knowledge & State"]
            Cosmos[(Azure Cosmos DB<br/>Workflow State)]:::azureData
            Queue[(Azure Storage Queue<br/>Issue Events)]:::azureData
            Monitor[Azure Application Insights<br/>Telemetry]:::azureData
        end
        subgraph Security["Secrets & Compliance"]
            KeyVault[[Azure Key Vault]]:::azureControl
            ManagedId[System Assigned<br/>Managed Identity]:::azureControl
        end
        subgraph Workers["Async Processing"]
            Functions[Azure Function App<br/>Watcher Bridge]:::azure
            Storage[Azure Blob Storage<br/>Artifacts & Logs]:::azureData
        end
    end

    subgraph Hybrid["Hybrid Operations"]
        LocalWatcher[Self-Hosted Folder Watcher<br/>Verbose Demo Mode]:::azureNeutral
        TokenTracker[Token Tracking CLI<br/>Observation Runs]:::azureNeutral
    end

    User --> APIM
    GitHub --> Queue
    APIM --> Container
    Container --> PM
    PM --> DEV
    DEV --> QA
    QA --> Container
    Container --> Cosmos
    Container --> Queue
    Queue --> Functions
    Functions --> Storage
    Functions --> Cosmos
    LocalWatcher --> Storage
    LocalWatcher --> Queue
    Storage --> TokenTracker
    KeyVault --> Container
    KeyVault --> Functions
    ManagedId --> KeyVault
    Monitor -.-> APIM
    Monitor -.-> Container
    Monitor -.-> Functions
    Monitor -.-> Cosmos

    linkStyle 0 stroke:#0078D4,stroke-width:3px;
    linkStyle 2 stroke:#5B58C6,stroke-width:3px;
    linkStyle 6 stroke:#5B58C6,stroke-width:2px,stroke-dasharray:5 3;
    linkStyle 7 stroke:#5B58C6,stroke-width:2px,stroke-dasharray:5 3;
    linkStyle 9 stroke:#00B294,stroke-width:3px;
    linkStyle 10 stroke:#00B294,stroke-width:3px;
    linkStyle 11 stroke:#00B294,stroke-width:3px;
    linkStyle 12 stroke:#00B294,stroke-width:3px;
```

## Exporting

1. Run `npx @mermaid-js/mermaid-cli -i docs/azure-architecture.md -o docs/azure-architecture.svg` to generate an SVG snapshot.
2. Attach the resulting asset to release notes or architectural reviews as needed.

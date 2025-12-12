# Document Processor Agent — Actions & Flows

## Flows Architecture

```mermaid
flowchart TD
    subgraph "Agent Topics"
        T1[Process File]
        T2[Route Invoice]
        T3[Route Contract]
        T4[Handle Exception]
    end

    subgraph "Power Automate Flows"
        F1[AI Classification]
        F2[Invoice Extraction]
        F3[Contract Extraction]
        F4[Error Logging]
    end

    subgraph "AI Builder"
        AI1[Document Classification]
        AI2[Invoice Processing Model]
        AI3[Text Classification]
    end

    subgraph "Destinations"
        D1[(Dataverse)]
        D2[Teams Channels]
        D3[SharePoint]
    end

    T1 --> F1 --> AI1
    T2 --> F2 --> AI2
    F1 --> AI3
    T4 --> F4
    F1 & F2 & F3 --> D1
    F1 & F2 & F3 & F4 --> D2
    T1 --> D3
```

## Flow 1: AI Document Classification

| Attribute | Value |
|-----------|-------|
| **Name** | DocProc-Classify |
| **Trigger** | Run a flow from Copilot |
| **Build Time** | 20 minutes |

### Parameters

**Input:**
| Parameter | Type | Required |
|-----------|------|----------|
| FileURL | String | Yes |
| FileName | String | Yes |
| LibraryID | String | Yes |

**Output:**
| Parameter | Type |
|-----------|------|
| DocumentType | String |
| Confidence | Number |
| KeyPhrases | Array |

### Flow Steps

```mermaid
flowchart TD
    A[Trigger] --> B[SharePoint: Get file content]
    B --> C[AI Builder: Classify Document]
    C --> D[AI Builder: Extract Key Phrases]
    D --> E{Type = Invoice?}
    E --> |Yes| F[Set: Type=Invoice]
    E --> |No| G{Type = Contract?}
    G --> |Yes| H[Set: Type=Contract]
    G --> |No| I{Type = Resume?}
    I --> |Yes| J[Set: Type=Resume]
    I --> |No| K[Set: Type=Unknown]
    F & H & J & K --> L[Return: Type, Confidence]
```

---

## Flow 2: Invoice Field Extraction

| Attribute | Value |
|-----------|-------|
| **Name** | DocProc-ExtractInvoice |
| **Trigger** | Run a flow from Copilot |
| **Build Time** | 15 minutes |

### Parameters

**Input:**
| Parameter | Type |
|-----------|------|
| FileURL | String |

**Output:**
| Parameter | Type |
|-----------|------|
| VendorName | String |
| InvoiceNumber | String |
| Amount | Number |
| DueDate | Date |
| Success | Boolean |

### Flow Steps

```mermaid
flowchart TD
    A[Trigger] --> B[SharePoint: Get file]
    B --> C[AI Builder: Process Invoice]
    C --> D{Extraction<br/>Successful?}
    D --> |Yes| E[Map: Fields to output]
    D --> |No| F[Return: Success=false]
    E --> G[Dataverse: Create Invoice record]
    G --> H[Return: Invoice data]
```

---

## Flow 3: Teams Notification

| Attribute | Value |
|-----------|-------|
| **Name** | DocProc-Notify |
| **Trigger** | Run a flow from Copilot |
| **Build Time** | 10 minutes |

### Parameters

**Input:**
| Parameter | Type |
|-----------|------|
| Channel | String |
| DocumentType | String |
| FileName | String |
| Summary | String |
| FileURL | String |

### Adaptive Card Template

```json
{
  "type": "AdaptiveCard",
  "body": [
    {
      "type": "TextBlock",
      "text": "New ${DocumentType} Processed",
      "weight": "Bolder",
      "size": "Large"
    },
    {
      "type": "FactSet",
      "facts": [
        {"title": "File", "value": "${FileName}"},
        {"title": "Type", "value": "${DocumentType}"},
        {"title": "Processed", "value": "${Timestamp}"}
      ]
    },
    {
      "type": "TextBlock",
      "text": "${Summary}",
      "wrap": true
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View Document",
      "url": "${FileURL}"
    }
  ]
}
```

---

## Flow 4: Error Logging

| Attribute | Value |
|-----------|-------|
| **Name** | DocProc-LogError |
| **Trigger** | Run a flow from Copilot |
| **Build Time** | 10 minutes |

### Flow Steps

```mermaid
flowchart TD
    A[Trigger] --> B[Dataverse: Create Error Log]
    B --> C[SharePoint: Move to Exceptions]
    C --> D[Teams: Post to Admin Channel]
    D --> E[Return: LogID]
```

---

## AI Builder Models

### Document Classification Model

**Type:** Custom text classification
**Categories:**
- Invoice
- Contract
- Resume
- Report
- Correspondence
- Unknown

**Training Data:** 50+ samples per category

### Invoice Processing Model

**Type:** Pre-built invoice processing
**Extracted Fields:**
- Vendor name and address
- Invoice number
- Invoice date
- Due date
- Total amount
- Line items

---

## Dataverse Tables

### Document Processing Log

| Column | Type | Description |
|--------|------|-------------|
| ProcessingID | Auto-number | DOC-#### |
| FileName | Text | Original filename |
| FileURL | URL | SharePoint link |
| DocumentType | Choice | Classification result |
| Confidence | Number | 0-100 |
| Status | Choice | Processed/Failed/Manual |
| ProcessedDate | DateTime | Completion time |
| ProcessingTime | Number | Seconds |

### Invoices

| Column | Type |
|--------|------|
| InvoiceID | Auto-number |
| VendorName | Text |
| InvoiceNumber | Text |
| Amount | Currency |
| DueDate | Date |
| Status | Choice |
| SourceDocumentURL | URL |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| IncomingLibraryID | SharePoint library GUID |
| ProcessedFolderPath | Destination for processed files |
| ExceptionsFolderPath | Destination for failed files |
| AccountingChannelID | Teams channel for invoices |
| LegalChannelID | Teams channel for contracts |
| AdminChannelID | Teams channel for exceptions |
| ConfidenceThreshold | Minimum confidence (default: 80) |

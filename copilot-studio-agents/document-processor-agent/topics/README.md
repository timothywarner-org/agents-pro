# Document Processor Agent — Topics

## Autonomous Agent Topics

Unlike conversational agents, autonomous agents use **event triggers** instead of user phrases.

```mermaid
flowchart LR
    subgraph "Event Sources"
        SP[SharePoint]
        OD[OneDrive]
        OL[Outlook]
    end

    subgraph "Trigger Topics"
        T1[File Created]
        T2[File Modified]
        T3[Email Received]
    end

    subgraph "Processing Topics"
        P1[Classify Document]
        P2[Route Invoice]
        P3[Route Contract]
        P4[Handle Exception]
    end

    SP --> T1
    OD --> T2
    OL --> T3
    T1 --> P1
    T2 --> P1
    T3 --> P1
    P1 --> P2 & P3 & P4
```

## Topic Backlog

| Topic Name | Trigger Type | Key Steps | Exception Handling |
|------------|--------------|-----------|-------------------|
| Process New File | SharePoint: File Created | Get metadata, classify, route | Low confidence → Manual queue |
| Process Modified File | SharePoint: File Modified | Re-classify if needed, update records | Conflict → Flag for review |
| Process Email Attachment | Outlook: Email Received | Extract attachments, classify each | No attachment → Log and skip |
| Route Invoice | Called from classification | Extract fields, create record, notify | Extraction fail → Manual queue |
| Route Contract | Called from classification | Extract parties, assign reviewer, notify | Missing fields → Request info |
| Handle Exception | Called on error | Log error, move file, alert admin | Repeated fails → Create ticket |

## Topic: Process New File

**Trigger:** When a file is created in SharePoint

**Configuration:**
- Site: `https://contoso.sharepoint.com/sites/Documents`
- Library: `Incoming Documents`
- File types: PDF, DOCX, XLSX

**Flow:**
```mermaid
flowchart TD
    A[Trigger: File Created] --> B[Get: File URL, Name, Size]
    B --> C{File Size < 10MB?}
    C --> |No| D[Exception: File too large]
    C --> |Yes| E[Call: AI Classification Flow]
    E --> F{Confidence > 80%?}
    F --> |Yes| G[Route by Type]
    F --> |No| H[Route to Manual Queue]
    G --> I[Update: File Metadata]
    H --> I
    I --> J[Log: Processing Complete]
```

**Variables:**
| Name | Type | Source |
|------|------|--------|
| FileURL | URL | Trigger output |
| FileName | Text | Trigger output |
| DocumentType | Text | Classification output |
| Confidence | Number | Classification output |
| ProcessingStatus | Text | Set by topic |

## Topic: Route Invoice

**Trigger:** Called when DocumentType = "Invoice"

**Flow:**
```mermaid
flowchart TD
    A[Start: Invoice Detected] --> B[Call: Extract Invoice Fields]
    B --> C{Extraction Successful?}
    C --> |Yes| D[Create: Dataverse Invoice Record]
    C --> |No| E[Route to Exception]
    D --> F{Amount > $10,000?}
    F --> |Yes| G[Start: Approval Flow]
    F --> |No| H[Notify: Accounting Channel]
    G --> H
    H --> I[Update: File Status = Processed]
```

**Extracted Fields:**
- Vendor Name
- Invoice Number
- Amount
- Due Date
- Line Items (array)

## Topic: Handle Exception

**Trigger:** Called when processing fails

**Flow:**
```mermaid
flowchart TD
    A[Start: Exception] --> B[Log: Error to Dataverse]
    B --> C[Move: File to Exceptions Folder]
    C --> D[Teams: Post to Admin Channel]
    D --> E{Error Count > 5<br/>in last hour?}
    E --> |Yes| F[Create: Support Ticket]
    E --> |No| G[End]
    F --> G
```

## Testing Scenarios

| Scenario | Test File | Expected Result |
|----------|-----------|-----------------|
| Invoice detected | Sample_Invoice.pdf | Routes to accounting, creates record |
| Contract detected | NDA_Template.docx | Routes to legal, assigns reviewer |
| Low confidence | Random_Document.pdf | Routes to manual queue |
| Large file | 15MB_Report.pdf | Exception: File too large |
| Processing error | Corrupted_File.pdf | Exception logged, admin notified |

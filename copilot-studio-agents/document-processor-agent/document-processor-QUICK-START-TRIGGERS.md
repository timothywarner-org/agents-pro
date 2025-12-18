# Quick Start: Event Triggers for Document Processor Agent

**What this guide covers:** Setting up autonomous event-driven document processing in Microsoft Copilot Studio.

**Time estimate:** 30-45 minutes for MVP

**Difficulty:** Intermediate

---

## Looking for Something Simpler?

If you want to start with a basic flow that does not require Copilot Studio or AI Builder, see **[QUICK-START-FLOWS.md](./QUICK-START-FLOWS.md)** first. That guide builds a single Power Automate flow that classifies documents by file name and moves them to subfolders.

**This guide (QUICK-START-TRIGGERS.md)** is for the full Copilot Studio integration with AI Builder classification and generative orchestration.

---

## Your SharePoint Environment

This guide uses the following SharePoint site:

| Setting | Value |
|---------|-------|
| **Site URL** | `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET` |
| **Library** | `Shared Documents` |
| **Agent Folder** | `document-processor-agent` |
| **Full Path** | `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET/Shared Documents/document-processor-agent` |

---

## Before You Start

This agent works differently from chatbots. Instead of waiting for users to type messages, it **listens for events** (like new files appearing in SharePoint) and processes them automatically.

### Prerequisites Checklist

- [ ] Microsoft 365 account with SharePoint access
- [ ] Copilot Studio license (trial works)
- [ ] Power Automate access (included with Microsoft 365)
- [ ] A SharePoint site with a document library

---

## Part 1: Enable Generative Orchestration

**Generative orchestration** lets your agent automatically choose which topic to run when an event arrives. Without this, event triggers will not work properly.

### Steps

- [ ] **Step 1.** Open [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)

- [ ] **Step 2.** Select your Document Processor agent (or create one first)

- [ ] **Step 3.** Click `Settings` in the left navigation

- [ ] **Step 4.** Find the `Generative AI` section

- [ ] **Step 5.** Under `Orchestration`, find the toggle: **"Use generative AI orchestration for your agent's responses?"**

- [ ] **Step 6.** Select `Yes`

- [ ] **Step 7.** Click `Save` at the top of the page

### What This Does

When enabled, your agent can:
- Automatically pick the right topic based on incoming data
- Chain multiple actions together without manual routing
- Handle unexpected scenarios gracefully

**Documentation:** [Generative actions overview](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions)

---

## Part 2: Create the SharePoint Trigger Flow

Copilot Studio agents cannot directly listen for SharePoint events. Instead, you create a **Power Automate flow** that:
1. Watches SharePoint for new files
2. Sends the file info to your agent
3. Receives the agent's response

### Steps

- [ ] **Step 1.** Go to [make.powerautomate.com](https://make.powerautomate.com)

- [ ] **Step 2.** Click `+ Create` in the left menu

- [ ] **Step 3.** Select `Automated cloud flow`

- [ ] **Step 4.** Name your flow: `DocProcessor-FileCreated`

- [ ] **Step 5.** In the trigger search box, type `SharePoint`

- [ ] **Step 6.** Select the trigger: **"When a file is created (properties only)"**

> **Why "properties only"?** This trigger is faster and more reliable than the deprecated "When a file is created in a folder" trigger. You will add a separate step to get the file content.

- [ ] **Step 7.** Click `Create`

---

## Part 3: Configure the SharePoint Trigger

### Steps

- [ ] **Step 1.** In the trigger box, click `Site Address` dropdown

- [ ] **Step 2.** Select your SharePoint site: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`

- [ ] **Step 3.** Click `Library Name` dropdown

- [ ] **Step 4.** Select `Shared Documents`

- [ ] **Step 5.** Click `Show advanced options`

- [ ] **Step 6.** In the `Folder` field, type: `/document-processor-agent`

- [ ] **Step 7.** (Optional) Click `Limit Columns by View` if your library has many columns

### Trigger Output Variables

After this trigger fires, you have access to:

| Variable | What It Contains |
|----------|------------------|
| `{Name}` | File name (e.g., `Invoice-2025-001.pdf`) |
| `{Link to item}` | Full URL to the file |
| `{Created By Email}` | Email of person who uploaded |
| `{File identifier}` | Internal ID for getting file content |

---

## Part 4: Add the "Get File Content" Action

The trigger only gives you file properties. To process the actual file, add this action.

### Steps

- [ ] **Step 1.** Click `+ New step` below the trigger

- [ ] **Step 2.** Search for `SharePoint`

- [ ] **Step 3.** Select action: **"Get file content"**

- [ ] **Step 4.** In `Site Address`, select the same site as your trigger

- [ ] **Step 5.** Click in the `File Identifier` field

- [ ] **Step 6.** In the Dynamic content panel, select `File identifier` from the trigger outputs

---

## Part 5: Create the Agent Flow (Called by Agent)

Now create a separate flow that your Copilot Studio agent can call as a **tool**. This flow will do the actual document classification.

### Steps

- [ ] **Step 1.** Go back to [make.powerautomate.com](https://make.powerautomate.com)

- [ ] **Step 2.** Click `+ Create` > `Instant cloud flow`

- [ ] **Step 3.** Name it: `DocProcessor-Classify`

- [ ] **Step 4.** Select trigger: **"When an agent calls the flow"**

> This special trigger makes the flow callable from Copilot Studio topics.

- [ ] **Step 5.** Click `Create`

### Add Input Parameters

- [ ] **Step 6.** In the trigger, click `+ Add an input`

- [ ] **Step 7.** Add these inputs:

| Name | Type |
|------|------|
| FileURL | Text |
| FileName | Text |
| LibraryName | Text |

### Add Classification Logic

- [ ] **Step 8.** Click `+ New step`

- [ ] **Step 9.** Add a `Compose` action (for MVP testing)

- [ ] **Step 10.** In the `Inputs` field, paste:

```json
{
  "DocumentType": "Invoice",
  "Confidence": 0.85,
  "RouteTo": "AP-Queue"
}
```

> **For production:** Replace this with AI Builder document classification. See [AI Builder document processing](https://learn.microsoft.com/ai-builder/document-processing-model-overview).

### Add Response

- [ ] **Step 11.** Click `+ New step`

- [ ] **Step 12.** Search for and select: **"Respond to the agent"**

- [ ] **Step 13.** Click `+ Add an output`

- [ ] **Step 14.** Add these outputs:

| Name | Type | Value |
|------|------|-------|
| DocumentType | Text | `outputs('Compose')?['DocumentType']` |
| Confidence | Number | `outputs('Compose')?['Confidence']` |
| RouteTo | Text | `outputs('Compose')?['RouteTo']` |

- [ ] **Step 15.** Click `Save`

- [ ] **Step 16.** Click `Publish` (top right)

---

## Part 6: Add the Flow as a Tool in Copilot Studio

### Steps

- [ ] **Step 1.** Return to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)

- [ ] **Step 2.** Open your Document Processor agent

- [ ] **Step 3.** Click `Tools` in the left navigation

- [ ] **Step 4.** Click `+ Add a tool`

- [ ] **Step 5.** Select `Flow` tab

- [ ] **Step 6.** Find and select `DocProcessor-Classify`

- [ ] **Step 7.** Click `Add and configure`

- [ ] **Step 8.** Enter a clear description:

```
Classifies an uploaded document by analyzing the file name and content.
Returns the document type (Invoice, Contract, Resume, or Unknown),
confidence score (0-1), and routing destination.
```

- [ ] **Step 9.** Click `Save`

**Documentation:** [Call a flow as a tool](https://learn.microsoft.com/microsoft-copilot-studio/advanced-use-flow)

---

## Part 7: Create the Classify and Route Topic

This topic runs when your agent receives file information from the SharePoint trigger flow.

### Steps

- [ ] **Step 1.** Click `Topics` in the left navigation

- [ ] **Step 2.** Click `+ Add a topic` > `From blank`

- [ ] **Step 3.** Name the topic: `Classify and Route`

> **Important:** Do not use periods in topic names. This causes export errors.

- [ ] **Step 4.** Click the `Trigger` node

- [ ] **Step 5.** Change the trigger to: **"The agent chooses"**

- [ ] **Step 6.** In the `Description` field, enter:

```
Use this topic when processing a new document from SharePoint.
Expects file URL, file name, and library name as inputs.
Classifies the document and routes it to the appropriate queue.
```

### Add Topic Variables

- [ ] **Step 7.** Click `Variables` in the topic toolbar

- [ ] **Step 8.** Add these topic variables:

| Name | Type |
|------|------|
| FileURL | Text |
| FileName | Text |
| LibraryName | Text |
| DocumentType | Text |
| Confidence | Number |
| RouteTo | Text |

### Build the Topic Flow

- [ ] **Step 9.** Add a `Message` node:

```
Processing document: {Topic.FileName}
```

- [ ] **Step 10.** Add an `Action` node > Select `DocProcessor-Classify` tool

- [ ] **Step 11.** Map the inputs:
   - FileURL -> `Topic.FileURL`
   - FileName -> `Topic.FileName`
   - LibraryName -> `Topic.LibraryName`

- [ ] **Step 12.** Map the outputs:
   - DocumentType -> `Topic.DocumentType`
   - Confidence -> `Topic.Confidence`
   - RouteTo -> `Topic.RouteTo`

- [ ] **Step 13.** Add a `Condition` node:
   - Condition: `Topic.Confidence < 0.6`

- [ ] **Step 14.** Under `If true`, add a `Message` node:

```
Low confidence classification. Routing to manual review queue.
```

- [ ] **Step 15.** Under `If false`, add a `Message` node:

```
Classified as {Topic.DocumentType} with {Topic.Confidence} confidence.
Routing to {Topic.RouteTo}.
```

- [ ] **Step 16.** Click `Save`

---

## Part 8: Connect the Trigger Flow to Your Agent

Now connect the SharePoint trigger flow (Part 2-4) to call your agent.

### Option A: HTTP Request to Direct Line (Recommended for MVP)

- [ ] **Step 1.** In Copilot Studio, go to `Channels` > `Mobile app`

- [ ] **Step 2.** Copy the `Token Endpoint` URL

- [ ] **Step 3.** Return to Power Automate and open `DocProcessor-FileCreated`

- [ ] **Step 4.** After the SharePoint trigger, add an `HTTP` action:

| Field | Value |
|-------|-------|
| Method | GET |
| URI | (paste your Token Endpoint) |

- [ ] **Step 5.** Add another `HTTP` action to start conversation:

| Field | Value |
|-------|-------|
| Method | POST |
| URI | `https://directline.botframework.com/v3/directline/conversations` |
| Headers | Authorization: `Bearer` + token from previous step |

- [ ] **Step 6.** Add an `HTTP` action to send the file info:

| Field | Value |
|-------|-------|
| Method | POST |
| URI | `https://directline.botframework.com/v3/directline/conversations/{conversationId}/activities` |
| Body | See JSON below |

```json
{
  "type": "message",
  "from": { "id": "PowerAutomate" },
  "text": "Process this document",
  "value": {
    "FileURL": "@{triggerOutputs()?['body/Link to item']}",
    "FileName": "@{triggerOutputs()?['body/Name']}",
    "LibraryName": "Shared Documents/document-processor-agent"
  }
}
```

### Option B: Use Dataverse as Intermediate (Simpler)

If HTTP calls feel complex, store the file info in Dataverse and have your agent poll for new records.

- [ ] **Step 1.** Create a Dataverse table: `Pending Documents`
- [ ] **Step 2.** In the SharePoint trigger flow, add: `Create a new row` in Dataverse
- [ ] **Step 3.** In Copilot Studio, create a scheduled topic that checks for pending rows

---

## Part 9: Create Exception Handling Flow

For documents with low confidence scores, route them to a manual review queue.

### Steps

- [ ] **Step 1.** In Power Automate, create a new flow: `DocProcessor-Exception`

- [ ] **Step 2.** Use trigger: **"When an agent calls the flow"**

- [ ] **Step 3.** Add inputs:

| Name | Type |
|------|------|
| FileURL | Text |
| FileName | Text |
| Reason | Text |

- [ ] **Step 4.** Add action: **"Copy file"** (SharePoint)
   - Source: `FileURL` input
   - Destination: `/Exceptions/` folder

- [ ] **Step 5.** Add action: **"Post message in a chat or channel"** (Teams)
   - Team: Select your admin team
   - Channel: Select exceptions channel
   - Message:

```
Document needs manual review:
File: {FileName}
Reason: {Reason}
Link: {FileURL}
```

- [ ] **Step 6.** Add: **"Respond to the agent"**
   - Output: `Success` (Boolean) = `true`

- [ ] **Step 7.** Save and Publish

- [ ] **Step 8.** Add this flow as a tool in Copilot Studio (same as Part 6)

---

## Part 10: Test Your Setup

### Test the Classification Flow

- [ ] **Step 1.** In Copilot Studio, open `Test your agent` panel

- [ ] **Step 2.** Type: `Process document Invoice-Test-001.pdf from Incoming Documents`

- [ ] **Step 3.** Verify the agent:
   - Calls the DocProcessor-Classify flow
   - Returns classification results
   - Routes based on confidence

### Test the SharePoint Trigger

- [ ] **Step 4.** Upload a test file to your `Incoming Documents` library

- [ ] **Step 5.** In Power Automate, check `Run history` for your trigger flow

- [ ] **Step 6.** Verify the flow:
   - Triggered on file upload
   - Sent data to your agent
   - Received classification response

### Test Exception Handling

- [ ] **Step 7.** Modify your Compose action to return low confidence:

```json
{
  "DocumentType": "Unknown",
  "Confidence": 0.3,
  "RouteTo": "ManualReview"
}
```

- [ ] **Step 8.** Upload another test file

- [ ] **Step 9.** Verify:
   - File copied to Exceptions folder
   - Teams notification sent

---

## Quick Reference: Key UI Locations

| Task | Where to Find It |
|------|------------------|
| Enable generative orchestration | Copilot Studio > Settings > Generative AI |
| Add a flow as tool | Copilot Studio > Tools > Add a tool |
| Create topic | Copilot Studio > Topics > Add a topic |
| Check flow runs | Power Automate > My flows > Run history |
| Get agent token endpoint | Copilot Studio > Channels > Mobile app |

---

## Troubleshooting

### Flow Not Triggering

**Symptom:** Upload file but nothing happens

**Check:**
- [ ] Is the flow turned on? (Power Automate > My flows > check toggle)
- [ ] Correct SharePoint site and library selected?
- [ ] Flow connections authenticated?

### Agent Not Selecting Topic

**Symptom:** Agent receives data but does not run Classify and Route topic

**Check:**
- [ ] Generative orchestration enabled? (Settings > Generative AI)
- [ ] Topic description clearly explains when to use it?
- [ ] Topic trigger set to "The agent chooses"?

### Low Confidence on Everything

**Symptom:** All documents route to exception queue

**Check:**
- [ ] AI Builder model trained with enough samples? (50+ per category recommended)
- [ ] File format supported? (PDF and DOCX work best)
- [ ] File content readable? (Not scanned images without OCR)

### HTTP Action Fails

**Symptom:** 401 or 403 error when calling Direct Line

**Check:**
- [ ] Token endpoint URL correct and complete?
- [ ] Agent published to a channel?
- [ ] Using fresh token? (Tokens expire after 1 hour)

---

## Next Steps

After completing this MVP:

1. **Add AI Builder** - Replace the static Compose action with actual document classification
2. **Add more document types** - Extend routing rules for contracts, resumes, etc.
3. **Add approval flows** - High-value invoices require manager approval
4. **Add Dataverse logging** - Track all processed documents for reporting

### Alternative: Start Simpler

If this guide feels overwhelming, start with **[QUICK-START-FLOWS.md](./QUICK-START-FLOWS.md)** instead. That guide builds a standalone Power Automate flow that:
- Watches the `document-processor-agent` folder
- Classifies files by keyword matching (no AI Builder required)
- Moves files to Invoices, Contracts, Resumes, or Exceptions subfolders
- Posts a notification to Teams

Once that flow is working, return to this guide to add Copilot Studio and AI Builder integration.

---

## Documentation Links

- [Generative orchestration](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions)
- [Topic triggers](https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers)
- [Call a flow as a tool](https://learn.microsoft.com/microsoft-copilot-studio/advanced-use-flow)
- [SharePoint triggers](https://learn.microsoft.com/connectors/sharepointonline)
- [AI Builder document processing](https://learn.microsoft.com/ai-builder/document-processing-model-overview)
- [Direct Line API](https://learn.microsoft.com/microsoft-copilot-studio/publication-connect-bot-to-custom-application)

---

*Last updated: December 2024*
*Compatible with: Microsoft Copilot Studio (December 2024 release)*

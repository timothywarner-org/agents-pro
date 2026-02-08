# Quick Start: Simple Document Classification Flow

**What this guide covers:** A single Power Automate flow that classifies documents by file name and moves them to subfolders.

**Time estimate:** 15-20 minutes

**Difficulty:** Beginner

**No AI Builder required:** This flow uses simple file name matching.

---

## How This Flow Works

```
New file uploaded to SharePoint
        |
        v
Check file name for keywords
        |
        +-- Contains "invoice" --> Move to Invoices/
        |
        +-- Contains "contract" --> Move to Contracts/
        |
        +-- Contains "resume" --> Move to Resumes/
        |
        +-- No match --> Move to Exceptions/
        |
        v
Post notification to Teams
```

---

## Before You Start

### Prerequisites Checklist

- [ ] Microsoft 365 account with SharePoint and Teams access
- [ ] Power Automate access (included with Microsoft 365)
- [ ] Your SharePoint site URL: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`

### Folder Structure Required

Your SharePoint document library needs this structure:

```
Shared Documents/
    document-processor-agent/          <-- Flow watches this folder
        Invoices/                      <-- Destination for invoices
        Contracts/                     <-- Destination for contracts
        Resumes/                       <-- Destination for resumes
        Exceptions/                    <-- Destination for unclassified files
```

Create these folders in SharePoint before starting if they do not exist.

---

## Part 1: Create a New Flow

- [ ] **Step 1.** Open your browser and go to [make.powerautomate.com](https://make.powerautomate.com)

- [ ] **Step 2.** Sign in with your Microsoft 365 account

- [ ] **Step 3.** Click `+ Create` in the left navigation menu

- [ ] **Step 4.** Click `Automated cloud flow`

- [ ] **Step 5.** In the **Flow name** field, type: `DocProcessor-ClassifyAndMove`

- [ ] **Step 6.** In the search box under "Choose your flow's trigger", type: `SharePoint`

- [ ] **Step 7.** Select the trigger: **When a file is created (properties only)**

> **Why this trigger?** The "properties only" version is faster and more reliable than older SharePoint triggers. It fires immediately when a file is uploaded.

- [ ] **Step 8.** Click `Create`

---

## Part 2: Configure the SharePoint Trigger

You should now see the flow designer with your trigger at the top.

- [ ] **Step 1.** Click the trigger box to expand it

- [ ] **Step 2.** Click the `Site Address` dropdown

- [ ] **Step 3.** Select: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`

> **Not seeing your site?** Click `Enter custom value` and paste the URL directly.

- [ ] **Step 4.** Click the `Library Name` dropdown

- [ ] **Step 5.** Select: `Shared Documents`

- [ ] **Step 6.** Click `Show advanced options`

- [ ] **Step 7.** In the `Folder` field, type: `/document-processor-agent`

> **Important:** The forward slash at the start is required. This ensures the flow only triggers for files in this specific folder.

---

## Part 3: Add a Variable to Track the Destination

We need a place to store where the file should go.

- [ ] **Step 1.** Click `+ New step`

- [ ] **Step 2.** In the search box, type: `Initialize variable`

- [ ] **Step 3.** Select action: **Initialize variable**

- [ ] **Step 4.** In the `Name` field, type: `DestinationFolder`

- [ ] **Step 5.** Click the `Type` dropdown and select: `String`

- [ ] **Step 6.** Leave the `Value` field empty for now

---

## Part 4: Check for "Invoice" in File Name

Now we build the classification logic using **Condition** actions.

- [ ] **Step 1.** Click `+ New step`

- [ ] **Step 2.** In the search box, type: `Condition`

- [ ] **Step 3.** Select action: **Condition**

- [ ] **Step 4.** Click in the first "Choose a value" box

- [ ] **Step 5.** In the **Dynamic content** panel that appears, type `Name` in the search box

- [ ] **Step 6.** Select `Name` (this is the file name from the trigger)

- [ ] **Step 7.** Click the middle dropdown and select: `contains`

- [ ] **Step 8.** In the right "Choose a value" box, type: `invoice`

> **Note:** This check is case-insensitive by default. It will match "Invoice", "INVOICE", and "invoice".

---

## Part 5: Set Destination for Invoices

- [ ] **Step 1.** Under the `If yes` branch, click `Add an action`

- [ ] **Step 2.** Search for: `Set variable`

- [ ] **Step 3.** Select action: **Set variable**

- [ ] **Step 4.** In the `Name` dropdown, select: `DestinationFolder`

- [ ] **Step 5.** In the `Value` field, type: `/document-processor-agent/Invoices`

---

## Part 6: Check for "Contract" (Nested in If No)

- [ ] **Step 1.** Under the `If no` branch of the first condition, click `Add an action`

- [ ] **Step 2.** Search for and select: **Condition**

- [ ] **Step 3.** In the first "Choose a value" box, select Dynamic content: `Name`

- [ ] **Step 4.** Set the operator to: `contains`

- [ ] **Step 5.** In the right box, type: `contract`

---

## Part 7: Set Destination for Contracts

- [ ] **Step 1.** Under this new condition's `If yes` branch, click `Add an action`

- [ ] **Step 2.** Search for: `Set variable`

- [ ] **Step 3.** Select action: **Set variable**

- [ ] **Step 4.** In the `Name` dropdown, select: `DestinationFolder`

- [ ] **Step 5.** In the `Value` field, type: `/document-processor-agent/Contracts`

---

## Part 8: Check for "Resume" (Nested in If No)

- [ ] **Step 1.** Under the second condition's `If no` branch, click `Add an action`

- [ ] **Step 2.** Search for and select: **Condition**

- [ ] **Step 3.** In the first "Choose a value" box, select Dynamic content: `Name`

- [ ] **Step 4.** Set the operator to: `contains`

- [ ] **Step 5.** In the right box, type: `resume`

---

## Part 9: Set Destination for Resumes

- [ ] **Step 1.** Under this condition's `If yes` branch, click `Add an action`

- [ ] **Step 2.** Search for: `Set variable`

- [ ] **Step 3.** Select action: **Set variable**

- [ ] **Step 4.** In the `Name` dropdown, select: `DestinationFolder`

- [ ] **Step 5.** In the `Value` field, type: `/document-processor-agent/Resumes`

---

## Part 10: Set Destination for Exceptions (Default)

Files that do not match any keyword go to the Exceptions folder.

- [ ] **Step 1.** Under the third condition's `If no` branch, click `Add an action`

- [ ] **Step 2.** Search for: `Set variable`

- [ ] **Step 3.** Select action: **Set variable**

- [ ] **Step 4.** In the `Name` dropdown, select: `DestinationFolder`

- [ ] **Step 5.** In the `Value` field, type: `/document-processor-agent/Exceptions`

---

## Part 11: Move the File to Its Destination

Now we add the action to actually move the file. This goes AFTER all the condition blocks.

- [ ] **Step 1.** Scroll down past all the condition blocks

- [ ] **Step 2.** Click `+ New step` (at the very bottom of the flow)

- [ ] **Step 3.** Search for: `SharePoint move file`

- [ ] **Step 4.** Select action: **Move file**

- [ ] **Step 5.** In `Site Address`, select: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`

- [ ] **Step 6.** Click in the `Source File Id` field

- [ ] **Step 7.** In **Dynamic content**, search for and select: `Identifier`

> **Identifier vs Id:** Use `Identifier` from the trigger. This is the internal SharePoint file reference.

- [ ] **Step 8.** Click in the `Destination Folder` field

- [ ] **Step 9.** In **Dynamic content**, select: `DestinationFolder` (the variable we created)

---

## Part 12: Post Notification to Teams

Let your team know when a file is processed.

- [ ] **Step 1.** Click `+ New step`

- [ ] **Step 2.** Search for: `Microsoft Teams`

- [ ] **Step 3.** Select action: **Post message in a chat or channel**

- [ ] **Step 4.** In `Post as`, select: `Flow bot`

- [ ] **Step 5.** In `Post in`, select: `Channel`

- [ ] **Step 6.** In `Team`, select your team from the dropdown

- [ ] **Step 7.** In `Channel`, select the channel for notifications

- [ ] **Step 8.** In the `Message` field, type:

```
Document processed:
File: [select Name from Dynamic content]
Moved to: [select DestinationFolder from Dynamic content]
Uploaded by: [select Created By DisplayName from Dynamic content]
```

> **Tip:** Click in the Message box, then select dynamic content fields. The final message will look like: "Document processed: File: Invoice-ACME-001.pdf Moved to: /document-processor-agent/Invoices"

---

## Part 13: Save and Test

- [ ] **Step 1.** Click `Save` in the top right corner

- [ ] **Step 2.** Wait for the "Your flow is ready" message

- [ ] **Step 3.** Open SharePoint in a new tab

- [ ] **Step 4.** Navigate to: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET/Shared Documents/document-processor-agent`

- [ ] **Step 5.** Upload a test file named: `test-invoice-001.pdf`

- [ ] **Step 6.** Wait 1-2 minutes for the flow to trigger

- [ ] **Step 7.** Check the `Invoices` subfolder for your file

- [ ] **Step 8.** Check your Teams channel for the notification

---

## Visual Flow Summary

When complete, your flow should look like this:

```
[When a file is created (properties only)]
              |
              v
[Initialize variable: DestinationFolder]
              |
              v
[Condition: Name contains "invoice"]
    |                    |
  Yes                   No
    |                    |
    v                    v
[Set variable:     [Condition: Name contains "contract"]
 /Invoices]            |                    |
                     Yes                   No
                       |                    |
                       v                    v
               [Set variable:     [Condition: Name contains "resume"]
                /Contracts]           |                    |
                                    Yes                   No
                                      |                    |
                                      v                    v
                              [Set variable:     [Set variable:
                               /Resumes]          /Exceptions]
              |
              v
[Move file to DestinationFolder]
              |
              v
[Post message in Teams]
```

---

## Quick Reference: Key Settings

| Setting | Value |
|---------|-------|
| SharePoint Site | `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET` |
| Library | `Shared Documents` |
| Watch Folder | `/document-processor-agent` |
| Invoice Destination | `/document-processor-agent/Invoices` |
| Contract Destination | `/document-processor-agent/Contracts` |
| Resume Destination | `/document-processor-agent/Resumes` |
| Exception Destination | `/document-processor-agent/Exceptions` |

---

## Troubleshooting

### Flow Does Not Trigger

**Symptom:** You upload a file but nothing happens.

**Check these things:**

- [ ] Is the flow turned on? Go to `My flows` and check the toggle is On
- [ ] Is the folder path correct? Must be `/document-processor-agent` with the leading slash
- [ ] Are the SharePoint connections valid? Click the flow, then `Edit`, then check for warning icons

**Try this:** In Power Automate, click your flow name, then click `Run history`. If there are no entries, the trigger is not firing.

---

### File Does Not Move

**Symptom:** Flow runs but file stays in the original folder.

**Check these things:**

- [ ] Does the destination folder exist in SharePoint?
- [ ] Do you have write permissions to the destination folder?
- [ ] Open the failed run and click `Move file` to see the error message

**Common error:** "Item does not exist" means the folder path is wrong. Double-check spelling and slashes.

---

### Teams Message Not Posting

**Symptom:** File moves correctly but no Teams notification.

**Check these things:**

- [ ] Is the Teams connection authorized? Look for a warning icon on the Teams action
- [ ] Do you have permission to post in the selected channel?
- [ ] Is the Flow bot enabled in your team?

**Try this:** Click on the Teams action in your flow and click `Change connection` to reauthorize.

---

### File Classified Incorrectly

**Symptom:** An invoice goes to Contracts folder.

**Check these things:**

- [ ] Does the file name contain multiple keywords? (e.g., "invoice-contract-review.pdf")
- [ ] The flow checks in order: invoice first, then contract, then resume
- [ ] Rename your test file to contain only one keyword

**How to fix:** If your files commonly have multiple keywords, add more specific conditions (e.g., check if it starts with "INV-" for invoices).

---

### Flow Runs But Shows "Failed"

**Symptom:** Red X on the flow run.

**Check these things:**

- [ ] Click the failed run to see which step failed
- [ ] Expand the failed step to read the error message
- [ ] Most common: permission issues or missing folders

**Quick fix for permissions:** Ask your SharePoint admin to grant you "Edit" access to the document library.

---

## Test Files to Try

Upload these files to test each path:

| File Name | Expected Destination |
|-----------|---------------------|
| `test-invoice-001.pdf` | Invoices/ |
| `vendor-invoice-acme.docx` | Invoices/ |
| `contract-renewal-2025.pdf` | Contracts/ |
| `resume-jane-doe.docx` | Resumes/ |
| `random-document.pdf` | Exceptions/ |

---

## What is Next

After this flow is working:

1. **Add more keywords:** Check for "PO", "purchase order", "CV", "curriculum vitae"
2. **Add email notifications:** Send an email when files go to Exceptions
3. **Add approval:** Route high-value items for manager approval
4. **Upgrade to AI:** Replace keyword matching with AI Builder document classification

See [QUICK-START-TRIGGERS.md](./QUICK-START-TRIGGERS.md) for the full Copilot Studio integration with AI Builder.

---

## Documentation Links

- [SharePoint connector reference](https://learn.microsoft.com/connectors/sharepointonline/)
- [Teams connector reference](https://learn.microsoft.com/connectors/teams/)
- [Power Automate conditions](https://learn.microsoft.com/power-automate/use-expressions-in-conditions)
- [Troubleshoot flow failures](https://learn.microsoft.com/power-automate/fix-flow-failures)

---

*Last updated: December 2024*
*Tested with: Power Automate (December 2024 release)*

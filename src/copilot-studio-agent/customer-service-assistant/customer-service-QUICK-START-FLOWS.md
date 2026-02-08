# Quick-Start: Power Automate Flow

**For:** Customer Service Assistant Agent
**Time:** 15-20 minutes
**Skill level:** Beginner

---

## What You Will Build

One simple flow that captures incoming support emails and logs them to SharePoint for tracking.

| Flow | What It Does |
|------|--------------|
| New Support Email to SharePoint | When email arrives, create a tracking item in SharePoint |

---

## Before You Start

You need:

- [ ] Microsoft 365 account with Power Automate access
- [ ] Access to Outlook (Office 365)
- [ ] Access to SharePoint site: `timwinfo2.sharepoint.com/sites/CERTSTAR.NET`
- [ ] About 15-20 minutes of focused time

---

## Key Terms (Read First)

| Term | Plain English |
|------|---------------|
| **Power Automate** | A tool that connects apps and automates tasks. Like setting up dominoes that fall automatically. |
| **Flow** | A series of automated steps. Like a recipe that runs itself. |
| **Trigger** | The event that starts a flow. Like pressing a button that starts the dominoes. |
| **Action** | One step in a flow. Like one domino falling. |
| **Connector** | A pre-built connection to an app (Outlook, SharePoint, Teams). Like a plug that fits a specific outlet. |

---

## Part 1: Create the SharePoint List

**Goal:** Create a place to store incoming support requests.

---

### Step 1: Open SharePoint

- [ ] Go to `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`
- [ ] Sign in with your Microsoft account

---

### Step 2: Navigate to the document library

- [ ] Click `Shared Documents` in the left sidebar
- [ ] Navigate to or create a folder called `customer-service-assistant`

---

### Step 3: Create a new list

- [ ] Click `+ New` in the top toolbar
- [ ] Select `List`
- [ ] Select `Blank list`
- [ ] Name it: `Support Requests`
- [ ] Click `Create`

---

### Step 4: Add columns to the list

You need to add four columns. For each column:

- [ ] Click `+ Add column` in the list header
- [ ] Select the column type
- [ ] Enter the name
- [ ] Click `Save`

| Column Name | Type | Purpose |
|-------------|------|---------|
| Subject | Single line of text | Email subject line |
| CustomerEmail | Single line of text | Sender's email address |
| EmailBody | Multiple lines of text | Content of the email |
| ReceivedDate | Date and time | When the email arrived |

**Note:** The `Title` column already exists. You can use it or leave it for the flow to populate.

---

### Step 5: Copy the list URL

- [ ] Look at your browser address bar
- [ ] Copy the URL (you will need it later)
- [ ] It looks like: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET/Lists/Support%20Requests`

**Checkpoint: SharePoint list created.**

---

## Part 2: Create the Power Automate Flow

**Goal:** When a support email arrives, automatically log it to SharePoint.

---

### Step 1: Open Power Automate

- [ ] Go to [make.powerautomate.com](https://make.powerautomate.com)
- [ ] Sign in with your Microsoft account
- [ ] Make sure you are in the correct environment (top-right corner)

---

### Step 2: Start a new flow

- [ ] Click `+ Create` in the left sidebar
- [ ] Select `Automated cloud flow`

---

### Step 3: Name your flow

- [ ] In the **Flow name** field, type: `Support Email to SharePoint`
- [ ] In the search box under **Choose your flow's trigger**, type: `when a new email arrives`
- [ ] Select `When a new email arrives (V3)` from **Office 365 Outlook**
- [ ] Click `Create`

**Why this trigger?**
The Outlook connector is one of the most mature and reliable connectors. It uses your existing Microsoft 365 authentication automatically.

---

### Step 4: Configure the email trigger

The trigger block appears on the canvas. Configure it:

- [ ] Click on the trigger block to expand it
- [ ] Click `Show advanced options`

Set these options:

| Setting | Value | Why |
|---------|-------|-----|
| **Folder** | Inbox (or a specific subfolder) | Where to watch for emails |
| **Include Attachments** | No | Keep it simple for now |
| **Subject Filter** | `Support:` or leave blank | Filter specific emails (optional) |

- [ ] Click outside the block to collapse it

**Tip:** If you want to filter emails, you can set the Subject Filter to only capture emails with "Support:" in the subject line.

---

### Step 5: Add the SharePoint action

- [ ] Click `+ New step` below the trigger
- [ ] In the search box, type: `create item`
- [ ] Select `Create item` from **SharePoint**

---

### Step 6: Configure the SharePoint connection

If this is your first time using SharePoint in Power Automate:

- [ ] A sign-in prompt appears
- [ ] Click `Sign in`
- [ ] Enter your Microsoft 365 credentials
- [ ] Click `Accept` to grant permissions

**Why this works easily:**
SharePoint uses the same Microsoft 365 authentication as Outlook. No API keys or complex setup needed.

---

### Step 7: Configure the SharePoint action

Fill in these fields:

| Field | Value | How to Set |
|-------|-------|------------|
| **Site Address** | `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET` | Type or select from dropdown |
| **List Name** | `Support Requests` | Select from dropdown after choosing site |

---

### Step 8: Map email fields to list columns

After selecting the list, your custom columns appear. Click in each field and select the **dynamic content** from the email trigger:

| List Column | Dynamic Content to Select |
|-------------|---------------------------|
| **Title** | `Subject` (from the trigger) |
| **Subject** | `Subject` (from the trigger) |
| **CustomerEmail** | `From` (from the trigger) |
| **EmailBody** | `Body` (from the trigger) |
| **ReceivedDate** | `Received Time` (from the trigger) |

To add dynamic content:

- [ ] Click in the field
- [ ] A popup appears with `Dynamic content` tab
- [ ] Click on the value you want to insert (it has a lightning bolt icon)

---

### Step 9: Save the flow

- [ ] Click `Save` in the top-right corner
- [ ] Wait for the "Your flow is ready" message

**Checkpoint: Flow created and saved.**

---

## Part 3: Test the Flow

**Goal:** Verify the flow works correctly.

---

### Step 1: Send a test email

- [ ] Open Outlook (web or desktop)
- [ ] Send an email TO yourself (or the monitored mailbox)
- [ ] Subject: `Support: Test request from Quick Start guide`
- [ ] Body: `This is a test email to verify the Power Automate flow is working correctly.`
- [ ] Click `Send`

---

### Step 2: Check the flow run

- [ ] Go back to Power Automate
- [ ] Click on your flow name (`Support Email to SharePoint`)
- [ ] Look at the **Run history** section at the bottom
- [ ] Wait 1-2 minutes for the flow to trigger

**Note:** Flows can take 1-5 minutes to trigger. The Outlook connector polls for new emails periodically.

---

### Step 3: Verify the run succeeded

- [ ] In Run history, look for a new entry
- [ ] The **Status** should show a green checkmark and say `Succeeded`
- [ ] Click on the run to see details

If you see a red X (Failed):
- [ ] Click on the failed run
- [ ] Expand each step to find the error
- [ ] See the Troubleshooting section below

---

### Step 4: Check SharePoint

- [ ] Go to `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`
- [ ] Open the `Support Requests` list
- [ ] Look for your test email entry
- [ ] Verify all columns are populated correctly

**Checkpoint: Flow tested and working.**

---

## Your Completed Flow (Visual Summary)

```
+----------------------------------+
|  TRIGGER                         |
|  When a new email arrives (V3)   |
|  Folder: Inbox                   |
+----------------------------------+
              |
              v
+----------------------------------+
|  ACTION                          |
|  Create item (SharePoint)        |
|  Site: CERTSTAR.NET              |
|  List: Support Requests          |
|  Title: [Subject]                |
|  CustomerEmail: [From]           |
|  EmailBody: [Body]               |
|  ReceivedDate: [Received Time]   |
+----------------------------------+
```

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Flow does not trigger | Email went to spam/junk | Check spam folder; move email to Inbox |
| Flow does not trigger | Wrong folder selected | Edit trigger; verify Folder setting |
| Flow does not trigger | Subject filter too strict | Remove or broaden the Subject Filter |
| SharePoint error: "List not found" | Site URL incorrect | Verify the exact Site Address URL |
| SharePoint error: "Access denied" | Missing permissions | Ask SharePoint admin for Contribute access |
| SharePoint error: "Column not found" | Column name mismatch | Check column names match exactly (case-sensitive) |
| Dynamic content not showing | Connection issue | Delete and re-add the SharePoint step |
| Flow takes too long to trigger | Normal behavior | Outlook trigger polls every 1-5 minutes |

---

## Common Questions

**Q: Can I use a shared mailbox instead of my personal inbox?**
A: Yes. In the trigger settings, click `Show advanced options` and enter the shared mailbox address in the `Original Mailbox Address` field.

**Q: Can I filter to only capture certain emails?**
A: Yes. Use the `Subject Filter` or `From` filter in the trigger's advanced options. You can also add a `Condition` action after the trigger.

**Q: What if I want to notify a Teams channel instead of SharePoint?**
A: Add a second action after the SharePoint step. Search for `Post message in a chat or channel` from the Microsoft Teams connector.

**Q: How do I turn off the flow temporarily?**
A: Open the flow, click the `...` menu (top-right), and select `Turn off`.

---

## What You Built

You now have:

- [x] A SharePoint list to track support requests
- [x] A Power Automate flow that automatically logs incoming emails
- [x] A foundation to expand with more automation

---

## Next Steps (Optional Enhancements)

When you are ready, you can expand this flow:

| Enhancement | How |
|-------------|-----|
| Add Teams notification | Add `Post message in a chat or channel` action |
| Categorize by subject keywords | Add `Condition` action to check subject content |
| Auto-assign priority | Add `Switch` action based on keywords like "urgent" |
| Connect to Copilot Studio | Use `HTTP` action to send data to your agent |

---

## Resources

- [Power Automate documentation](https://learn.microsoft.com/en-us/power-automate/)
- [Office 365 Outlook connector](https://learn.microsoft.com/en-us/connectors/office365/)
- [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepointonline/)
- [Create your first flow](https://learn.microsoft.com/en-us/power-automate/getting-started)

---

**Document version:** 2025-01
**Last verified against:** Power Automate web app (December 2024)
**SharePoint site:** `timwinfo2.sharepoint.com/sites/CERTSTAR.NET`

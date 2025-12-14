# Customer Service Assistant — Event Trigger: New Support Email → Triage + Teams Notify

## Goal
When a support email arrives (shared mailbox), the agent classifies intent/urgency and posts a summary into a Teams triage chat/channel.

## Event trigger choice
Use a **Power Automate** flow with an Outlook trigger (email received) and then send a proactive Teams message "as" the agent.

## Trigger payload fields (recommended)
- `ticketId` (string) — generated GUID
- `from` (string) — sender email
- `subject` (string)
- `receivedUtc` (string ISO-8601)
- `bodyPreview` (string, ~1-2k chars)
- `attachments` (array of {name,url}) optional
- `priorityHint` (string) optional

## Power Automate flow outline (pseudo-definition)
1. **Trigger**: Outlook — *When a new email arrives (V3)*
   - Mailbox: Shared mailbox `support@contoso.com`
   - Folder: Inbox
   - Only with attachments: optional
2. **Compose**: `ticketId = guid()`
3. **Compose**: `bodyPreview = substring(triggerBody()?['bodyPreview'], 0, 1500)`
4. **Microsoft Teams** — *Post message in a chat or channel*
   - **Post as**: *Microsoft Copilot Studio (Preview)*
   - **Post in**: *Chat with bot*
   - **Bot**: *Customer Service Assistant*
   - **Recipient**: `support-triage@contoso.com` (or individual UPN)
   - **Message**: Use the prompt block below

## Message prompt (paste as the Teams message)
Triage this new support email and propose next action.

Ticket: {ticketId}
From: {from}
Subject: {subject}
Received: {receivedUtc}
BodyPreview:
{bodyPreview}

Rules:
- Output a 6-line summary.
- Include: intent, urgency (low/med/high), product/sku if present, and a suggested reply draft.
- If it's a warranty/return/order-status question, cite the relevant policy from knowledge.
- If you need more info, list 3 questions to ask the customer.

## Notes
- The Teams proactive message pattern is documented by Microsoft. See Learn: *Send proactive Microsoft Teams messages*. 

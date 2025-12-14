# Employee Onboarding Agent — Event Trigger: New Hire Added → Welcome + Checklist

## Goal
When HR adds a new employee to your onboarding tracker (Dataverse or SharePoint list), the agent sends a proactive Teams welcome message with next steps and a checklist.

## Event trigger choice
Use **Dataverse** (preferred) or **SharePoint** "item created" triggers.
Then send a proactive Teams message from the agent.

## Trigger payload fields (recommended)
- `employeeId` (string)
- `displayName` (string)
- `email` (string)
- `managerEmail` (string)
- `startDate` (string)
- `role` (string)
- `location` (string)

## Power Automate flow outline (pseudo-definition)
1. **Trigger**: Dataverse — *When a row is added, modified or deleted*
   - Table: `NewHires`
   - Change type: Added
2. **Compose**: Build `welcomeMessage` using the prompt below.
3. **Teams** — *Post message in a chat or channel*
   - **Post as**: *Microsoft Copilot Studio (Preview)*
   - **Post in**: *Chat with bot*
   - **Bot**: *Employee Onboarding Agent*
   - **Recipient**: `email` (the new hire)
   - **Message**: `welcomeMessage`
4. Optional: Post a second message to the manager with a manager-specific checklist.

## Message prompt (paste as the Teams message)
You are the Contoso Employee Onboarding Agent.
Send a welcome message to the new hire and give them a Day 1 checklist.

New hire:
- Name: {displayName}
- Email: {email}
- Role: {role}
- Start date: {startDate}
- Location: {location}

Rules:
- Use short bullet points.
- Include the first 3 checklist items from the onboarding-checklist.csv knowledge file.
- Offer to help with IT equipment and policy acknowledgements.

## Notes
This uses the same proactive message technique described in Microsoft Learn.

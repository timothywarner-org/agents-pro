# Employee Onboarding Agent

Plan the onboarding automation agent that orchestrates HR tasks and approvals.

## Scenario Snapshot
- **Objective:** Guide new hires through onboarding steps, surface resources, and trigger approvals.
- **Channel targets:** Microsoft Teams, embedded SharePoint page.
- **Success metrics:** Task completion rate, approval turnaround time, handoff volume.

## Core Topics
- Map conversational checklists and state-tracking in `topics/`.
- Include authentication checkpoints when surfacing personalized data.
- Plan fallbacks that escalate to HR when prerequisites fail.

## Actions & Integrations
- Log Power Automate flows for provisioning tasks, Teams announcements, and email notifications in `actions/`.
- Note Dataverse tables or Microsoft Graph connectors needed for profile updates.

## Knowledge Sources
- Capture policy documents, FAQ PDFs, and SharePoint onboarding hubs in `knowledge/`.
- Flag content that requires version control or localization.

## Governance & Rollout
- Track environment-specific configuration (environments, security groups, DLP policies) to speed up solution promotion.

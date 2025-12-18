# Event Trigger + Automation Templates (Repo Additions)

These templates are **teaching artifacts**: they are not guaranteed import-ready Power Automate exports.
They are designed to be copy/paste friendly and map 1:1 to click paths in Copilot Studio and Power Automate.

See the chat response for click-exact steps and the rationale behind each automation.

## Naming Convention

All files follow the pattern: `{agent-prefix}-{trigger-name}[-payload].{ext}`

- **Agent prefix**: Identifies which agent the automation belongs to
- **Trigger name**: Describes the event trigger (e.g., `new-email`, `sharepoint-file-created`, `new-hire`)
- **-payload suffix**: Indicates sample JSON payload files
- **Extension**: `.md` for flow documentation, `.sample.json` for payloads

## Files by Agent

### Customer Service Assistant (`customer-service-`)

| File | Description |
|------|-------------|
| `customer-service-new-email-triage.md` | Power Automate flow for email triage and Teams notification |
| `customer-service-new-email-payload.sample.json` | Sample trigger payload for new support emails |

### Employee Onboarding Agent (`employee-onboarding-`)

| File | Description |
|------|-------------|
| `employee-onboarding-new-hire.md` | Power Automate flow for new hire welcome messages |
| `employee-onboarding-new-hire-payload.sample.json` | Sample trigger payload for new employee records |

### Document Processor Agent (`document-processor-`)

| File | Description |
|------|-------------|
| `document-processor-sharepoint-file-created.md` | Event trigger for SharePoint document classification and routing |
| `document-processor-sharepoint-file-created-payload.sample.json` | Sample trigger payload for SharePoint file events |

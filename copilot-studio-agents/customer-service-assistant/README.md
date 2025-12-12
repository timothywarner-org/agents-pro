# Customer Service Assistant Agent

Use this folder to plan custom topics, actions, and knowledge sources for the support-focused agent.

## Scenario Snapshot
- **Objective:** Resolve tier-one support questions with curated knowledge and escalation pathways.
- **Channel targets:** Microsoft Teams, web demo site.
- **Success metrics:** Resolution rate, customer satisfaction trend, escalation volume (per [analytics guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-improve-agent-effectiveness)).

## Core Topics
- Define greeting, escalation, and FAQ topics in `topics/`.
- Document trigger phrases and expected user journeys for each topic.
- Note hand-offs to live agents using the Escalate system topic.

## Actions & Integrations
- Catalogue Power Automate flows and connectors in `actions/`.
- Capture connection references, environment variables, and Dataverse tables needed for deployment.

## Knowledge Sources
- Track SharePoint libraries, website URLs, and file uploads in `knowledge/`.
- Flag content that requires generative answers versus scripted responses.

## Governance & Rollout
- Record testing checkpoints, analytics dashboards, and production readiness sign-off here before exporting the agent as a managed solution.

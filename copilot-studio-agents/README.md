# Copilot Studio Agent Scaffolding

This scaffold organizes planning artifacts for the three agents we’ll build during the O’Reilly live course. The structure aligns with Microsoft Copilot Studio guidance on [planning conversational AI projects](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/project-best-practices) and [topics best practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/topics-overview).

## Layout
- `customer-service-assistant/` — knowledge-driven support agent for internal and external FAQs.
- `employee-onboarding-agent/` — HR process automation with approvals and task orchestration.
- `document-processor-agent/` — autonomous trigger-based workflow for document classification.

Each agent folder contains:
- `topics/` — conversation paths to author in Copilot Studio, including trigger phrases and dialog logic.
- `actions/` — Power Automate flows, connectors, and tool integrations referenced by topics.
- `knowledge/` — data sources, generative answers configuration, and SharePoint/OneDrive references.

## Authoring Checklist
1. Define business goals and success metrics before creating custom topics.
2. Avoid periods (`.`) in topic names to keep solution exports compliant.
3. Create topics with Copilot or manually, then layer guardrails with system topics.
4. Use generative answers sparingly; back them with curated knowledge sources.
5. Capture environment variables and connection references in the `actions` notes for ALM readiness.
6. Publish updates to a sandbox environment first, then promote via managed solutions.

## Next Steps
- Complete the `README.md` and checklists in each agent folder prior to building agents in Copilot Studio.
- Track analytics configuration and live channel deployment details alongside the scaffold so the team can reference them after the course.

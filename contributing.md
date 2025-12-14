# Contributing Guide

## Repository Purpose
- Serve as the instructor playbook for the four-hour O'Reilly course described in [README.md](README.md) and [course-plan.md](course-plan.md).
- Keep every artifact aligned with the agent scaffolds in [copilot-studio-agents/README.md](copilot-studio-agents/README.md) and the marketing collateral housed in [reference/](reference/how-to-create-ai-agents-like-a-pro-markdown.md).
- Capture real learner feedback, success metrics, and environment prerequisites so future cohorts launch smoothly.

## Before You Start
- Review the agent build guides for [Hour 2](copilot-studio-agents/customer-service-assistant/README.md), [Hour 3](copilot-studio-agents/employee-onboarding-agent/README.md), and [Hour 4](copilot-studio-agents/document-processor-agent/README.md).
- Confirm your proposed change supports the Overview → Scenario → Success Metrics → Phased Build → Testing/Publishing → Sample cadence used throughout the repo.
- Check existing issues to ensure the topic is not already being tracked.

## Contribution Workflow
1. **Discuss**: Open an issue summarizing learner problem statements, desired outcomes, and affected files.
2. **Plan**: Outline agenda timing changes, flow dependencies, and Microsoft documentation references to update.
3. **Implement**: Work in small, reviewable commits; update tables, diagrams, and environment notes together.
4. **Validate**: Compare against source materials in [reference/](reference/how-to-create-ai-agents-like-a-pro-training-proposal.md); run Markdown linting if available.
5. **Pull Request**: Link the tracking issue, provide a concise learner impact summary, and attach screenshots or Mermaid previews when visual assets change.
6. **Review**: Respond quickly to maintainer feedback; expect extra scrutiny for changes that influence live delivery sequencing.

## Style and Quality Checklist
- Headings use Title Case and preserve existing em dash formatting where present.
- Bulleted lists are compact, using `-` for each item.
- Mermaid diagrams maintain the color palette already used in agent guides.
- Connector licensing, authentication scopes, and environment variables are documented when Power Automate updates are introduced.
- External links point to official Microsoft or O'Reilly resources and are wrapped in angle brackets when displayed inline.

## Communication
Questions or urgent blockers? Contact **Tim Warner** at **tim@techtrainertim.com** or message via <https://techtrainertim.com>. Include repository links, learner impact, and desired delivery timeline in your note.
